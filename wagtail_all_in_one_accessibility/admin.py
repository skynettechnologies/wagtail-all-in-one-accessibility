from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.helpers import ButtonHelper
from .models import AllInOneAccessibility

class WagtailHomePageCarouselButtonHelper(ButtonHelper):
    def add_button(self,request, classnames_add=None, classnames_exclude=None):
        
        retVal = super().add_button(request)
        # set add permission to False, if object already exists
        if retVal and AllInOneAccessibility.objects.exists():
            retVal = False
        return None
    

class AccessibilityModelAdmin(ModelAdmin):
    
    model = AllInOneAccessibility
    menu_label = "All In One Accessibility"
    add_to_settings_menu = False 
    exclude_from_explorer = False 
    button_helper_class = WagtailHomePageCarouselButtonHelper

modeladmin_register(AccessibilityModelAdmin)








