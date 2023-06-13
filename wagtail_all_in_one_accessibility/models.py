from django.db import models
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

aioa_SELECT_CHOICE = [('top_left','Top left'),
      ('top_center','Top Center'),
      ('top_right','Top Right'),
      ('middel_left','Middle left'),
      ('middel_right','Middle Right'),
      ('bottom_left','Bottom left'),
      ('bottom_center','Bottom Center'),
      ('bottom_right','Bottom Right')]
def validate_token(value):
    if value is not None:
        pass
    else:
        raise ValidationError("")
class wagtail_all_in_one_accessibility(models.Model):
    aioa_license_Key = models.CharField(max_length=150,blank=True,validators=[validate_token],default=' ',verbose_name='License Key')
    aioa_color_code = models.CharField(max_length=50,blank=True,default=' ',verbose_name ='Hex color code',help_text='You can cutomize the ADA Widget color. For example: #FF5733')
    aioa_place = models.CharField(max_length=100,blank=True,choices=aioa_SELECT_CHOICE,default=('bottom_right','Bottom Right'),verbose_name='Where would you like to place the accessibility icon on your site')
    
    def __str__(self):
    
        return '{}, {}, {}'.format(self.aioa_place,self.aioa_color_code, self.aioa_license_Key)
    
    class Meta:
        verbose_name = 'All in One Accessibility Settings'
        verbose_name_plural = 'All in One Accessibility Settings'
        
        
    

# for a in wagtail_all_in_one_accessibility.objects.all():
#     print(a)
#     if a.aioa_license_Key == "":
#         aioa_NOTE  = mark_safe("<span class='validate_pro'><p>You are currently using Free version which have limited features. </br>Please <a href='https://www.skynettechnologies.com/add-ons/product/all-in-one-accessibility/'>purchase</a> License Key for additional features on the ADA Widget</p></span>")
#     else:
#         aioa_NOTE = ''    

