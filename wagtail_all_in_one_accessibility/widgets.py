# widgets.py
from django.forms.widgets import RadioSelect
from django.utils.html import format_html

SIZE_MAP = {
    'aioa-big-icon': 75,
    'aioa-medium-icon': 65,
    'aioa-default-icon': 55,
    'aioa-small-icon': 45,
    'aioa-extra-small-icon': 35,
}

class ImageRadioSelect(RadioSelect):

    template_name = 'widgets/icon_type_radio.html'

class DependentImageRadioSelect(RadioSelect):
    template_name = 'widgets/dependent_radio.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['size_map'] = SIZE_MAP
        return context

