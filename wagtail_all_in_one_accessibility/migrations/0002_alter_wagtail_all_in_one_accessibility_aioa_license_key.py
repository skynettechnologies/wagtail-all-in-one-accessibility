# Generated by Django 4.2.2 on 2023-06-12 12:22

from django.db import migrations, models
import wagtail_all_in_one_accessibility.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_all_in_one_accessibility', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wagtail_all_in_one_accessibility',
            name='aioa_license_Key',
            field=models.CharField(blank=True, default=' ', help_text='aioa_NOTE', max_length=150, validators=[wagtail_all_in_one_accessibility.models.validate_token], verbose_name='License Key'),
        ),
    ]
