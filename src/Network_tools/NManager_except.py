
class NetworkObjError(Exception):
    """Base class for exceptions"""
    pass

class NetworkManagerNotInstalled(NetworkObjError):
    """Exception raised if Network manager is not installed"""
    def __init__(self, value, message="Network manager is not installed!"):
        self.value = value
        self.msg  = message
        super().__init__(self.msg)

class IPv4_AddressInvalid(NetworkObjError):
    """Exception raised if the read ipv4 address is invalid"""
    def __init__(self, value, message="IPV4 address Invalid") -> None:
        self.value = value
        self.msg = message
        super().__init__(self.msg)

class SubprocessFailed(NetworkObjError):
    def __init__(self, value, message) -> None:
        self.value = value
        self.message = message
        super().__init__(self.msg)

class UnableToRetrive_SSID(NetworkObjError):
    def __init__(self, value, message) -> None:
        self.value = value
        self.message = message
        super().__init__(self.msg)
