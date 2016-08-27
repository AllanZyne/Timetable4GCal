#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
#

"""
   课程
"""

__author__ = 'Allan Zyne'

# TODO: Change CourseSchedule dynamically
# TODO: Load/Save the calendar event id
# TODO: Load/Save the calendar in excel
# TODO: More easily change course_pattern

# TODO: Add a gui ??


import os
from timetable import Time
from timetable.GCal import TimeTableCalendar
from timetable import Jwweb
from timetable.Parser import CourseParser
from collections import OrderedDict
from Config import *
import getpass


class TimeTable:
    """

    """
    course_entry_list = []
    course_schedule = None
    title = None

    def __init__(self, title, course_entry_list, course_schedule):
        """

        :type title: str
        :type course_entry_list: [timetable.data.CourseEntry]
        :type course_schedule:  []
        :return:
        """
        self.title = title
        self.course_entry_list = course_entry_list
        self.course_schedule = course_schedule


def get_data(time_value, class_value):
    """ 从本地或者网上获取课程表数据

    :type time_value: int
    :type class_value: int
    :rtype: str
    """
    # 检查本地是否已存在
    page_fn = "cache" + os.sep + "%s-%s.html" % (time_value, class_value)
    page = None

    if os.path.exists(page_fn):
        print "local exists %s." % page_fn
        tt_file = open(page_fn, 'r')
        page = tt_file.read()
    else:
        print "get %s from internet" % page_fn
        page = Jwweb.get_timetable_html(time_value, class_value)
        tt_file = open(page_fn, 'w')
        tt_file.write(page)
        tt_file.close()

    return page


if __name__ == "__main__":

    class_name = u'11软工（卓越）'

    # 得到课程表数据
    class_value = Jwweb.get_class_value(class_name)
    time_value = Jwweb.get_time_value(school_year, semester)

    page = get_data(time_value, class_value)

    # 分解课程表数据
    parser = CourseParser(OrderedDict(content_pattern), unicode(page, 'gbk'))
    course_list = parser.start()

    # 设置时间、日期
    school_date = Time.CourseDate(datetime.date(year=2014, month=2, day=17))
    course_time = Time.CourseTime(lesson_time)

    course_datetime = Time.CourseSchedule(school_date, course_time)

    # 组成课程表
    table = TimeTable(class_name, course_list, course_datetime)

    print "Timetable\n"

    user = raw_input('Google account: ')
    pw = getpass.getpass('password: ')

    cal = TimeTableCalendar(user, pw, table)
    cal.run(False)

