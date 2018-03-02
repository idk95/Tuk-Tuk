#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 2015-2016 Programacao 1 (LTI)
# 46593 Patrícia Jesus



def hourToInt(time):
    """
    Return the hours with int type.

    Requires: a string with the time in the format hh:mm
    Ensures: an integer with the hour of the time 
    """
    t = time.split(":")
    return int(t[0])



def minutesToInt(time):
    """
    Returns the minutes with int type.

    Requires: a string with the time in the format hh:mm
    Ensures: an integer with the hour of the time 
    """
    t = time.split(":")
    return int(t[1])


def intToTime(hour, minutes):
    """
    Returns time with str type.

    Requires: two arguments with int type, the first
    argument is the hour and the second minute
    Ensures: a string with the time 
    """
    h = str(hour)
    m = str(minutes)

    if hour < 10:
        h = "0" + h

    if minutes < 10:
        m = "0" + m

    return h + ":" + m



def add(time1, time2):
    """
    Returns time with str type.

    Requires: two arguments with str type and
    the time in the format hh:mm.
    Ensures: the sum of the two arguments.
    """
    t1Hour = hourToInt(time1)
    t1Minutes = minutesToInt(time1)
    t2Hour = hourToInt(time2)
    t2Minutes = minutesToInt(time2)

    hours = (t1Minutes + t2Minutes) / 60
    minutes = (t1Minutes + t2Minutes) % 60

    t1H = t1Hour + t2Hour + hours
    t1M = minutes

    return intToTime(t1H, t1M)



def diff(time1, time2):
    """
    Returns time with str type.

    Requires: two arguments with str type and
    the time in the format hh:mm.
    Ensures: the difference of the two arguments.
    """
    t1Hour = hourToInt(time1)
    t1Minutes = minutesToInt(time1)
    t2Hour = hourToInt(time2)
    t2Minutes = minutesToInt(time2)

    t1H = t1Hour - t2Hour
    minutes = t1Minutes - t2Minutes
    t1M = abs(minutes)

    if minutes < 0:
        t1H = t1H - 1
        t1M = 60 - t1M
        
    if t1H < 0:
        t1H = 0
        t1M = 0

    return intToTime(t1H, t1M)

def HoursMinInt(time):
    '''
    Turns a string with time into integer in minutes
    Requires: A string time hh:mm
    Ensures: The time in minutes with integer type
    '''
    hours = hourToInt(time) * 60
    minutes = minutesToInt(time) + hours
    return minutes

def MinIntHourString(minutes):
    '''
    Turns minutes with integer type into a string with time in format hh:mm
    Requires: A integer with minutes
    Ensures: The time in string with format hh:mm
    '''
    hours = str(minutes/60)
    minutes = str(minutes%60)
    if len(hours) == 1:
        hours = '0' + hours
    if len(minutes) == 1:
        minutes = '0' + minutes
    time = hours+':'+minutes
    return time
