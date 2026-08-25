import logging

from django.apps import AppConfig
from django.db.models.signals import post_migrate

logger = logging.getLogger(__name__)

# Canonical defaults (single source of truth), mirrors the model field defaults.
AIOA_DEFAULTS = {
    "aioa_color_code": "420083",
    "enable_widget_icon_position": False,
    "to_the_right_px": 20,
    "to_the_right": "to_the_left",
    "to_the_bottom_px": 20,
    "to_the_bottom": "to_the_bottom",
    "aioa_place": "bottom_right",
    "aioa_size": "oversize",
    "aioa_icon_type": "aioa-icon-type-1",
    "enable_icon_custom_size": False,
    "aioa_size_value": 50,
    "aioa_icon_size": "aioa-default-icon",
}


class WagtailAllInOneAccessibilityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wagtail_all_in_one_accessibility"
    verbose_name = "All in One Accessibility"

    def ready(self):
        # Make sure a settings row always exists once migrations have run.
        post_migrate.connect(_ensure_default_settings, sender=self)
        # NOTE: domain registration (add-user-domain) is intentionally NOT
        # triggered here at process startup any more. It's now triggered
        # from context_processors.admin_AIOA(), the moment the widget
        # <script> tag is actually injected into a front-end page request --
        # i.e. registration reflects real visitor traffic to a real domain,
        # rather than firing (and re-firing on every autoreload/restart) at
        # app startup. See registration.register_domain().


def _ensure_default_settings(sender, **kwargs):
    """
    Runs after every `manage.py migrate`.

    BaseGenericSetting already creates a row on first access (see
    `AllInOneAccessibility.load()`), but this is a safety net for the case
    where the row was deleted manually after being created. It never
    overwrites values an admin has already saved.
    """
    try:
        from .models import AllInOneAccessibility
        if not AllInOneAccessibility.objects.exists():
            AllInOneAccessibility.objects.create(**AIOA_DEFAULTS)
            logger.info("[AIOA] Default settings row created by post_migrate signal.")
    except Exception as exc:
        logger.warning("[AIOA] Could not ensure default settings: %s", exc)
