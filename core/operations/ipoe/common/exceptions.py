# core/operations/ipoe/common/exceptions.py

class IPOEError(Exception):
    pass


class UnsupportedVendor(IPOEError):
    pass


class ParseError(IPOEError):
    pass
