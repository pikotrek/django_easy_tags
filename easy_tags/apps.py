from django.apps import AppConfig
from django.conf import settings
from django.db import ProgrammingError
from django.utils.module_loading import import_string

from easy_tags import conf as easy_tags_settings


def get_setting(setting):
    val = setting
    if isinstance(val, str):
        val = [import_string(val)]
    elif isinstance(val, (list, tuple)):
        val = [import_string(v) if type(v) is str else v for v in val]
    elif val is not None:
        val = [val]
    else:
        val = []
    return val


class EasyTagConfig(AppConfig):
    name = 'easy_tags'
    label = 'easy_tags'

    configured = False

    def ready(self):
        if EasyTagConfig.configured:
            return

        from django.contrib.contenttypes.models import ContentType
        from tagging.registry import register

        app_settings = {}

        for model_setting in getattr(settings, 'EASY_TAGS', {}):
            if 'MODEL' in model_setting:
                app_settings[import_string(model_setting['MODEL'])] = {
                    'label': model_setting.get('LABEL'),
                    'permissions': model_setting.get('PERMISSIONS'),
                    'filters': model_setting.get('FILTERS')
                }

        content_types = {}
        try:
            for model, content_type in ContentType.objects.get_for_models(*app_settings.keys()).items():
                label = app_settings[model]['label']
                if not label:
                    label = content_type.model
                content_types[label] = {
                    'content_type': content_type,
                    'permissions': get_setting(app_settings[model]['permissions']),
                    'filters': get_setting(app_settings[model]['filters'])
                }
                register(model)
            easy_tags_settings.EASY_TAGS_CONFIG = content_types

            EasyTagConfig.configured = True
        except ProgrammingError:
            pass
