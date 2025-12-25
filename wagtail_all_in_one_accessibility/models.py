# models.py
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from .panels import ImageChoicePanel
from .widgets import ImageRadioSelect
from .widgets import DependentImageRadioSelect
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
import requests
from urllib.parse import urlparse

AIOA_SELECT_CHOICES = [
    ('top_left', 'Top Left'),
    ('top_center', 'Top Center'),
    ('top_right', 'Top Right'),
    ('middle_left', 'Middle Left'),
    ('middle_right', 'Middle Right'),
    ('bottom_left', 'Bottom Left'),
    ('bottom_center', 'Bottom Center'),
    ('bottom_right', 'Bottom Right'),
]

AIOA_SIZE_CHOICES = [
    ('regular', 'Regular Size'),
    ('oversize', 'Oversize'),
]


to_the_right_choice = [('to_the_left','To the left'),
      ('to_the_right','To the right'),
    ]

to_the_bottom_choice = [('to_the_bottom','To the bottom'),
      ('to_the_top','To the top'),
    ]

AIOA_ICON_SIZE_CHOICES = [
    ('aioa-big-icon', ''),
    ('aioa-medium-icon', ''),
    ('aioa-default-icon', ''),
    ('aioa-small-icon', ''),
    ('aioa-extra-small-icon', ''),
]

ICON_CHOICES = [
    (f'aioa-icon-type-{i}', f'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-{i}.svg')
    for i in range(1, 30)
]

@register_setting(icon='cog')
class AllInOneAccessibility(BaseGenericSetting):
    
    domain_url = models.URLField(
        blank=True,
        editable=True,
        verbose_name="Domain URL (auto-filled)",
        help_text="Auto-filled from browser when saving settings."
    )

    aioa_color_code = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name='Hex Color Code',
        help_text='You can customize the ADA Widget color. For example: #FF5733'
    )

    enable_widget_icon_position = models.BooleanField(
        default=False,
        verbose_name="Enable Precise accessibility widget icon position"
    )
    
    to_the_right_px = models.PositiveSmallIntegerField(
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        verbose_name="Right offset (PX)",
    )

    to_the_right = models.CharField(
        max_length=50,
        default='to_the_left',choices=to_the_right_choice,
        verbose_name="To the left"
    )

    to_the_bottom_px = models.PositiveSmallIntegerField(
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        verbose_name="Bottom offset (PX)",
        
    )

    to_the_bottom = models.CharField(
        max_length=50,
        default='to_the_bottom',choices=to_the_bottom_choice,
        verbose_name="To the bottom"
    )
    
    aioa_place = models.CharField(
        max_length=100,
        choices=AIOA_SELECT_CHOICES,
        default='bottom_right',
        verbose_name='Where would you like to place the accessibility icon on your site'
    )
    
    aioa_size = models.CharField(
        max_length=20,
        choices=AIOA_SIZE_CHOICES,
        default='oversize',
        verbose_name='Select Widget Size'
    )

    aioa_icon_type = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        default='aioa-icon-type-1',
        verbose_name='Select icon type'
    )

    enable_icon_custom_size = models.BooleanField(
        default=False,
        verbose_name="Enable Icon Custom Size"
    )

    aioa_size_value = models.PositiveSmallIntegerField(
        default=50,
        validators=[MinValueValidator(20), MaxValueValidator(150)],
        verbose_name="Select exact icon size (PX)",
        help_text="20 - 150px are permitted values"
    )

    
    aioa_icon_size = models.CharField(
        max_length=50,
        choices=AIOA_ICON_SIZE_CHOICES,
        default='aioa-default-icon',
        verbose_name='Select icon size for Desktop',
        help_text='This size preview will change according to the selected icon type.'
    )
  
    
    panels = [
        FieldPanel('domain_url', classname="hidden"),

        FieldPanel('aioa_color_code'),
        FieldPanel('enable_widget_icon_position', classname='field-enable-widget-icon'),
        FieldRowPanel([
            FieldPanel('to_the_right_px', classname='field-to-the-right-px'),
            FieldPanel('to_the_right', classname='field-to-the-right'),
        ], classname='field-right-row',help_text="0 - 250px are permitted values"),

        FieldRowPanel([
            FieldPanel('to_the_bottom_px', classname='field-to-the-bottom-px'),
            FieldPanel('to_the_bottom', classname='field-to-the-bottom'),
        ], classname='field-bottom-row',help_text="0 - 250px are permitted values"),
       
        FieldPanel('aioa_place', classname='field-aioa-place'),
        FieldPanel('aioa_size', classname='field-aioa-size'),
        ImageChoicePanel('aioa_icon_type', widget=ImageRadioSelect),
       
        FieldPanel('enable_icon_custom_size', classname='field-enable-icon-size'),
        FieldPanel('aioa_size_value', classname='field-aioa-size-value'),
        ImageChoicePanel('aioa_icon_size', widget=DependentImageRadioSelect, classname='field-aioa-icon-size'),

    ]

    # Save hook to trigger external API on save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.domain_url:
            self.send_to_external_api(self.domain_url)

    # Placeholder function for sending data to external API
    def send_to_external_api(self, domain_url=None):

        if not domain_url:
            domain_url = self.domain_url  # fallback from the model
        parsed_url = urlparse(domain_url)
        domain_url = f"{parsed_url.scheme}://{parsed_url.hostname}"

        data = {
            "u":domain_url,
            "widget_color_code": self.aioa_color_code,
            "is_widget_custom_position": int(self.enable_widget_icon_position),
            "is_widget_custom_size": int(self.enable_icon_custom_size),
        }

        if not self.enable_widget_icon_position:
            data.update({
                "widget_position_top": None,
                "widget_position_right": None,
                "widget_position_bottom": None,
                "widget_position_left": None,
                "widget_position": self.aioa_place,
            })
        else:
            widget_position = {
                "widget_position_top": None,
                "widget_position_right": None,
                "widget_position_bottom": None,
                "widget_position_left": None,
            }

            if self.to_the_right == "to_the_left":
                widget_position["widget_position_left"] = self.to_the_right_px
            elif self.to_the_right == "to_the_right":
                widget_position["widget_position_right"] = self.to_the_right_px

            if self.to_the_bottom == "to_the_bottom":
                widget_position["widget_position_bottom"] = self.to_the_bottom_px
            elif self.to_the_bottom == "to_the_top":
                widget_position["widget_position_top"] = self.to_the_bottom_px

            data.update(widget_position)
            data["widget_position"] = ""

        if not self.enable_icon_custom_size:
            data.update({
                "widget_icon_size": self.aioa_icon_size,
                "widget_icon_size_custom": 0,
            })
        else:
            data.update({
                "widget_icon_size": "",
                "widget_icon_size_custom": self.aioa_size_value,
            })

        widget_size_value = 1 if self.aioa_size == "oversize" else 0
        data.update({
            "widget_size": widget_size_value,
            "widget_icon_type": self.aioa_icon_type,
        })
        
        # Send API request to external service (with fallback error handling)
        try:
            response = requests.post('https://ada.skynettechnologies.us/api/widget-setting-update-platform', json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Settings sync failed: {e}") from e

        
    def __str__(self):
        return "All in One Accessibility"
    
    class Meta:
        verbose_name = "All in One Accessibility"
        verbose_name_plural = "All in One Accessibility"
    

        


