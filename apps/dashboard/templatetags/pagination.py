import math

from django import template

register = template.Library()


@register.simple_tag(name="get_pages")
def get_pages(page_obj):
    pagination_to_show = 9
    page_left_limit = math.ceil(pagination_to_show / 2)
    total_pages = page_obj.paginator.num_pages
    page = page_obj.number

    if page < page_left_limit:
        pages = list(range(1, pagination_to_show + 1))[:total_pages]

    elif page > total_pages - (page_left_limit - 1):
        start_page = total_pages - pagination_to_show
        pages = [start_page +
                 x for x in range(1, pagination_to_show + 1)][-total_pages:]

    else:
        start_page = page - page_left_limit
        pages = [start_page + x for x in range(1, pagination_to_show + 1)]

    return pages


@register.simple_tag(name="filtered_pagination")
def filtered_pagination(*args, **kwargs):
    applied_filters = kwargs.get('applied_filters', dict())
    query_string = ''
    if applied_filters:
        for f, v in applied_filters.items():
            if f != 'page':
                for value in applied_filters.getlist(f):
                    query_string += f'{f}={value}&'
    return query_string
