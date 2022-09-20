from collections import namedtuple
from sys import argv

from pydantic import BaseModel
from requests import get


class VersionResponse(BaseModel):
    version: str = "v0.0.0"
    revision: str = "0000000"


def make_call(url: str, timeout: int = 9_000) -> VersionResponse:
    return VersionResponse.parse_obj(get(f"{url}/api/info", timeout=timeout, verify=False).json())


if __name__ == "__main__":
    InputData = namedtuple("InputData", ["url", "version", "revision"])
    input_data = InputData(url=argv[1], version=argv[2], revision=argv[3])

    version_response = make_call(input_data.url)

    assert input_data.version == version_response.version, \
        f"Is {input_data.version} should be {version_response.version}"
    assert input_data.revision == version_response.revision, \
        f"Is {input_data.revision} should be {version_response.revision}"
