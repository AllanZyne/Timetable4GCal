# -*- encoding: utf-8 -*-
#
#

"""
   定义所要用到的数据结构
"""

__author__ = 'Allan Zyne'

import re
import logging

logging.basicConfig(level=logging.ERROR, format='%(levelname)s %(message)s')
logger = logging.getLogger(__name__)


class SchoolLocation:
    location = None      # 地点
    building_no = None
    class_no = None

    def __init__(self, location, building_no=None, class_no=None):
        """

        :type location: str
        :type building_no: int
        :type class_no: int
        """
        self.location = location
        self.building_no = building_no
        self.class_no = class_no


class CourseTime:
    weekday = None  # 星期
    lesson = None   # 节课

    def __init__(self, weekday, lesson):
        """ weekday[1..7], lesson[1..]

        :type weekday: int
        :type lesson: int
        """
        if 1 <= weekday <= 7:
            self.weekday = weekday
        else:
            logger.error("weekday %d", weekday)

        if lesson >= 1:
            self.lesson = lesson
        else:
            logger.error("lesson %d", lesson)


class CourseTeacher:
    name = None      # 教师
    title = None     # 职称：教授，副教授。。。

    def __init__(self, name, title=None):
        """

        :type name: str
        :type title: str
        """
        self.name = name
        self.title = title


class CourseRecurrence:
    recurrence = None
    weeks = None     # [(nth_week, None), (nth_week_start, nth_week_end)]
    odd_even = 0     # 0 每天 1 奇数 2 偶数

    def __init__(self, recurrence):
        self.recurrence = recurrence

        result = re.match(u" *\[([\d, \-]+)(\w?)(\w)\] *", recurrence, re.U).groups()
        self.weeks = result[0]
        self.odd_even = 0
        if result[1] == u'单':
            self.odd_even = 1
        elif result[1] == u'双':
            self.odd_even = 2

        self.weeks = []

        for week_interval in result[0].split(u','):
            week_tuple = week_interval.split(u'-')
            if len(week_tuple) == 1:
                self.weeks.append((self.adjust(int(week_tuple[0])), None))
            else:
                self.weeks.append((int(week_tuple[0]), int(week_tuple[1])))

    def adjust(self, nth_week):
        if self.odd_even == 1:    # odd weeks
            if nth_week % 2 == 0:
                return nth_week + 1
        elif self.odd_even == 2:  # even weeks
            if nth_week % 2 == 1:
                return nth_week + 1
        return nth_week


class CourseEntry:
    name = None        # 课程
    type = None        # 性质：选修， 必修
    mode = None        # 考察方式：考试，考察，论文
    teacher = None     # 教师
    where = None       # 地点
    when = None        # 时间
    recurrence = None  # 重复

    def __init__(self, name=None, type=None, mode=None, teacher=None, where=None, when=None, recurrence=None):
        """

        :type name: str | unicode
        :type type: str | unicode
        :type mode: str | unicode
        :type teacher: CourseTeacher
        :type where: SchoolLocation
        :type when: CourseTime
        :type recurrence: CourseRecurrence
        """
        self.name = name
        self.type = type
        self.mode = mode
        self.teacher = teacher
        self.where = where
        self.when = when
        self.recurrence = recurrence


