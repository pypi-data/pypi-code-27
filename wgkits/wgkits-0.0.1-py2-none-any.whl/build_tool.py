# -*- coding:utf-8 -*
"""
author: wanggeng
date: 2018-06-08
func: build apk tools

"""
import os,re,sys
import json
import codecs
import shutil

from list_con import MyListConf
from jinja2 import FileSystemLoader as FSLoader
from jinja2 import Environment as Env
try:
    from shutil import which
except ImportError:
    from backports.shutil_which import which
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def path2unix(*pathes):
    return re.sub(r'(\\\\|//|\\)', r'/', os.path.join(*pathes))

"""
出现异常时，终止脚本运行并显示错误信息
"""
def sys_quit(*str):
    log(str)
    sys.exit(10)

"""
 merge all elements in c to s
"""
def merge_dict(s,c):
    r=s.copy()
    r.update(c)
    return r

def has_path(path):
    return True if os.path.exists(path) else False

def has_file(path):
    return True if os.path.isfile(path) else False
def has_dir(path):
    return True if os.path.isdir(path) else False

def log(*str):
    print(str)

def get_cmd(name):
    return which(name)

def get_ndk_cmd():
    cmd=get_cmd("ndk-build")
    if cmd:
        return cmd
    else:
        log("ndk path not exist!")
        sys.exit(10)

def get_ant_cmd():
    cmd=get_cmd("ant")
    if cmd:
        return cmd
    else:
        log("ant path not exist!")
        sys.exit(10)

def get_android_cmd():
    cmd=get_cmd("android")
    if cmd:
        return cmd
    else:
        log("android sdk path not exist!")
        sys.exit(10)

def get_templates():
    return (os.path.join(os.getcwd(),"thirdparty/build_tools/templates"))

def render_template(tmp_name, dic, path=get_templates()):
    tmpLoader = FSLoader(searchpath=path)
    tmpEnv = Env(loader=tmpLoader)
    tmpl=tmp_name
    template = tmpEnv.get_template(tmpl)
    outputText = template.render(dic)
    return outputText

def read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path) as f:
            cfg_json=json.load(f)
            return cfg_json

def write_json(file_path, str):
    if os.path.exists(file_path):
        with open(file_path, 'w') as f:  
            json.dump(str, f, encoding="utf-8")

def read_file(file_name, lines=False):
    with codecs.open(file_name,'r',encoding='utf8') as f:
        return f.readlines() if lines else f.read()

def write_file(file_name, str):
    with codecs.open(file_name,'w',encoding='utf8') as f:
        f.write(str)

def list_dir(sourceDir, include_source=None, include_file=True):
    """与 :func:`os.listdir()` 类似，但提供一些筛选功能，且返回生成器对象。
    :param str sourceDir: 待处理的文件夹。
    :param bool include_source: 遍历结果中是否包含源文件夹的路径。
    :param bool include_file:    是否包含文件。True 表示返回的内容中既包含文件，又
                                包含文件夹；Flase 代表仅包含文件夹。
    :return: 一个生成器对象。
    """
    for cur_file in os.listdir(sourceDir):
        if cur_file.lower() == ".ds_store":
            continue
        pathWithSource = os.path.join(sourceDir, cur_file)
        if include_file or os.path.isdir(pathWithSource):
            if include_source:
                yield pathWithSource
            else:
                yield cur_file

def copy_dir(sou_dir, dst_dir, del_dst=False, del_subdst=False):
    """:func:`shutil.copytree()` 也能实现类似功能，
    但前者要求目标文件夹必须不存在。
    而 copy_dir 没有这个要求，它可以将 sou_dir 中的文件合并到 dst_dir 中。
    :param str sou_dir: 待复制的文件夹；
    :param str dst_dir: 目标文件夹；
    :param bool del_dst: 是否删除目标文件夹。
    :param bool del_subdst: 是否删除目标子文件夹。
    """
    if del_dst and os.path.isdir(del_dst):
        shutil.rmtree(dst_dir)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for cur_file in list_dir(sou_dir):
        dst_file = os.path.join(dst_dir, cur_file)
        cur_file = os.path.join(sou_dir, cur_file)
        if os.path.isdir(cur_file):
            if del_subdst and os.path.isdir(dst_file):
                shutil.rmtree(dst_file)
                os.makedirs(dst_file)
            copy_dir(cur_file, dst_file)
        else:
            shutil.copyfile(cur_file, dst_file)

def write_xml(path, root):
    data=ET.tostring(root, encoding='utf8', method='xml')
    with codecs.open(path, 'w') as f:
        f.write(data)

def read_xml(path):
    tree=ET.parse(path, parser=ET.XMLParser(encoding='utf-8'))
    root=tree.getroot()
    return root

def modify_elem_txt(root, t_name, attri, elem_new):
    for n in root.iter(t_name):
        if n.attrib == attri:
            n.text=elem_new
    return root

def add_string_elem(root, attri_v, txt):
    t=ET.SubElement(root, 'string',{'name':attri_v})
    t.text=txt
    t.tail="\n"
    return root

def has_list_section(path, sec_name):
    cfg=MyListConf()
    cfg.readfp(codecs.open(path, "r", 'utf-8'))
    return cfg.has_list(sec_name)

def get_list(path, sec_name):
    if has_list_section(path, sec_name):
        cfg=MyListConf()
        cfg.readfp(codecs.open(path, "r", 'utf-8'))
        return cfg.list(sec_name)
    else:
        sys_quit("no sec_name={0} in {1}" .format(sec_name, path))

"""
delete all the files with the pattern given
"""
def remove_files(path, p):
    if not has_path(path):
        sys_quit("path={0} not exist!" .format(path))
    log("current workdir={0}" .format(path2unix(path)))
    for root, folder, files in os.walk(path):
        for file in files:
            if p.match(file):
                path=path2unix(os.path.join(root, file))
                log("del file:{0}" .format(path))
                os.remove(path)
