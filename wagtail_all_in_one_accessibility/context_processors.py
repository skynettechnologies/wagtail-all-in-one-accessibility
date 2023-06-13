import json
import random
from django.conf import settings
from .models import wagtail_all_in_one_accessibility
from django.utils.safestring import mark_safe


def admin_AIOA(request):
    aioa_NOTE = ''
    aioa_BaseScript = ''
    for a in wagtail_all_in_one_accessibility.objects.all():
        aioa_BaseScript = 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode='+ a.aioa_color_code + '&token=' + a.aioa_license_Key+'&t='+str(random.randint(0,999999))+'&position=' + a.aioa_place
        
        if a.aioa_license_Key == "":
            wagtail_all_in_one_accessibility._meta.get_field('aioa_license_Key').help_text = mark_safe("<span class='validate_pro'><p>You are currently using Free version which have limited features. </br>Please <a href='https://www.skynettechnologies.com/add-ons/product/all-in-one-accessibility/'>purchase</a> License Key for additional features on the ADA Widget</p></span>")
        else:
            wagtail_all_in_one_accessibility._meta.get_field('aioa_license_Key').help_text = ""
    return {'AIOA_URL': aioa_BaseScript}

