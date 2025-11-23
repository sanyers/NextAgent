from fastapi import Depends, Header, HTTPException, status


async def require_token(authorization: str | None = Header(default=None)) -> str:
    """
    校验请求头中的 Bearer Token，非 auth 模块接口默认依赖此函数。

    Args:
        authorization: Authorization 请求头

    Raises:
        HTTPException: 当 Token 缺失或格式错误时抛出 401
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少或非法的 Authorization 头",
        )
    return authorization.removeprefix("Bearer ").strip()


def get_current_user(token: str = Depends(require_token)) -> dict[str, str]:
    """
    简化示例：根据 token 返回当前用户信息。
    实际项目中应解析 JWT 并查询用户。

    Args:
        token: 经过 require_token 验证后的 token 字符串

    Returns:
        伪造用户信息
    """
    return {"user_id": "demo", "token": token}


