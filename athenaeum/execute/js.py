from typing import Any


def execute_js_code_by_PyExecJS(js_code: str, func_name: str, *args: Any, **kwargs: Any) -> Any:  # noqa
    import execjs

    ctx = execjs.compile(js_code)
    result = ctx.call(func_name, *args, **kwargs)
    return result


def execute_js_code_by_py_mini_racer(js_code: str, func_name: str, *args: Any, **kwargs: Any) -> Any:
    import py_mini_racer

    ctx = py_mini_racer.MiniRacer()
    ctx.eval(js_code)
    result = ctx.call(func_name, *args, **kwargs)
    return result
