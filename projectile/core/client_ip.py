"""
to use it we need to import it first. 
import core import client_ip

ip_info = client_ip.get(request)

request is API request(http request)
get() returns a tuple containing ip and ip type
"""

from ipware import get_client_ip


def get(request):
    ip, is_routeable = get_client_ip(request)
    if ip is None:
        ip = "0.0.0.0"
    else:
        if is_routeable:
            ip_version = "Public"
        else:
            ip_version = "Private"
    return (ip, ip_version)
