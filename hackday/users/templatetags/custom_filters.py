import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def checkbox_first(value):
    new = re.sub(r'(<label[^>]+>.*):(</label>) (<input type="checkbox"[^>]+>)',
            '\\3 \\1', value)
    new = re.sub(r'(<label[^>]+>.*):(</label>) '
            '(<input checked="checked" type="checkbox"[^>]+>)',
            '\\3 \\1', new)
    return mark_safe(new)
