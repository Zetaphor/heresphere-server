import netifaces
import socket
from logger_config import get_logger

logger = get_logger()

def get_all_ips():
    """
    Returns a dictionary with IP addresses for each network interface.
    """
    ip_addresses = {}
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        # Check if AF_INET key exists to get IPv4 addresses
        if netifaces.AF_INET in addresses:
            ipv4_addresses = addresses[netifaces.AF_INET]
            ip_addresses[interface] = [ip_info['addr'] for ip_info in ipv4_addresses]
    return ip_addresses

def get_lan_ip():
    """
    Returns the LAN IP address of the machine.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Note: No actual data is sent to the server, we just need a connection object
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            return ip
    except Exception as e:
        logger.error(f"Error getting LAN IP: {e}")
        return None
