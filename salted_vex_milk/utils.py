#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for salted_vex_milk
"""
import django_tables2 as tables

class FloatColumn(tables.Column):
    """Custom column for displaying floats to two decimal places"""
    def render(self, value):
        return '{:0.2f}'.format(value)


def seconds_to_days(seconds):
    seconds_per_day = 86400
    seconds_per_hour = 3600
    seconds_per_minute = 60
    num_days = seconds // seconds_per_day
    seconds = seconds - (num_days*seconds_per_day)
    num_hours = seconds // seconds_per_hour
    seconds = seconds - (num_hours*seconds_per_hour)
    num_minutes = seconds // seconds_per_minute
    return [num_days, num_hours, num_minutes]


def minutes_to_days(minutes):
    minutes_per_day = 1440
    minutes_per_hour = 60
    num_days = minutes // minutes_per_day
    minutes = minutes - (num_days*minutes_per_day)
    num_hours = minutes // minutes_per_hour
    num_minutes = minutes - (num_hours*minutes_per_hour)
    return (num_days, num_hours, num_minutes)
