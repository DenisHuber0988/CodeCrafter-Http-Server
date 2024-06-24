TRAILING_SLASH = "/"

# Accepted paths

BASE_PATH = ""  # Path '/' when trailing is removed -> split("/").
ECHO_PATH = "echo"
USER_AGENT_PATH = "user-agent"


PATHS = [
    BASE_PATH,
    ECHO_PATH,
    USER_AGENT_PATH
]


def parse_path(path: str, headers: list) -> tuple[bool, str]:
    try:
        _, endpoint, data = path.split(TRAILING_SLASH)
    except ValueError:  # There is no data sent (no data to unpack)
        _, endpoint = path.split(TRAILING_SLASH)
        data = ""

    if endpoint in PATHS:

        if endpoint == USER_AGENT_PATH:
            # Return the version of the product (User-Agent)
            user_agent_header = headers[0]
            _, version = user_agent_header.split(" ")
            return True, version

        return True, data

    return False, ""
