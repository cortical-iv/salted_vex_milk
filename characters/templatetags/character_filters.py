#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom template filter(s) for use in character template.
"""

from django import template
from salted_vex_milk.utils import render_minutes

register = template.Library()

@register.filter('minute_format')
def minute_format(value):
    minute_string = render_minutes(value)
    return minute_string