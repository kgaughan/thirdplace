import hashlib
import typing as t
from urllib import parse


def gravatar(email: str, size: int = 64, default: t.Optional[str] = None) -> str:
    email_hash = hashlib.md5(email.lower().encode("utf-8")).hexdigest()  # noqa: S324
    params = {"s": str(size)}
    if default is not None:
        params["d"] = default
    return f"https://www.gravatar.com/avatar/{email_hash}?{parse.urlencode(params)}"
