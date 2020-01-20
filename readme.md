
# django_easy_tags

django_easy_tags is a simple django app which extends [django-tagging](https://django-tagging.readthedocs.io/en/develop/) package and makes tagging configuration extremely easy. By adding a single line in your settings file you have all most used tagging functionalities in place.

## Quick start


1. Add "easy_tags" to your INSTALLED_APPS setting like this:
    ```
    INSTALLED_APPS = [
        ...
        'easy_tags',
    ]
    ```
0. Include the easy_tags URLconf in your project urls.py like this::
    ```
    path('', include('easy_tags.urls')),
    ```
0. Run `python manage.py migrate` to create django-tagging models.

0. Add model you would like to tag in your settings file::
    ```
    EASY_TAGS = [
        {
            'MODEL': 'books.models.Book',
        }
    ]
    ```

## Basic usage

1. Get all tags for a model `book`:
    ```
   /tags/book/
    ```
1. Get all tags for given `book`:
    ```
   /tags/book/1/
    ```
1. Assign tags to a `book`:
    ```
   /tags/book/1/
   ["adventure", "s-f"]
    ```
1. Search tags for given `book`:
    ```
   /tags/book/1/?tag=adventure
    ```
1. Get objects with given tags assigned
    ```
   /book/?tag=adventure
    ```
