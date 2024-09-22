
import time
from datetime import datetime
class response:

    def __init__(self):
        self.errors = []
        self._response = {}
        self._id = 11
        self.status = 'failed' 
        self.start_time = None
        self.stop_time = None
        self.request = ''
        self.suggestions = []


    def response_construct(self)->dict:
        res = {
                "request_id" : self._id,
                "alias" : "wlan0 config",
                "request" : self.request,
                "status" : self.status,
                "errors" : self.errors,
                "timestamp":
                {
                    "start":self.start_time,
                    "end":self.start_time,
                },

                "logs": "",
                "suggestions" : self.suggestions

            }
                
        return res
    def get_response(self)->dict:
        self.stop_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.response_construct()