# wagtail_hooks.py
from wagtail import hooks
from django.utils.html import format_html

# Load global JS for conditional field logic
@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html('<script src="/static/js/conditional_fields.js"></script>')

# Load global CSS
@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="/static/css/admin.css">')

# Inject JS into Wagtail editor for auto-filling domain URL
@hooks.register('insert_editor_js')
def fill_domain_url_js():
    return format_html('<script src="/static/js/fill_domain_url.js"></script>')



@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['wagtail_all_in_one_accessibility/accessibility.svg']































