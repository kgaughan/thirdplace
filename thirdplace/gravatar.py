import hashlib
import typing as t
from urllib import parse

URL_TEMPLATE = "https://www.gravatar.com/avatar/{}?{}"


def gravatar(email: str, size: int = 64, default: t.Optional[str] = None):
    email_hash = hashlib.md5(email.lower().encode("utf-8")).hexdigest()
    params = {"s": str(size)}
    if default is not None:
        params["d"] = default
    return URL_TEMPLATE.format(email_hash, parse.urlencode(params))
