import os
import ast
import inspect
import textwrap

from abc import ABCMeta

# TODO: Refactor


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
    except Exception:
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

class _InterfaceMeta(ABCMeta):
    def __call__(cls, *args, **kwargs):
        # فقط اگر خودِ کلاس Interface باشه → نمونه‌سازی ممنوع
        if InterfaceBase in cls.__bases__:
            raise TypeError(f"Cannot instantiate interface class '{cls.__name__}'")
        return super().__call__(*args, **kwargs)

    def __new__(mcls, name, bases, namespace):
        if name == "InterfaceBase":
            return super().__new__(mcls, name, bases, namespace)

        is_interface = InterfaceBase in bases

        if is_interface:
            interface_methods = {}
            for attr, value in list(namespace.items()):
                if attr.startswith("__") and attr.endswith("__"):
                    continue
                if attr == "__annotations__":
                    continue

                if inspect.isfunction(value):
                    if not _is_empty_function(value):
                        raise TypeError(f"Method '{attr}' in interface '{name}' must have empty body.")
                    interface_methods[attr] = "method"
                    continue

                if isinstance(value, staticmethod):
                    if not _is_empty_function(value.__func__):
                        raise TypeError(f"Static method '{attr}' in interface '{name}' must have empty body.")
                    interface_methods[attr] = "staticmethod"
                    continue

                if isinstance(value, classmethod):
                    if not _is_empty_function(value.__func__):
                        raise TypeError(f"Class method '{attr}' in interface '{name}' must have empty body.")
                    interface_methods[attr] = "classmethod"
                    continue

                if isinstance(value, property):
                    if value.fget and not _is_empty_function(value.fget):
                        raise TypeError(f"Property getter '{attr}' in interface '{name}' must have empty body.")
                    if value.fset and not _is_empty_function(value.fset):
                        raise TypeError(f"Property setter '{attr}' in interface '{name}' must have empty body.")
                    interface_methods[attr] = "property"
                    continue

                if isinstance(value, type):
                    continue

                raise TypeError(f"Attribute '{attr}' in interface '{name}' should not have a value.")

            namespace["_interface_contracts_"] = interface_methods

        else:
            contracts = {}
            for base in bases:
                if hasattr(base, "_interface_contracts_"):
                    contracts.update(base._interface_contracts_)

            for method_name, kind in contracts.items():
                if method_name not in namespace:
                    raise TypeError(
                        f"Class '{name}' must implement '{method_name}' from interface '{base.__name__}'"
                    )

                value = namespace[method_name]
                if kind == "method" and (not inspect.isfunction(value) or _is_empty_function(value)):
                    raise TypeError(f"Method '{method_name}' in '{name}' must implement interface method.")
                if kind == "staticmethod" and (
                    not isinstance(value, staticmethod) or _is_empty_function(value.__func__)
                ):
                    raise TypeError(f"Static method '{method_name}' in '{name}' must implement interface method.")
                if kind == "classmethod" and (
                    not isinstance(value, classmethod) or _is_empty_function(value.__func__)
                ):
                    raise TypeError(f"Class method '{method_name}' in '{name}' must implement interface method.")
                if kind == "property":
                    if not isinstance(value, property):
                        raise TypeError(f"Property '{method_name}' in '{name}' must implement interface property.")
                    if value.fget is None or _is_empty_function(value.fget):
                        raise TypeError(f"Property getter '{method_name}' in '{name}' must implement interface.")
        
        return super().__new__(mcls, name, bases, namespace)


class InterfaceBase(metaclass=_InterfaceMeta):
    pass
