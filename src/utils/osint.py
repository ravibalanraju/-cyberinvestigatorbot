# src/utils/osint.py

import whois
import dns.resolver
import requests
from src.logger import logger


def whois_lookup(domain):
    try:
        return whois.whois(domain)
    except Exception:
        logger.exception("WHOIS lookup failed")
        return None


def dns_records(domain):
    recs = {}
    try:
        for rtype in ["A", "AAAA", "MX", "NS", "TXT"]:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                recs[rtype] = [str(a) for a in answers]
            except Exception:
                recs[rtype] = []
    except Exception:
        pass
    return recs


def check_breach(email):
    # TODO: integrate with HaveIBeenPwned API
    return None
