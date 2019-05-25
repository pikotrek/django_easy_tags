
django-easy-tags
-

django-easy-tags is a simple django app which extends [django-tagging](https://django-tagging.readthedocs.io/en/develop/) package and makes tagging configuration extremely easy. By adding a single line in your settings file you have all most used tagging functionalities in place.

Quick start
-

1. Add "easy_tags" to your INSTALLED_APPS setting like this:
    ```
    INSTALLED_APPS = [
        ...
        'easy_tags',
    ]
    ```
2. Include the easy_tags URLconf in your project urls.py like this::
    ```
    path('', include('easy_tags.urls')),
    ```
3. Run `python manage.py migrate` to create django-tagging models.

4. Add model you would like to tag in your settings file::
    ```
    EASY_TAGS = [
        {
            'MODEL': 'books.models.Book',
        }
    ]
    ```
