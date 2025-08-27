# wagtail_hooks.py
from wagtail import hooks
from django.utils.html import format_html

@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html('<script src="/static/js/conditional_fields.js"></script>')


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="/static/css/admin.css">')


@hooks.register('insert_editor_js')
def fill_domain_url_js():
    return format_html('<script src="/static/js/fill_domain_url.js"></script>')





    


    

































