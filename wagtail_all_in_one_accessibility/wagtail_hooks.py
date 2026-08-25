# wagtail_hooks.py
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import capfirst

from wagtail import hooks
from wagtail.admin.menu import MenuItem

# NOTE: these paths are namespaced under the app's own static folder
# (static/wagtail_all_in_one_accessibility/...), matching Django/Wagtail's
# app static-file convention. The previous version referenced bare
# "/static/js/..." and "/static/css/..." paths, which only ever resolved by
# accident (any other installed app shipping a "js" or "css" static folder
# would silently shadow or be shadowed by these files) and would 404 outright
# under STATICFILES_STORAGE backends that hash/namespace files (e.g.
# ManifestStaticFilesStorage). Using `static()` resolves correctly regardless
# of STATIC_URL, storage backend, or CDN configuration.


@hooks.register("insert_global_admin_js")
def global_admin_js():
    # Both scripts are no-ops on pages that don't have their target fields,
    # so it's safe (and necessary) to load them globally.
    #
    # IMPORTANT: fill_domain_url.js used to be registered via
    # `insert_editor_js`, a hook that Wagtail only renders on the *Page*
    # editor template. The All in One Accessibility settings screen is a
    # generic-settings edit view, not a page editor, so that hook never fired
    # there and the hidden `domain_url` field was never populated on the
    # settings form. Registering both scripts here (a hook that
    # `admin_base.html` renders on every admin page) fixes that.
    return format_html(
        '<script src="{}"></script>\n<script src="{}"></script>',
        static("wagtail_all_in_one_accessibility/js/conditional_fields.js"),
        static("wagtail_all_in_one_accessibility/js/fill_domain_url.js"),
    )


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_all_in_one_accessibility/css/admin.css"),
    )


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["wagtail_all_in_one_accessibility/accessibility.svg"]


# ---------------------------------------------------------------------------
# Top-level "All in One Accessibility" menu item
# ---------------------------------------------------------------------------
#
# `@register_setting` on AllInOneAccessibility (see models.py) is what wires
# up the singleton settings row -- `.load()`, permissions, the admin
# URL-finder, and the edit view at `wagtailsettings:edit`. That's all still
# needed. What it does NOT let you configure is *where* the menu entry it
# creates lives: `wagtail.contrib.settings.registry.Registry.register()`
# unconditionally registers into the `register_settings_menu_item` hook, so
# the entry always nests under Settings with no opt-out.
#
# To surface it as its own top-level sidebar item instead (matching how
# sibling plugins like the accessibility scanner appear), we add a second
# menu item under `register_admin_menu_item` pointing at the exact same edit
# URL, then use `construct_settings_menu` to drop the original entry back out
# of the Settings submenu -- otherwise it would show up in both places.


def _aioa_edit_url():
    return reverse(
        "wagtailsettings:edit",
        args=["wagtail_all_in_one_accessibility", "allinoneaccessibility"],
    )


class AllInOneAccessibilityMenuItem(MenuItem):
    def is_shown(self, request):
        from .models import AllInOneAccessibility

        permission_policy = AllInOneAccessibility.get_permission_policy()
        return permission_policy.user_has_permission(request.user, "change")


@hooks.register("register_admin_menu_item")
def register_aioa_admin_menu_item():
    from .models import AllInOneAccessibility

    return AllInOneAccessibilityMenuItem(
        capfirst(AllInOneAccessibility._meta.verbose_name),
        _aioa_edit_url(),
        name="all-in-one-accessibility",
        icon_name="accessibility",
        order=9001,  # just after core items (Pages/Images/Documents/Reports), before Settings (10000)
    )


@hooks.register("construct_settings_menu")
def hide_aioa_from_settings_menu(request, menu_items):
    # Registered by `@register_setting` in models.py. Removed here so it
    # only appears via the top-level menu item above, not in both places.
    menu_items[:] = [item for item in menu_items if item.name != "all-in-one-accessibility"]
