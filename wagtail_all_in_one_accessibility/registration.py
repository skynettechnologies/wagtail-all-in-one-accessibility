"""
registration.py
----------------
Registers ALL valid domains from ALLOWED_HOSTS with the add-user-domain API.
Each domain is tracked independently. New domains register on next migrate/restart.
Mirrors the Misago / django-all-in-one-accessibility reference plugin exactly.
"""

import os
import json
import base64
import logging
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

# Default python-requests User-Agent gets throttled (429) by the Skynet API's
# WAF/rate-limiter. Sending a normal, identifiable UA avoids that -- mirrors
# the Django reference plugin's registration.py.
_REQUEST_HEADERS = {
    "User-Agent": "AIOA-Wagtail-Plugin/2.2.0 (+https://ada.skynettechnologies.us)",
    "Accept": "*/*",
}


def _get_flag_file():
    """
    Returns the flag file path.
    Priority:
      1. BASE_DIR/.aioa_registered.json  (project root)
      2. Fallback to package directory
    """
    try:
        from django.conf import settings
        if hasattr(settings, "BASE_DIR"):
            return os.path.join(str(settings.BASE_DIR), ".aioa_registered.json")
    except Exception:
        pass
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".accessibility_api_called.json",
    )


def _is_valid_registration(info):
    """
    A domain is only genuinely registered if the recorded response was an
    actual HTTP 200 -- mirrors the guard in the Django reference plugin's
    registration.py, which never persists a non-200 (or network-error)
    result as "registered" at all.

    Without this guard a domain that hit a 429 (rate limit) or a network
    error got permanently marked api_called: True anyway, which blocked any
    retry forever -- the domain looked "done" even though add-user-domain
    never actually succeeded for it. Treat any entry that isn't a clean 200
    as unregistered so it gets retried and the flag file self-heals instead
    of requiring a manual edit.
    """
    return isinstance(info, dict) and info.get("api_called") is True and info.get("status_code") == 200


def _read_flag():
    """
    Returns dict of already-registered domains: {domain_name: info}.
    Filters out any stale/corrupted entries that aren't a genuine HTTP 200
    registration (see _is_valid_registration) so they're retried instead
    of staying stuck forever.
    """
    flag_file = _get_flag_file()
    raw = {}

    if not os.path.exists(flag_file):
        legacy = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            ".accessibility_api_called.json",
        )
        if os.path.exists(legacy):
            try:
                with open(legacy, "r") as f:
                    data = json.load(f)
                if isinstance(data, dict) and "called" in data and "domains" not in data:
                    # Legacy single-flag format from earlier plugin versions.
                    raw = {}
                else:
                    raw = data.get("domains", {})
            except Exception:
                raw = {}
    else:
        try:
            with open(flag_file, "r") as f:
                data = json.load(f)
            if isinstance(data, dict) and "domain" in data and "domains" not in data:
                raw = {data["domain"]: data}
            else:
                raw = data.get("domains", {})
        except Exception:
            raw = {}

    cleaned = {name: info for name, info in raw.items() if _is_valid_registration(info)}

    dropped = set(raw) - set(cleaned)
    if dropped:
        # Persist the repair immediately so the corrupted/failed entries
        # don't keep coming back on every subsequent read.
        logger.info("[AIOA] Dropping stale/invalid registration entries for retry: %s", sorted(dropped))
        _write_flag(cleaned)

    return cleaned


def _write_flag(domains):
    """Persist the full domains registry."""
    flag_file = _get_flag_file()
    try:
        with open(flag_file, "w") as f:
            json.dump({"domains": domains}, f, indent=2)
    except Exception as exc:
        logger.warning("[AIOA] Could not write registration flag file: %s", exc)


def register_domain(domain_url, domain_name):
    """
    Registers a single domain with the add-user-domain API, the same way the
    django-all-in-one-accessibility reference plugin does it, but scoped to
    one domain instead of looping over ALLOWED_HOSTS.

    This is what actually gets called -- from the context processor, at the
    moment the widget <script> tag is injected into a real front-end page
    request -- so registration reflects the domain a visitor is actually
    hitting rather than a static, potentially stale guess at startup.

    - Already registered (HTTP 200 on file) -> skipped, returns immediately.
    - Success (HTTP 200) -> marked as registered.
    - Failure (429 / other non-200 / network error) -> NOT marked, so it's
      retried automatically the next time the widget script is rendered.
    """
    if not domain_name:
        return

    registered = _read_flag()
    if domain_name in registered:
        return  # Already registered -- nothing to do.

    in_eu = _detect_eu()
    no_required_eu = 0 if in_eu else 1

    try:
        payload = {
            "name": domain_name,
            "email": f"no-reply@{domain_name}",
            "company_name": "",
            "website": base64.b64encode(domain_url.encode()).decode(),
            "package_type": "basic",
            "start_date": datetime.utcnow().isoformat(),
            "end_date": "",
            "price": "",
            "discount_price": "0",
            "platform": "Wagtail",
            "api_key": "",
            "is_trial_period": "",
            "is_free_widget": "1",
            "bill_address": "",
            "country": "",
            "state": "",
            "city": "",
            "post_code": "",
            "transaction_id": "",
            "subscr_id": "",
            "payment_source": "",
            "no_required_eu": no_required_eu,
        }

        response = requests.post(
            "https://ada.skynettechnologies.us/api/add-user-domain",
            data=payload,
            headers=_REQUEST_HEADERS,
            timeout=10,
        )

        if response.status_code == 200:
            # Only mark as registered on real success.
            registered[domain_name] = {
                "api_called": True,
                "registered_at": datetime.utcnow().isoformat(),
                "domain_url": domain_url,
                "no_required_eu": no_required_eu,
                "status_code": response.status_code,
            }
            _write_flag(registered)
            logger.info("[AIOA] Registered: %s (HTTP %s)", domain_name, response.status_code)
        else:
            # Non-200 (e.g. 429) -- don't mark as registered, so the next
            # page render (which triggers this again) retries it instead of
            # being silently stuck forever.
            logger.warning(
                "[AIOA] Registration failed for %s: HTTP %s -- will retry on next page load",
                domain_name, response.status_code,
            )

    except Exception as exc:
        # Network-level failure (timeout, DNS, connection error, etc.)
        # Also NOT marked as registered, so it retries on the next page load.
        logger.warning("[AIOA] Registration failed for %s: %s -- will retry on next page load", domain_name, exc)


def register_domain_on_install():
    """
    Loops over ALL valid domains in ALLOWED_HOSTS and registers any that
    aren't registered yet, via register_domain().

    Not called automatically on app startup any more -- see apps.py.
    Registration is instead triggered per-request from context_processors.py,
    the moment the widget <script> tag is actually injected into a front-end
    page (mirroring where the reference django-all-in-one-accessibility
    plugin's widget script gets served from). This function is kept for
    management-command / manual use, e.g. to pre-register every configured
    host in bulk without waiting for a visitor to hit each one.
    """
    all_domains = _get_all_domains_from_settings()
    for domain_url, domain_name in all_domains:
        register_domain(domain_url, domain_name)


def _detect_eu():
    """Returns True if the server is in an EU country."""
    try:
        resp = requests.get("https://ipapi.co/json/", headers=_REQUEST_HEADERS, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("in_eu", False)
    except Exception:
        pass
    return False


def _get_all_domains_from_settings():
    """
    Returns [(domain_url, domain_name)] for every real host in ALLOWED_HOSTS.
    Skips localhost, 127.0.0.1, wildcards, and duplicates.
    """
    from django.conf import settings

    if hasattr(settings, "AIOA_DOMAIN"):
        raw = settings.AIOA_DOMAIN.rstrip("/")
        if "://" in raw:
            from urllib.parse import urlparse
            p = urlparse(raw)
            return [(f"{p.scheme}://{p.hostname}", p.hostname)]
        return [(f"https://{raw}", raw)]

    skip = {"localhost", "127.0.0.1", "*", ".localhost", "0.0.0.0"}
    seen, result = set(), []
    for host in getattr(settings, "ALLOWED_HOSTS", []):
        clean = host.lstrip(".")
        if clean and clean not in skip and clean not in seen:
            seen.add(clean)
            result.append((f"https://{clean}", clean))
    return result


def get_no_required_eu_default():
    """
    Read the flag file and return the current no_required_eu value to decide
    which CDN (global vs EU) the front-end widget script should load from.
    Defaults to 1 (non-EU / global CDN) when nothing has been registered yet.
    """
    registered = _read_flag()
    if not registered:
        return 1
    first = next(iter(registered.values()), {})
    return first.get("no_required_eu", 1)
