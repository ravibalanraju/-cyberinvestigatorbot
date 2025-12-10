# src/utils/portscan.py

import nmap
from src.logger import logger
from src.config import FORBIDDEN_DOMAINS

nm = nmap.PortScanner()

TOP_30 = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 
    443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080,
    53, 67, 68, 161, 162, 389, 636, 9200, 10000
]

TOP_100 = TOP_30 + [i for i in range(1024, 1124)]


def is_forbidden(ip_or_host):
    for f in FORBIDDEN_DOMAINS:
        if str(ip_or_host).endswith(f):
            return True
    return False


def scan_ports(ip, ports=" ".join(map(str, TOP_30))):
    if is_forbidden(ip):
        return None

    try:
        res = nm.scan(hosts=str(ip), ports=ports, arguments='-sS -T4')
        return res
    except Exception:
        logger.exception("Nmap scan failed")
        return None
