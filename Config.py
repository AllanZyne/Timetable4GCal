#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
#

"""
   课程和时间
"""

__author__ = 'Allan Zyne'


import datetime


class_name = u'11软工（卓越）'

school_year = 2013
semester = 1        # 0：上学期；1：下学期

#
content_pattern = [
    (u"课程",     ur"([\w]+)"),
    (u"教师",     ur"(\w+)"),
    (u"职称",     ur"(\(\w+\))"),
    (u"重复",     ur"(\[[\d\-, ]+\w?周\])"),
    (u"节期",     ur"(\[[\d\-]+节\])"),
    (u"地点",     ur"(\d+[\w\d\(\)]+)")
]

# content_pattern = [
#     (u"课程",     ur"([\w ]+)"),
#     (u"性质",     ur"(\(\w+\))"),
#     (u"考察方式", ur"(\[\w*\])"),
#     (u"学分",     ur"([\w：\d\.]+)"),
#     (u"总学时",   ur"([\w：\d\.]+)"),
#     (u"安排学时", ur"([\w：\d\.]+)"),
#     (u"教师",     ur"(\w+)"),
#     (u"职称",     ur"(\(\w+\))"),
#     (u"重复",     ur"(\[[\d\-, ]+\w?周\])"),
#     (u"节期",     ur"(\[[\d\-]+节\])"),
#     (u"本部",     ur"(\(本部\))"),
#     (u"地点",     ur"(\d+[\w\d\(\)]+)")
# ]

#
lesson_time = [
    (datetime.time(8, 0), 100),
    (datetime.time(10, 20), 100),
    (datetime.time(14, 0), 100),
    (datetime.time(16, 20), 100),
    (datetime.time(19, 0), 100)
]
