import os
import ast
import inspect
import textwrap

from decorators import interface


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
            
    for node in ast.walk(mod):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func.__name__:
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
    node = _find_func_node_from_file(func)
    if node is not None:
        return node
    
    return _find_func_node_from_snippet(func)


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


class _InterfaceMeta(type):
    
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        cls._is_interface_ = getattr(cls, "_is_interface_", None)
        cls._interface_contracts_ = set()
        return cls
    
    
    def __call__(cls, *args, **kwargs):
        if getattr(cls, "_is_interface_", False):
            raise TypeError(f"Cannot instantiate interface class '{cls.__name__}'")
        return super().__call__(*args, **kwargs)
    

    def __validate__(cls):
        if cls._is_interface_ is None:
            del cls
            raise TypeError(
                f"Class must be decorated with @interface or @concrete"
            )

        if cls._is_interface_:
            # enforce interface
            for attr, value in list(vars(cls).items()):
                if attr.startswith("__") and attr.endswith("__"):
                    continue
                if attr in ("__annotations__", "_is_interface_", "_interface_contracts_"):
                    continue

                if inspect.isfunction(value):
                    if not _is_empty_function(value):
                        cls_name = cls.__name__
                        del cls
                        raise TypeError(
                            f"Method '{attr}' in interface '{cls_name}' must have empty body."
                        )
                    cls._interface_contracts_.add(attr)
                    continue

                if isinstance(value, staticmethod):
                    if not _is_empty_function(value.__func__):
                        cls_name = cls.__name__
                        del cls
                        raise TypeError(
                            f"Static method '{attr}' in interface '{cls_name}' must have empty body."
                        )
                    cls._interface_contracts_.add(attr)
                    continue

                if isinstance(value, classmethod):
                    if not _is_empty_function(value.__func__):
                        cls_name = cls.__name__
                        del cls
                        raise TypeError(
                            f"Class method '{attr}' in interface '{cls_name}' must have empty body."
                        )
                    cls._interface_contracts_.add(attr)
                    continue

                if isinstance(value, property):
                    if value.fget and not _is_empty_function(value.fget):
                        cls_name = cls.__name__
                        del cls
                        raise TypeError(
                            f"Property getter '{attr}' in interface '{cls_name}' must have empty body."
                        )
                    if value.fset and not _is_empty_function(value.fset):
                        cls_name = cls.__name__
                        del cls
                        raise TypeError(
                            f"Property setter '{attr}' in interface '{cls_name}' must have empty body."
                        )
                    cls._interface_contracts_.add(attr)
                    continue
                
                cls_name = cls.__name__
                del cls
                raise TypeError(
                    f"Attribute '{attr}' in interface '{cls_name}' should not have a value."
                )


            # inherit contracts from parents
            for base in cls.__mro__[1:]:
                if hasattr(base, "_interface_contracts_"):
                    cls._interface_contracts_ |= base._interface_contracts_

        else:
            # enforce concrete
            contracts = set()
            for base in cls.__mro__[1:]:
                if hasattr(base, "_interface_contracts_"):
                    contracts |= base._interface_contracts_

            missing = []
            for contract in contracts:
                impl = getattr(cls, contract, None)
                if impl is None or _is_empty_function(impl):
                    missing.append(contract)

            if missing:
                cls_name = cls.__name__
                del cls
                raise TypeError(
                    f"Concrete class '{cls_name}' must implement contracts: {', '.join(missing)}"
                )


@interface
class InterfaceBase(metaclass=_InterfaceMeta):
    pass
