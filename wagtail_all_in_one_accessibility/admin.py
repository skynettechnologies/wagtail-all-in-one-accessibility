from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register 
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from django.contrib import admin
from .models import wagtail_all_in_one_accessibility

class WagtailHomePageCarouselButtonHelper(ButtonHelper):
    def add_button(self,request, classnames_add=None, classnames_exclude=None):
        
        retVal = super().add_button(request)
        # set add permission to False, if object already exists
        if retVal and wagtail_all_in_one_accessibility.objects.exists():
            retVal = False
        return None


class ExampleModelAdmin(ModelAdmin):
    
    model = wagtail_all_in_one_accessibility
    list_display = ('aioa_license_Key', 'aioa_color_code', 'aioa_place')
    list_display_links  = ('aioa_license_Key', 'aioa_color_code', 'aioa_place')
    add_to_settings_menu = False 
    exclude_from_explorer = False 
    button_helper_class = WagtailHomePageCarouselButtonHelper

modeladmin_register(ExampleModelAdmin)

