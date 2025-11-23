from typing import Any


def success(*, data: Any = None, msg: str = "ok") -> dict[str, Any]:
    """
    构建统一成功响应结构。

    Args:
        data: 需要返回的业务数据
        msg: 描述信息

    Returns:
        统一的成功响应字典
    """
    return {
        "code": 1,
        "msg": msg,
        "data": data,
    }


def fail(*, msg: str = "error", data: Any = None, code: int = 0) -> dict[str, Any]:
    """
    构建统一失败响应结构。

    Args:
        msg: 错误描述
        data: 可选的补充数据
        code: 业务错误码

    Returns:
        统一的失败响应字典
    """
    return {
        "code": code,
        "msg": msg,
        "data": data,
    }


