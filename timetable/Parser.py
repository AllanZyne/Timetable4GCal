# -*- encoding: utf-8 -*-
#
#

"""
   解析课程表数据
"""

__author__ = 'Allan Zyne'


import re
from HTMLParser import HTMLParser
import Data
import logging

logging.basicConfig(level=logging.DEBUG, format='')
logger = logging.getLogger(__name__)


ROWS = 5
COLS = 7

HTML_TYPE = 1
EXCEL_TYPE = 2

CONTENT_CR = 3   # number of cr of a content cell


table_content = [[[] for col in range(COLS+1) ] for row in range(ROWS+1)]


class CourseParser:
    def __init__(self, content_pattern, data):
        """

        :type content_pattern: collections.OrderedDict
        :type data: unicode

        """
        self.data = data

        if self.__data_type(data) == HTML_TYPE:
            self.parser = CourseHTMLParser()
        else:
            pass

        self.content = content_pattern
        logger.debug(u" *".join(content_pattern.values()))
        self.pattern = re.compile(u" *".join(content_pattern.values()), re.U)

    def __data_type(self, data):
        return HTML_TYPE

    def __match_content(self, rows, cols):
        course_list = []
        content = self.content

        logger.debug("\nStart Matching Content\n===============================")

        for i in range(1, rows+1):     # 节
            logger.debug(u"第%d节", i)
            for j in range(1, cols+1): # 周
                for text in table_content[i][j]:
                    if text.lstrip(u' \t\n\r'):
                        logger.debug(u"周%d", j)

                        for key, value in zip(content.keys(), re.match(self.pattern, text).groups()):
                            content[key] = value

                        course = Data.CourseEntry()
                        course.name = content.get(u"课程")
                        logger.debug(u"\t课程: %s", course.name)

                        course.teacher = Data.CourseTeacher(name=content.get(u"教师"), title=content.get(u"职称"))
                        logger.debug(u"\t教师: %s", course.teacher.name)

                        course.mode = content.get(u"考察方式")
                        if course.mode:
                            logger.debug(u"\t考察方式: %s", course.mode)

                        course.when = Data.CourseTime(weekday=j, lesson=i)
                        course.where = Data.SchoolLocation(location=content[u"地点"])
                        logger.debug(u"\t地点: %s", course.where.location)

                        course.recurrence = Data.CourseRecurrence(recurrence=content[u'重复'])

                        course_list.append(course)

        return course_list

    def start(self):
        """

        :rtype: [var.CourseEntry]
        """
        self.parser.feed(self.data)
        return self.__match_content(5, 7)



class CourseHTMLParser(HTMLParser):
    start = False
    row_c = 0
    col_c = 0
    content_c = 0
    content = ""

    def handle_starttag(self, tag, attrs):
        if self.start:
            if tag == 'tr':
                self.row_c += 1
                self.col_c = 0
            elif tag == 'td':
                self.col_c += 1

    def handle_endtag(self, tag):
        if self.start:
            if self.row_c == 5 and self.col_c == 8:
                self.start = False

    def handle_data(self, data):
        if self.start:
            if self.row_c == 1 or self.row_c == 3:                          # 1、3节  隔2列
                if self.col_c > 2:
                    self.put_data(self.row_c, self.col_c-2, data)
            elif self.row_c == 2 or self.row_c == 4 or self.row_c == 5:     # 2、4、5节 隔1列
                if self.col_c > 1:
                    self.put_data(self.row_c, self.col_c-1, data)

        elif data.strip(u' \r\n\t') == u'星期一':
            self.start = True

    def put_data(self, row, col, data):
        self.content_c += 1
        if self.content_c == CONTENT_CR:
            logger.debug("%d  %d -> %s", row, col, self.content + data)
            table_content[row][col].append(self.content + data)

            self.content = ""
            self.content_c = 0
        else:
            self.content += data

    def feed(self, data):
        logger.debug("\nStart CourseHTMLParser")
        logger.debug(u"周 节")

        HTMLParser.feed(self, data)

        return table_content

if __name__ == "__main__":
    text = u"大型数据库技术 (必)[考查]学分：3.0 总学时：48 安排学时：32 郭东恩 (副教授) [1-5, 7-17周][1-2节]" \
           u" (本部)15302计算机基础实验室(实验室)"
    pattern = u"([\w ]+) *(\(\w+\)) *(\[\w*\]) *([\w：\d\.]+) *([\w：\d\.]+) *([\w：\d\.]+) *(\w+) *" \
              u"(\(\w+\)) *(\[[\d\-, ]+\w?周\]) *(\[[\d\-]+节\]) *(\(本部\)) *(\d+[\w\d\(\)]+)"
    for t in re.match(pattern, text, re.U).groups():
        print t

    # col = 3
    # l = [ [ [] for col in range] for col in range(col)]
    # print l
    # l[1].append(1)
    # print l
    # l[2].append(2)
    # print l

