from iop import BusinessService

from models.schemas import AudioUploadRequest, AudioQueryRequest
from interop.msg import HttpMessageResponse


class BS(BusinessService):
    def on_message(self, request) -> HttpMessageResponse:
        if isinstance(request, AudioUploadRequest):
            return self.send_request_sync("EmbedBO", request)
        elif isinstance(request, AudioQueryRequest):
            return self.send_request_sync("QueryBO", request)
        else:
            raise ValueError("Unknown request type")
