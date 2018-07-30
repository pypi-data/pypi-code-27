#! -*- coding:utf-8 -*-
"""
Description:
    mit down load
"""
from __future__ import print_function
from collections import OrderedDict
import argparse
import os
import pickle
import re
import sys
import textwrap
import time
if sys.version > '3':
    import urllib.request as ul
else:
    import urllib as ul



"""
global var
"""
COURSES_INFO = OrderedDict()
CIN = None
IS_DOWNLOAD_ACTIVE = False
PATH = ""
DOWNLOAD_FILE = ""


# DOWNLOADING_FILE = ""

P_ = {'a': r'<a.*?</a>',
      'course_preview': r'<a rel="coursePreview".*?</a>',
      'atxt': r'<a.*>(.*?)</a>',
      'url': r'href="(.*?)"',
      'courses_datas': r'((?:/[\w-]+)*/?[\w-]+\.(pdf|py|xml|srt|mp4|scm))',
      '404': r'<title>.*Page not Found.*</title>',
      'meta': r'<meta\s+content=.*?/>',
      'li': r'<li\s+class=.*?</li>'
     }

URL = {'home': 'https://ocw.mit.edu',
       'top': 'https://ocw.mit.edu/courses/find-by-topic',
       'catlog': 'https://ocw.mit.edu/courses/'
      }

"""
set env
"""
def setenv():
    """set some basic env pargs"""
    global CIN
    if sys.version > '3':
        CIN = input
    else:
        CIN = raw_input

def sleep(sec, string):
    """sleep render"""

    dash = '.'
    format = '\r {:<3}{}'
    for i in range(sec+1):
        dashs = dash * (i % 4) + ' ' * (3 - (i % 4))
        sys.stdout.write(format.format(string, dashs))
        sys.stdout.flush()
        time.sleep(1)
    print()

def readable_dir(prospective_dir):
    """ check if dir is exist or acessable"""

    if not os.path.isdir(prospective_dir):
        sys.exit("{} is not a valid path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        sys.exit("{} is not a readable dir".format(prospective_dir))

def check_and_make_dir(path):
    """ check path"""

    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
"""
internet
"""

def connect(url):
    """connect url"""

    try:
        reply = ul.urlopen(url)
        content = reply.read()
        return content
    except Exception:
        sys.exit(">>> connection error: %s" % sys.exc_info()[0])

def downloading(url, full_path, reporthook=None):
    """
    :param url:
    :param full_path:
    :param reporthook:
    :return:
    """
    try:
        ul.urlretrieve(url, full_path, reporthook)
    except Exception:
        print ('>>> {} download failed.'.format(url))

def reporthook(count, block_size, total_size):
    """progress bar for download"""

    pound = '#'
    global START_TIME
    if count == 0:
        START_TIME = time.time()
        return
    duration = time.time() - START_TIME
    progress_size = int(count * block_size)
    kbps = progress_size / (duration * 1024.0)

    ui = '\r    - {:<40} ... [{:<20}]{:>5}% {:>9} KB/s'

    progress = min(20, int(20 * count * block_size / total_size))
    percent = min(100, 100.0 * count * block_size / total_size)
    sys.stdout.write(ui.format(DOWNLOAD_FILE, pound * progress,
                               round(percent, 1), round(kbps, 1)))
    sys.stdout.flush()
    if progress == 20:
        sys.stdout.write('\n')

def filt_htm(content):
    """filt extra tabs for html courses_data"""
    if sys.version > '3':
        content = content.decode('utf-8')
    return re.sub(r'[\s\r\t\n]+', ' ', content)


def get_htm(url):
    """ """

    return filt_htm(connect(url))


"""
update database
"""
def get_basic_course_info_group(urlstring):
    """ urlstring = /courses/aeronautics-and-astronautics/16-00-in \
                    troduction-to-aerospace-engineering-and-design-spring-2003

        return string(department name)
    """
    basic_course_infos =  urlstring.split('/')
    department_name_component = [string.title() for string in basic_course_infos[2].split('-')]
    string_department_name = ' '.join(department_name_component)
    return string_department_name

def build_course_info(url_str, course_name=None, course_type=None, course_display_id=None):

    course_str = url_str[url_str.rindex('/') + 1: ]
    if COURSES_INFO.has_key(course_str):

        if course_display_id:
            COURSES_INFO[course_str]['course_display_id'].append(course_display_id)
        if course_name:
            COURSES_INFO[course_str]['course_name'] = course_name
        if course_type:
            COURSES_INFO[course_str]['course_type'] = course_type

    else:
        COURSES_INFO[course_str] =  {}
        COURSES_INFO[course_str]['department'] = get_basic_course_info_group(url_str)
        COURSES_INFO[course_str]['course_url'] = url_str

        if course_display_id:
            COURSES_INFO[course_str]['course_display_id'] = []
            COURSES_INFO[course_str]['course_display_id'].append(course_display_id)

        if course_name:
            COURSES_INFO[course_str]['course_name'] = course_name
        if course_type:
            COURSES_INFO[course_str]['course_type'] = course_type



# def init_department(department, department_name):
#     """init department element"""
#     DEPARTMENTS[department] = OrderedDict()
#     DEPARTMENTS[department]['name'] = department_name
#     DEPARTMENTS[department]['course'] = OrderedDict()
#
# def init_course_info(department, url_str, course_id):
#     """init course element"""
#     department['course'][course_id] = OrderedDict()
#     department['course'][course_id]['ref_id'] = course_id
#     department['course'][course_id]['url'] = url_str
#     department['course'][course_id]['name'] = None
#     department['course'][course_id]['type'] = None
#     department['count'] = department.get('count', 0) + 1
#
# def update_course_info(department, course_id, course_name=None,
#                        course_type=None, course_display_id=None):
#     """update course informations(ref_id, course_type, course name)"""
#     if course_name:
#         department['course'][course_id]['name'] = repr(course_name)
#     if course_type:
#         department['course'][course_id]['type'] = course_type
#     if course_display_id and course_display_id != course_id:
#         department['course'][course_display_id] = department['course'].pop(course_id)
#         REF_COURSES[course_id] = course_display_id

def update_database():
    """update course database"""
    clear_datas()
    catlog_index = get_htm(URL['catlog'])
    for i in re.findall(P_['course_preview'], catlog_index):
        url = re.findall(P_['url'], i)[0]
        text = re.findall(P_['atxt'], i)[0].strip()
        select_qualified_data(text.strip(), url.strip())  
    path = os.path.join(os.path.dirname(__file__), 'data', 'mitcl.dat')  
    with open(path, 'wb') as data:
        # pickle.dump([DEPARTMENTS, REF_COURSES], data, protocol=2)
        pickle.dump(COURSES_INFO, data, protocol=2)

def clear_datas():
    """empty global data dict"""
    COURSES_INFO.clear()
    # DEPARTMENTS.clear()
    # REF_COURSES.clear()

def select_qualified_data(text, url):
    """update course"""
    text = text.strip()
    if url.startswith('/courses'):
        if re.search(r'^\w+\.\S+$', text):
            build_course_info(url, course_display_id=text)
        elif re.match(r'^(Graduate|Undergraduate)$', text):
            build_course_info(url, course_type=text)
        else:
            build_course_info(url, course_name=text)


def load():
    """load database from json file"""
    global COURSES_INFO
    path = os.path.join(os.path.dirname(__file__), 'data', 'mitcl.dat')
    if os.path.exists(path):
        with open(path, 'r') as data:
            COURSES_INFO = pickle.load(data)
    else:
        print("download course database for first time")
        update_database()


"""
search function
"""

def search(string):
    """list qualified course
        course: {
                 'department': 'Electrical Engineering And Computer Science',
                 'course_type': 'Undergraduate',
                 'course_name': 'Design and Analysis of Algorithms (Spring 2015)',
                 'course_display_id': ['6.046J', '18.410J'],
                 'course_url': '/courses/electrical-engineering-and-computer-science/
                                 6-046j-design-and-analysis-of-algorithms-spring-2015'
                }
    """
    try:
        pattern = re.compile(string, re.IGNORECASE)
    except re.error:
        sys.exit(">>> Invalid pattern")
    for course in COURSES_INFO.values():
        # print ("##", course)
        if any([re.search(pattern, course_id) for course_id in course['course_display_id']]) or \
                re.search(pattern, course['course_name']) or \
                re.search(pattern, course['course_type']):
            yield (course)


def check(string):
    """list qualified course"""
    result = [i for i in search(string)]
    if len(result) > 1:
        print ('{:<5} {:<40} {}'.format("Index", "Course Id", "Course Name"))
        for index, course in enumerate(result):
            print ('{:<5} {:<40} {}'.format(index, '/'.join(course['course_display_id']),
                                            course['course_name']))
        try:
            number = int(CIN("select your course: "))
            course = result[number]
        except Exception:
            sys.exit(">>> wrong choice.")

        get_description(course)

    elif len(result) == 1:
        for index, course in enumerate(result):
            get_description(course)
    else:
         sys.exit('>>> course not found')

def get_description(course):
    """
    format:
        [department name]
        [course_id] [course_name] [author]
        [descripton]
    course: {
             'department': 'Electrical Engineering And Computer Science',
             'course_type': 'Undergraduate',
             'course_name': 'Design and Analysis of Algorithms (Spring 2015)',
             'course_display_id': ['6.046J', '18.410J'],
             'course_url': '/courses/electrical-engineering-and-computer-science/
                            6-046j-design-and-analysis-of-algorithms-spring-2015'
            }
    sub_urls = [(ref_url_of_sub_page, title_of_sub_page)
    """
    url = '{}/{}'.format(URL['home'], course['course_url'])
    course_index = get_htm(url)
    course_id = '/'.join(course['course_display_id'])

    sub_urls = []
    for meta in re.findall(P_['meta'], course_index):
        if re.search('Description', meta):
            description = repr(re.findall(r'content="(.*?)"', meta)[0].strip())
        if re.search('Author', meta):
            author = repr(re.findall(r'content="(.*?)"', meta)[0].strip())
    for li in re.findall(P_['li'], course_index):
        url = re.findall(P_['url'], li)[0].strip()
        sub_title = repr(re.findall(P_['atxt'], li)[0].strip())
        sub_urls.append((url, sub_title))

    department_name = course['department']
    course_name = course['course_name']
    dedent = textwrap.dedent(description).strip()
    dedent = textwrap.fill(dedent, initial_indent=' ' * 10, subsequent_indent=' ', width=80)
    print (' [{}]\n {:<20} {} - {}'.format(department_name, course_id, course_name, author))
    print (dedent)

    if IS_DOWNLOAD_ACTIVE:
        sleep(15, "preparing")
        download_subpage(sub_urls, department_name, course_id)

"""
down course info
"""

def download_subpage(tuple_sub_url_and_sub_title, department_name, course_id):
    """
    sub_urls = [(ref_url_of_sub_page, title_of_sub_page)

    print_tag format:
    root
        - sub folders
            + files ...
        - sub folders
            + files ...
    """
    print ('\n{:*^40}'.format("Files Retrieved"))
    print(department_name)
    path_depart = '_'.join(department_name.split()).lower()
    path_course = course_id.replace('.', '_')
    if PATH:
        path_course = os.path.join(PATH, path_depart, path_course)
        check_and_make_dir(path_course)
    else:
        readable_dir(os.getcwd())
        path_course = os.path.join(os.getcwd(), path_depart, path_course)
        check_and_make_dir(path_course)

    for _ in tuple_sub_url_and_sub_title:
        sub_url, sub_title = _
        print('\n+  {}'.format(sub_title))
        sub_url = '{}/{}'.format(URL['home'], sub_url)
        course_sub_index = get_htm(sub_url)

        # return tuple list [ref_url_of_file, type_of_file]
        for file_url, _ in set(re.findall(P_['courses_datas'], course_sub_index)):
            if file_url.count('/') == 0:
                continue
            else:
                sub_title = str('_'.join(sub_title.split()).lower())
                check_and_make_dir(os.path.join(path_course, sub_title))
                file_url = '{}{}'.format(URL['home'], file_url)
                # filter the test wrong match test case
                path_file = os.path.join(path_course, sub_title, file_url.split('/')[-1])
                global DOWNLOAD_FILE
                DOWNLOAD_FILE = file_url.split('/')[-1]
                downloading(file_url, path_file, reporthook)

"""
args
"""

def parse_arg():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description='MIT course check and download.')
    parser.add_argument('-c', '--check', metavar='course',
                        help='Find course with course id or name, re support.')
    parser.add_argument('-d', '--download', action='store_true',
                        help='Download course files')
    parser.add_argument('-p', '--path', type=readable_dir,
                        help='Custom defined direction. Default stored in current direction')
    parser.add_argument('--update', action='store_true',
                        help='Update course database')
    args = parser.parse_args()
    if len(sys.argv) == 1:
        sys.exit(parser.print_help())
    return args

def handle_args(args):
    """arg handle """
    global IS_DOWNLOAD_ACTIVE, PATH
    if args.update:
        print ("Updating database...")
        update_database()
        print ("Update completed...")

    if args.download:
        IS_DOWNLOAD_ACTIVE = True
        if args.check is None:
            sys.exit(">>> -c is required when -d is called")
    if args.check:
        check(args.check)

"""
main func and test func
"""

def test1():
    """
    :return:
    """
    url = "https://www.python.org/ftp/python/2.7.15/python-2.7.15-macosx10.6.pkg"
    to_file = "/Volumes/Transcend/coding/python/project/mit/test.pkg"
    global  DOWNLOAD_FILE
    DOWNLOAD_FILE = "python-2.7.15-macosx10.6.pkg"
    downloading(url, to_file, reporthook)


def testDatabase():
    """update course database"""
    catalog_index = get_htm(URL['catlog'])
    for i in re.findall(P_['course_preview'], catalog_index):
        url = re.findall(P_['url'], i)[0]
        text = re.findall(P_['atxt'], i)[0].strip()
        # print (text," ===== ", url) # Pass
        test_select_qualified_data(text.strip(), url.strip())
    # path = os.path.join(os.path.dirname(__file__), 'data', 'mitcl.dat')
    # with open(path, 'wb') as data:
    #     pickle.dump([DEPARTMENTS, REF_COURSES], data, protocol=2)
    # print (COURSES_INFO)
    search('6.042')


def test_select_qualified_data(text, url):

    """update course"""
    text = text.strip()
    # print ("@@@", text, url)
    if url.startswith('/courses'):

        if re.search(r'^\w+\.\S+$', text):
            # print ("@@@", text, url)

            build_course_info(url, course_display_id=text)
        elif re.match(r'^(Graduate|Undergraduate)$', text):
            # print (text, url)
            build_course_info(url, course_type=text)
        else:
        #     print (text, url)
            build_course_info(url, course_name=text)

def main():
    """main"""
    setenv()
    load()
    handle_args(parse_arg())

if __name__ == '__main__':
    main()

