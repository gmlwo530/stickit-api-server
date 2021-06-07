from typing import Any, Dict, List
from pydantic import BaseModel

STATUS_CODE_MSG = {
    400: "The server cannot or will not process the request due to something that is perceived to be a client error",
    401: "Request has not been applied because it lacks valid authentication credentials for the target resource.",
    403: "Server understood the request but refuses to authorize it.",
    404: "Not found"
}

class ResMsg(BaseModel):
    detail: str

    @classmethod
    def get_res_msg(cls, status_codes: List[int]=[]) -> Dict[int, Dict[str, Any]]:
        return {
            status_code: {
                "model": cls,
                "description": STATUS_CODE_MSG[status_code]
            }
            for status_code in status_codes
        }

    