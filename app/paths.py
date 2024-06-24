TRAILING_SLASH = "/"

# Accepted paths

BASE_PATH = ""  # Path '/' when trailing is removed -> split("/").
ECHO_PATH = "echo"


PATHS = [
    BASE_PATH,
    ECHO_PATH,
]


def parse_path(path):
    try:
        _, endpoint, data = path.split(TRAILING_SLASH)
    except ValueError:  # There is no data sent (no data to unpack)
        _, endpoint = path.split(TRAILING_SLASH)
        data = ""

    if endpoint in PATHS:
        return True, data

    return False, ""
