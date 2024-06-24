# Accepted paths

BASE_PATH = "/"
ECHO_PATH = "echo"


PATHS = [
    BASE_PATH,
    ECHO_PATH,
]


def parse_path(path):
    _, endpoint, data = path.split(BASE_PATH)

    if endpoint in PATHS:
        return True, data

    return False, ""
