import hashlib
from typing import Optional
from urllib import parse

URL_TEMPLATE = "https://www.gravatar.com/avatar/{}?{}"


def gravatar(email, size: int = 64, default: Optional[str] = None):
    email_hash = hashlib.md5(email.lower().encode("utf-8")).hexdigest()
    params = {"s": size}
    if default is not None:
        params["d"] = default
    return URL_TEMPLATE.format(email_hash, parse.urlencode(params))
