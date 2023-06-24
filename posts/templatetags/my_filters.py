from django import template
from django.utils import timezone
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def custom_date(value):
    now = timezone.now()
    diff = now - value

    if diff.days <= 0 and diff.seconds < 3600:
        return str(diff.seconds//60) + " minutes ago"
    elif diff.days <= 0 and diff.seconds >= 3600:
        return str(diff.seconds//3600) + " hours ago"
    elif diff.days >= 1 and diff.days < 7:
        return str(diff.days) + " days ago"
    else:
        return value.strftime("%B %d, %Y")  # If more than a week ago, return a formatted date

# In your_app/templatetags/your_app_filters.py
from django import template

register = template.Library()

@register.filter
def times(number):
    return range(number)
