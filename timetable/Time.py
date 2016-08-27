# -*- encoding: utf-8 -*-
#
#

"""
   课程时间日期相关
"""

__author__ = 'Allan Zyne'


from datetime import timedelta, time, date, datetime


class CourseSchedule:
    def __init__(self, school_date, course_time):
        """

        :type school_date: timetable.Time.CourseDate
        :type course_time: timetable.Time.CourseTime
        """
        self.date = school_date
        self.time = course_time

    def date_t_time_format(self, nth_week=1, weekday=1, nth_class=1):
        datetime = self.get_datetime(nth_week, weekday, nth_class)
        return datetime[0].strftime('%Y%m%dT%H%M%S'), datetime[1].strftime('%Y%m%dT%H%M%S')

    def get_datetime(self, nth_week, weekday, nth_class):
        date = self.date.get_date(nth_week, weekday)
        time = self.time.get_time(nth_class)
        return datetime.combine(date, time[0]), datetime.combine(date, time[1])


#
# 设置 开学时间
# 得到第几周的日期
# 第几周到第几周
#
class CourseDate:
    def __init__(self, date):
        self.date = date

    def get_date(self, nth_week = 1, weekday = 1):
        """
        返回从date开始第nth周周weekday的日期

        :type nth_week: int
        :type week: int
        :rtype : datetime.date
        """
        return self.date + timedelta(days=(7*(nth_week - 1) + (weekday - 1)))

#
#
# 设置每节课的开始时间和长度或结束时间
# 课间时间？
#
class CourseTime:
    course_time = []

    def __init__(self, time_list=None):
        if time_list is not None:
            self.insert_time_list(time_list)

    def insert_time_list(self, time_list):
        if len(time_list[0]) == 2:
            for t, d in time_list:
                self.insert_time(t, d)
        else:
            for s, d, e in time_list:
                self.insert_time(s, d, e)

    def insert_time(self, start_time, duration = 0, end_time = None):
        """
        生成一个词典保存一节课的时间段。
        start表示开始时间，duration表示持续时间(分钟)，end表示结束时间。
        如果指定了duration，就忽略end。

        :type start_time: datetime.time
        :type duration: int
        :type end_time: datetime.time
        """
        if end_time is None:
            d = date(1, 1, 1)
            dt = timedelta(minutes = duration)
            end_time = (datetime.combine(d, start_time) + dt).time()

        self.course_time.append({"t_start": start_time, "t_dur": duration, "t_end": end_time })

    def get_time(self, n):
        time = self.course_time[n-1]
        return time["t_start"], time["t_end"], time["t_dur"]

    def get_start_time(self, n):
        return self.course_time[n-1]["t_start"]

    def get_end_time(self, n):
        return self.course_time[n-1]["t_end"]

    def get_duration(self, n):
        return self.course_time[n-1]["t_dur"]