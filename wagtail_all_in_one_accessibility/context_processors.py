# context_processors.py
"""
Injects the AIOA widget context into every template.

Provides:
  - AIOA_URL      : complete widget script URL with all settings as query params
  - aioa_settings : the AllInOneAccessibility settings instance (or None)

Usage in your base template (before </body>):
    <script id="aioa-adawidget" src="{{ AIOA_URL }}"></script>

IMPORTANT: Write the <script> tag directly in your template and place
{{ AIOA_URL }} only in the src="..." attribute. Do NOT pre-build a full
<script> tag as a context variable -- Django's template engine escapes HTML
in variables, which would render the tag as visible text instead of
executing it.

Domain registration (add-user-domain) also happens from here -- see
_register_current_domain() below -- because this is the point where the
widget <script> tag is actually injected into a front-end page. That means
registration reflects a domain real visitors are hitting, fired the first
time that domain's front-end page is rendered, rather than being tied to
app startup/reload or an admin "Save" click.
"""

import threading

from .registration import get_no_required_eu_default, register_domain, _read_flag


def _register_current_domain(request):
    """
    Fires add-user-domain for the current request's host the first time the
    widget script is injected for that domain, then never again (the flag
    file makes this a no-op on every subsequent request/page load once a
    domain is registered). Runs in a background thread so registering never
    adds latency to the page that's rendering the widget.
    """
    try:
        host = request.get_host().split(":")[0]
    except Exception:
        return

    skip = {"localhost", "127.0.0.1", "0.0.0.0"}
    if not host or host in skip:
        return

    # Cheap check on the calling thread first, so we don't spin up a thread
    # (or touch the network) for the common case of an already-registered
    # domain -- which is nearly every request once a site is up and running.
    if host in _read_flag():
        return

    domain_url = f"{request.scheme}://{host}"
    threading.Thread(
        target=register_domain,
        args=(domain_url, host),
        daemon=True,
    ).start()


def admin_AIOA(request):
    _register_current_domain(request)

    eu_base = "https://eu.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js"
    global_base = "https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js"

    # 1. Determine EU vs global CDN from the one-time domain registration.
    no_required_eu = get_no_required_eu_default()
    base_url = eu_base if no_required_eu == 0 else global_base

    # 2. Load widget settings.
    aioa_settings = None
    try:
        from .models import AllInOneAccessibility
        aioa_settings = AllInOneAccessibility.load(request)
    except Exception:
        aioa_settings = None

    # 3. Build the complete widget URL with all params.
    #
    # Expected format (exactly what the widget JS expects):
    #   ?colorcode=#852369&token=&position=bottom_right&size=oversize
    #    &icontype=aioa-icon-type-15&iconsize=aioa-default-icon
    # or, with precise positioning enabled:
    #   ?colorcode=#852369&token=&left=8&top=60&size=oversize
    #    &icontype=aioa-icon-type-15&iconsize=25
    #
    # Rules:
    #   - colorcode uses a literal # (NOT %23) -- the widget JS reads it as-is
    #   - token is always present, empty string if not set
    #   - position: &position=bottom_right  OR  &left=N/&right=N + &top=N/&bottom=N (precise mode)
    #   - iconsize: CSS class name (standard) OR px number (custom size enabled)
    if aioa_settings:
        color = (aioa_settings.aioa_color_code or "420083").lstrip("#")
        token = getattr(aioa_settings, "aioa_token", "") or ""

        params = f"colorcode=#{color}&token={token}"

        # Position: this is the part that previously never reached the
        # front-end widget, so "custom position" had no visible effect.
        if aioa_settings.enable_widget_icon_position:
            if aioa_settings.to_the_right == "to_the_left":
                params += f"&left={aioa_settings.to_the_right_px}"
            else:
                params += f"&right={aioa_settings.to_the_right_px}"

            if aioa_settings.to_the_bottom == "to_the_top":
                params += f"&top={aioa_settings.to_the_bottom_px}"
            else:
                params += f"&bottom={aioa_settings.to_the_bottom_px}"
        else:
            params += f"&position={aioa_settings.aioa_place}"

        # Size
        params += f"&size={aioa_settings.aioa_size}"

        # Icon type
        params += f"&icontype={aioa_settings.aioa_icon_type}"

        # Icon size -- px number (custom) or CSS class name (standard)
        if aioa_settings.enable_icon_custom_size:
            params += f"&iconsize={aioa_settings.aioa_size_value}"
        else:
            params += f"&iconsize={aioa_settings.aioa_icon_size}"

        aioa_url = f"{base_url}?{params}"
    else:
        # No settings row yet -- widget loads with default purple.
        aioa_url = f"{base_url}?colorcode=#420083&token="

    return {
        "AIOA_URL": aioa_url,
        "aioa_settings": aioa_settings,
    }
