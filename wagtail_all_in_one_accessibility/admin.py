import os
import json
import threading
import base64
from datetime import datetime
from urllib.parse import urlparse
import requests
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.helpers import ButtonHelper
from .models import AllInOneAccessibility

# Custom button helper to restrict "Add" if object already exists
class WagtailHomePageCarouselButtonHelper(ButtonHelper):
    def add_button(self, request, classnames_add=None, classnames_exclude=None):
        retVal = super().add_button(request)
        # set add permission to False, if object already exists
        if retVal and AllInOneAccessibility.objects.exists():
            retVal = False
        return retVal  # fix: return retVal, not None to keep default behavior when allowed

# Function to call external APIs once per server instance (uses file flag)
FLAG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".accessibility_api_called.json")

def call_accessibility_apis_once(request):
    if os.path.exists(FLAG_FILE):
        return

    try:
        headers = {}
        response = requests.get("https://ipapi.co/json/", headers=headers, timeout=5)
        in_eu = False
        if response.status_code == 200:
            in_eu = response.json().get("in_eu", False)

        full_url = request.build_absolute_uri('/').rstrip('/')
        parsed = urlparse(full_url)
        domain_url = f"{parsed.scheme}://{parsed.hostname}"
        domain_name = parsed.hostname

        payload = {
            "name": domain_name,
            "email": f"no-reply@{domain_name}",
            "company_name": "",
            "website": base64.b64encode(domain_url.encode()).decode(),
            "package_type": "free-widget",
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
            "no_required_eu": 1 if not in_eu else 0
        }
    
        register_resp = requests.post("https://ada.skynettechnologies.us/api/add-user-domain", data=payload, headers=headers)
      
        with open(FLAG_FILE, "w") as f:
            json.dump({
                "called": True,
                "no_required_eu": 1 if not in_eu else 0
            }, f)

    except Exception as e:
        error_content = str(e)
      

# Register model in Wagtail admin with custom button helper
class AccessibilityModelAdmin(ModelAdmin):
    
    model = AllInOneAccessibility
    menu_label = "All in One Accessibility"
    add_to_settings_menu = False
    menu_icon = "accessibility"
    exclude_from_explorer = False 
    button_helper_class = WagtailHomePageCarouselButtonHelper
   
# Patch the index_view to run your API call once on menu click
original_index_view = AccessibilityModelAdmin.index_view

def patched_index_view(self, request, *args, **kwargs):
    threading.Thread(target=call_accessibility_apis_once, args=(request,), daemon=True).start()
    return original_index_view(self, request, *args, **kwargs)

AccessibilityModelAdmin.index_view = patched_index_view

# Register the model admin
modeladmin_register(AccessibilityModelAdmin)






