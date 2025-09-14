import os
import ast
import inspect
import textwrap
from abc import ABCMeta


def _find_func_node_from_file(func):
    try:
        source_file = inspect.getsourcefile(func) or inspect.getfile(func)
    except (TypeError, OSError):
        return None
    
    if not source_file or not os.path.exists(source_file):
        return None
    
    with open(source_file, "r", encoding="utf-8") as f:
        src = f.read()
        
    try:
        mod = ast.parse(src)
    except SyntaxError:
        return None
    
    target_lineno = getattr(func, "__code__", None) and func.__code__.co_firstlineno
    for node in ast.walk(mod):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func.__name__:
            if getattr(node, "lineno", None) == target_lineno:
                return node
            
    return None


def _find_func_node_from_snippet(func):
    try:
        src_snip = inspect.getsource(func)
    except (OSError, TypeError, IOError):
        return None
    
    src_snip = textwrap.dedent(src_snip)
    try:
        mod = ast.parse(src_snip)
    except SyntaxError:
        return None
    
    for node in ast.walk(mod):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func.__name__:
            return node
        
    return None


def _get_function_ast_node(func):
    return _find_func_node_from_file(func) or _find_func_node_from_snippet(func)


def _is_ast_body_empty(node: ast.AST) -> bool:
    if not node or not hasattr(node, "body"):
        return False
    
    body = node.body
    if len(body) == 0:
        return True
    
    if len(body) == 1:
        stmt = body[0]
        if isinstance(stmt, ast.Pass):
            return True
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
            return True
        
    return False


def _is_empty_function(func) -> bool:
    node = _get_function_ast_node(func)
    if node is not None:
        return _is_ast_body_empty(node)
    code = getattr(func, "__code__", None)
    if code is None:
        return False
    
    co_names = getattr(code, "co_names", ())
    co_consts = getattr(code, "co_consts", ())
    if not co_names and (co_consts == (None,) or co_consts == (None,)):
        return True
    
    return False


def _collect_interface_contracts_from_mro(cls):
    contracts = {}
    for base in cls.__mro__:
        if getattr(base, "_is_interface_", False):
            parent_contracts = getattr(base, "_interface_contracts_", {})
            for name, kind in parent_contracts.items():
                contracts[name] = kind
                
    return contracts


def _has_nonempty_implementation(cls, name, kind):
    try:
        val = inspect.getattr_static(cls, name)
    except AttributeError:
        return False

    if kind == "property":
        if isinstance(val, property):
            fget = val.fget
            return (fget is not None) and (not _is_empty_function(fget))
        return False

    if isinstance(val, staticmethod):
        return not _is_empty_function(val.__func__)

    if isinstance(val, classmethod):
        return not _is_empty_function(val.__func__)

    if inspect.isfunction(val):
        return not _is_empty_function(val)

    func = getattr(val, "__func__", None)
    if func and hasattr(func, "__code__"):
        return not _is_empty_function(func)

    return False


class _InterfaceMeta(ABCMeta):
    def __call__(cls, *args, **kwargs):
        if getattr(cls, "_is_interface_", False):
            raise TypeError(f"Cannot instantiate interface class '{cls.__name__}'")
        return super().__call__(*args, **kwargs)

    def __new__(mcls, name, bases, namespace):
        if name == "InterfaceBase":
            return super().__new__(mcls, name, bases, namespace)

        is_interface = namespace.get("__interface__", None)
        if is_interface is None:
            raise TypeError(f"Class '{name}' must be decorated with @interface or @concrete.")

        namespace.pop("__interface__", None)

        if is_interface:
            contracts = {}
            for base in bases:
                if getattr(base, "_is_interface_", False):
                    contracts.update(getattr(base, "_interface_contracts_", {}))

            for attr, value in list(namespace.items()):
                if attr.startswith("__") and attr.endswith("__"):
                    continue
                if attr == "__annotations__":
                    continue

                if inspect.isfunction(value):
                    if not _is_empty_function(value):
                        raise TypeError(f"Method '{attr}' in interface '{name}' must have empty body.")
                    contracts[attr] = "method"
                    continue

                if isinstance(value, staticmethod):
                    if not _is_empty_function(value.__func__):
                        raise TypeError(f"Static method '{attr}' in interface '{name}' must have empty body.")
                    contracts[attr] = "staticmethod"
                    continue

                if isinstance(value, classmethod):
                    if not _is_empty_function(value.__func__):
                        raise TypeError(f"Class method '{attr}' in interface '{name}' must have empty body.")
                    contracts[attr] = "classmethod"
                    continue

                if isinstance(value, property):
                    if value.fget and not _is_empty_function(value.fget):
                        raise TypeError(f"Property getter '{attr}' in interface '{name}' must have empty body.")
                    if value.fset and not _is_empty_function(value.fset):
                        raise TypeError(f"Property setter '{attr}' in interface '{name}' must have empty body.")
                    contracts[attr] = "property"
                    continue

                if isinstance(value, type):
                    continue

                raise TypeError(f"Attribute '{attr}' in interface '{name}' should not have a value.")

            namespace["_is_interface_"] = True
            namespace["_interface_contracts_"] = contracts

            return super().__new__(mcls, name, bases, namespace)

        else: # Concrete
            cls = super().__new__(mcls, name, bases, namespace)
            total_contracts = _collect_interface_contracts_from_mro(cls)

            missing = []
            for method_name, kind in total_contracts.items():
                if not _has_nonempty_implementation(cls, method_name, kind):
                    missing.append(method_name)

            if missing:
                raise TypeError(
                    f"Class '{name}' must implement the following members: {', '.join(missing)}"
                )

            cls._is_interface_ = False
            cls._interface_contracts_ = {}
            return cls


class InterfaceBase(metaclass=_InterfaceMeta):
    _is_interface_ = True
    _interface_contracts_ = {}
