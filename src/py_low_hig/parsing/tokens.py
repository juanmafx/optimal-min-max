MAX_TOKEN_LENGTH = 4096
STOP_WORD = "done"


def parse_integer(token: str) -> int | None:
    if len(token) > MAX_TOKEN_LENGTH:
        return None
    try:
        return int(token)
    except ValueError:
        return None
