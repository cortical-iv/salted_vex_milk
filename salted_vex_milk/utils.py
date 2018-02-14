#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for salted_vex_milk
"""
import logging

import django_tables2 as tables



"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



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
    num_seconds = seconds - (num_minutes*seconds_per_minute)
    return [num_days, num_hours, num_minutes, num_seconds]


def render_seconds(value):
    """Renders time originally recorded in seconds as Xd Mh Ym. Leaves off seconds.
    Usually for events on order of hours or more."""
    time_logged = seconds_to_days(value)
    days = time_logged[0]
    hours = time_logged[1]
    minutes = time_logged[2]
    if value > 0:
        if days > 0:
            time_played = f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            time_played = f"{hours}h {minutes}m"
        else:
            time_played = f"{minutes}m"
    else:
        time_played = '0m'
    return time_played

def render_seconds_to_seconds(value):
    """Renders time originally recorded in seconds as Xd Mh Ym. Leaves in seconds,
    usually for thigns on order of minutes."""
    time_logged = seconds_to_days(value)
    days = time_logged[0]
    hours = time_logged[1]
    minutes = time_logged[2]
    seconds = time_logged[3]
    if value > 0:
        if days > 0:
            time_played = f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            time_played = f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            time_played = f"{minutes}m {seconds}s"
        else:
            time_played = f"{seconds}s"
    else:
        time_played = '0s'
    return time_played



def minutes_to_days(minutes):
    minutes_per_day = 1440
    minutes_per_hour = 60
    logger.debug(f"svm.utils.minutes_to_days minutes: {minutes}")
    logger.debug(f"svm.utils.minutes_to_days minutes type: {type(minutes)}")
    num_days = minutes // minutes_per_day
    minutes = minutes - (num_days*minutes_per_day)
    num_hours = minutes // minutes_per_hour
    num_minutes = minutes - (num_hours*minutes_per_hour)
    return [num_days, num_hours, num_minutes]


def render_minutes(value):
    time_logged = minutes_to_days(value)
    #logger.debug(time_logged)
    days = time_logged[0]
    hours = time_logged[1]
    minutes = time_logged[2]
    time_played = ''
    if value > 0:
        if days > 0:
            time_played += str(days) + 'd '
        if hours > 0:
            time_played += str(hours) + 'h '
        time_played += str(minutes) + 'm'
    else:
        time_played = '0m'
    return time_played