# panels.py
from wagtail.admin.panels import FieldPanel

class ImageChoicePanel(FieldPanel):
    widget = None

    def __init__(self, field_name, widget, *args, **kwargs):
        super().__init__(field_name, *args, **kwargs)
        self.widget = widget

    def get_form_options(self):
        opts = super().get_form_options()
        opts['widgets'] = {self.field_name: self.widget}
        return opts
