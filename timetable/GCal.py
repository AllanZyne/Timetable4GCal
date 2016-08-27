# -*- encoding: utf-8 -*-
#
#

"""
   Google Calendar
"""

__author__ = 'Allan Zyne'


import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
import logging

logging.basicConfig(level=logging.DEBUG, format='')
logger = logging.getLogger(__name__)


DEFAULT_TIMEZONE = 'Asia/Hong_Kong'
DEFAULT_LOCATION = u'南阳理工学院'
DEFAULT_CAL_NAME = u'课程表'


def date_t_time_format(course_schedule, nth_week=1, weekday=1, nth_class=1):
    """

    :type course_schedule: timetable.Time.CourseSchedule
    :type nth_week: int
    :type weekday: int
    :type nth_class: int
    :rtype: ("", "")
    """
    datetime = course_schedule.get_datetime(nth_week, weekday, nth_class)
    return datetime[0].strftime('%Y%m%dT%H%M%S'), datetime[1].strftime('%Y%m%dT%H%M%S')


class TimeTableCalendar:
    def __init__(self, email, password, timetable):
        """

        :type email: str
        :type password: str
        :type timetable: TimeTable.TimeTable
        """

        self.timetable = timetable
        self.email = email
        self.password = password
        self.calendar_name = DEFAULT_CAL_NAME
        self.timezone = DEFAULT_TIMEZONE
        self.event_list = []

        self.cal_client = gdata.calendar.client.CalendarClient(source='Nyist-TimeTable4GCal-1.0')

    def set_calendar_name(self, name):
        self.calendar_name = name

    def __insert_calendar(self, title, description, time_zone=DEFAULT_TIMEZONE, location=DEFAULT_LOCATION,
                          color='#2952A3'):
        """Creates a new calendar using the specified var.

        :type title: unicode
        :type description: unicode
        :type time_zone: str
        :type location: unicode
        :type color: str
        """

        logger.debug('Creating new calendar with title "%s"', title)

        calendar = gdata.calendar.data.CalendarEntry()
        calendar.title = atom.data.Title(text=title)
        calendar.summary = atom.data.Summary(text=description)
        calendar.where.append(gdata.calendar.data.CalendarWhere(value=location))
        calendar.color = gdata.calendar.data.ColorProperty(value=color)
        calendar.timezone = gdata.calendar.data.TimeZoneProperty(value=time_zone)
        calendar.hidden = gdata.calendar.data.HiddenProperty(value='false')

        new_calendar = self.cal_client.InsertCalendar(new_calendar=calendar)
        return new_calendar

    def __insert_course(self, course):
        """

        :type course: timetable.Data.CourseEntry
        :rtype: gdata.calendar.var.CalendarEventEntry
        """
        logger.debug("Insert course: %s", course.name)
        recurrence_data_list = self.__course_recurrence_data(course.when, course.recurrence)
        for recurrence_data in recurrence_data_list:
            event = self.__insert_event(course.name, course.teacher.name, course.where.location, recurrence_data)
            self.event_list.append(event)

        return event

    def __course_recurrence_data(self, course_time, course_recur):
        """

        :type course_time: timetable.Data.CourseTime
        :type course_recur: timetable.Data.CourseRecurrence
        :return: str
        """
        weekday = course_time.weekday
        nth_class = course_time.lesson

        weekly_interval = course_recur.odd_even

        recurrence_data_list = []

        for nth_week_start, nth_week_end in course_recur.weeks:
            dt_str = date_t_time_format(self.timetable.course_schedule, nth_week_start, weekday, nth_class)

            dtstart = "DTSTART;TZID=%s:%s\r\n" % (self.timezone, dt_str[0])
            dtend = "DTEND;TZID=%s:%s\r\n" % (self.timezone, dt_str[1])
            rrule = ""

            if nth_week_end is not None:
                step = 1
                if weekly_interval:
                    step = 2

                count = len(range(nth_week_start, nth_week_end+1, step))

                if weekly_interval == 0:
                    rrule = "RRULE:FREQ=WEEKLY;COUNT=%s\r\n" % count
                else:
                    rrule = "RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=%s\r\n" % count
            recurrence_data = dtstart + dtend + rrule
            logger.debug(recurrence_data)
            recurrence_data_list.append(recurrence_data)

        return recurrence_data_list

    def __insert_event(self, title, content, where, recurrence_data):
        """

        :type title: unicode
        :type content: unicode
        :type where: unicode
        :type recurrence_data: str
        :rtype: gdata.calendar.var.CalendarEventEntry
        """

        event = gdata.calendar.data.CalendarEventEntry()
        event.title = atom.data.Title(text=title)
        event.content = atom.data.Content(text=content)
        event.where.append(gdata.data.Where(value=where))
        event.recurrence = gdata.data.Recurrence(text=recurrence_data)

        new_event = self.cal_client.InsertEvent(event, self.calendar.content.src)

        return new_event

    def run_single_test(self):
        inserted_calendar = self.__insert_event(u'形势与政策Ⅴ',
                                                u'赵黎黎',
                                                u'3号楼3102多媒体(多媒体教室)',
                                                'DTSTART;TZID=Asia/Hong_Kong:20140103T162000\r\n'
                                                + 'DTEND;TZID=Asia/Hong_Kong:20140103T175000\r\n')

    def run(self, test=True):

        logger.debug("Login to Google count(%s)...", self.email)
        self.cal_client.ClientLogin(self.email, self.password, self.cal_client.source)

        logger.debug("Get calendars list...")
        feed = self.cal_client.GetOwnCalendarsFeed()

        self.calendar = None
        calendar_name = self.calendar_name

        if test:
            calendar_name += "_test"
            logger.debug("---------Test Mode---------")

        for a_calendar in feed.entry:
            if a_calendar.title.text == calendar_name:
                if test:
                    self.cal_client.Delete(a_calendar.GetEditLink().href)
                else:
                    self.calendar = a_calendar
                break

        if self.calendar is None:
            self.calendar = self.__insert_calendar(calendar_name, self.timetable.title)

        #
        for course in self.timetable.course_entry_list:
            event = self.__insert_course(course)


if __name__ == "__main__":
    user = "xxxxxx@gmail.com"
    pw = "xxxxxxxxxx"
