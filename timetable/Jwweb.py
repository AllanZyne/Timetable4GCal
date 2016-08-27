# -*- encoding: utf-8 -*-
#
#

"""
   从教务网络管理系统 http://172.31.31.34/jwweb/ 中提取有关课程检索的信息
"""

__author__ = 'Allan Zyne'


import urllib
import urllib2


course_select_url = "http://172.31.31.34/jwweb/ZNPK/KBFB_LessonSel.aspx"
course_table_url = "http://172.31.31.34/jwweb/ZNPK/KBFB_ClassSel_rpt.aspx"

course_select_html = None
course_table_html = None

class_value = {
    u"11软工（卓越）": "2011151901"
}

time_value = []


def get_time_value(school_year, semester):
    """
    :param school_year: 学年
    :param semester: 0 上学期 1 下学期

    """
    return str(school_year)+str(semester)


def get_time_value_list():
    pass


def get_class_value(class_name):
    # if course_select_html is None:
    #     get_course_select_html()

    return class_value[class_name]


def get_course_select_html():
    page = urllib2.urlopen(course_select_url)
    course_select_html = page.read()
    return course_select_html


def get_timetable_html(time_value, class_value):
    """
    从 教务管理系统 得到课程表，传递的 学年学期 school_year 和 班级值 class_value
    的值可以从这个网站得到

    :type school_year: str
    :type class_value: str
    :rtype: str
    """
    form = { 'Sel_XNXQ': time_value,           # 学年学期
             'txtxzbj': '',                    # 班级代号
             'Sel_XZBJ': class_value,          # 选择班级
             'type': '1',                      # 样式
             'Submit01': '\xbc\xec\xcb\xf7'}

    headers = { "Host": '172.31.31.34',
                "User_Agent": "Mozilla/5.0 (Windows NT 6.2; rv:26.0) Gecko/20100101 Firefox/26.0",
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                'Referer': 'http://172.31.31.34/jwweb/ZNPK/KBFB_ClassSel.aspx',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'keep_alive',
                'Content-Length': '72' }

    request = urllib2.Request(course_table_url, urllib.urlencode(form), headers)

    print request.get_data()
    print request.header_items()

    print "Send request to %s." %  course_table_url
    response = urllib2.urlopen(request)
    print "Get response."
    html = response.read()
    response.close()
    return html

