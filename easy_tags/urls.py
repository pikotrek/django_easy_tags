from django.urls import path

from easy_tags import settings
from easy_tags.views import TaggingView, AllTagsView

urlpatterns = []

for label, config in settings.EASY_TAGS_CONFIG.items():
    urlpatterns.append(
        path(
            f'tags/{label}/<int:pk>/',
            TaggingView.as_view(
                {
                    'get': 'list',
                    'post': 'create'
                },
                config=config
            ),
            name=f'{label}_tags'
        )
    )
    urlpatterns.append(
        path(
            f'tags/{label}/',
            AllTagsView.as_view(
                {
                    'get': 'list'
                },
                config=config
            ),
            name=f'{label}_all_tags'
        )
    )
