import re as _re
from subprocess import run as _run,\
        PIPE as _PIPE
from .pep import Version as _Version

_git_describe_re = r'(?P<tag>.*)'\
        + r'(?:-(?P<post>[0-9]+)-g(?P<hash>[0-9a-f]{8,40}))'\
        + r'(?:-(?P<dirty>dirty))?'\
        + r'$'
_git_describe_re = _re.compile(_git_describe_re)

def _tag_n(t):
    if t:
        return str(t)
    raise ValueError()
def _post_n(p):
    if p is None:
        return 0
    return int(p)
def _hash_n(h):
    if h:
        return str(h)
    raise ValueError()
def _dirty_n(d):
    return bool(d)

class Description(object):
    def __init__(self,dstring):
        if isinstance(dstring,str):
            self.description = dstring
        elif isinstance(dstring,dict):
            self.__tag = dstring['tag']
            self.__post = dstring.get('post',0)
            self.__hash = dstring['hash']
            self.__dirty = dstring.get('dirty',False)
        else:
            raise TypeError("Cannot create Description from {}".format(type(dstring)))

    def __getitem__(self,key):
        return getattr(self,key)
    def keys(self):
        return (key for key in ['tag','post','hash','dirty'])
    __iter__=keys
    def items(self):
        return ((key,self[key]) for key in self.keys())

    @property
    def description(self):
        return { 'tag': self.tag, 'post': self.post, 'hash': self.hash, 'dirty': self.dirty }
    @description.setter
    def description(self,dstring):
        m = _git_describe_re.match(dstring)
        if not m:
            raise ValueError("Not a description string: '{}'".format(dstring))
        self.__tag = _tag_n(m.group('tag'))
        self.__post = _post_n(m.group('post'))
        self.__hash = _hash_n(m.group('hash'))
        self.__dirty = _dirty_n(m.group('dirty'))

    @property
    def tag(self):
        return self.__tag
    @property
    def post(self):
        return self.__post
    @property
    def hash(self):
        return self.__hash
    @property
    def dirty(self):
        return self.__dirty

    def version(self):
        v = _Version(self.tag)
        if v.local.value is not None:
            raise ValueError("Local version...")
        local = []
        if (self.post and v.dev.value) or self.dirty:
            local.append('git')
            local.append(self.hash[:8])
        if self.dirty:
            local.append('dirty')
        if self.post:
            if v.dev.value is None:
                v.post += 0
            v.dev += self.post
        if len(local):
            v.local = local
        return v

"""
git describe --tags --long --dirty --abbrev=40
"""
_git_describe_cmd = ['git','describe','--tags','--long','--dirty','--abbrev=40']
def describe():
    ret = _run(_git_describe_cmd,stdout=_PIPE,stderr=_PIPE)
    if ret.returncode:
        return None
    dstring = ret.stdout.split(b'\n')[0].decode('utf-8')
    return Description(dstring)

def taglist_to_versionlist(tl):
    vl = []
    for t in tl:
        try:
            v = _Version(t)
            vl.append(v)
        except ValueError:
            continue
    vl.sort()
    return vl

"""
git tag --merged
"""
_git_taglist_cmd = ['git','tag','--merged']
_git_revlist_cmd = ['git','rev-list','HEAD']
def versiontag():
    ret = _run(_git_taglist_cmd,stdout=_PIPE)
    ret.check_returncode()
    taglist = ret.stdout.decode('utf-8').split('\n')[:-1]
    versions = taglist_to_versionlist(taglist)
    if versions:
        version = versions[-1]
        tag = version.tag
        vtag = version.tag
    else:
        ret = _run(_git_revlist_cmd,stdout=_PIPE)
        ret.check_returncode()
        tag = list(ret.stdout.decode('utf-8').split('\n'))[-2]
        vtag = '0'
        version = _Version(vtag)
    if version.local.value is not None:
        raise ValueError("Should not have a local version tag...")
    ret = _run(['git','rev-list','--count','{}..HEAD'.format(tag),'--'],stdout=_PIPE,stderr=_PIPE)
    if ret.returncode:
        raise RuntimeError(ret.stderr.decode('utf-8'))
    post=int(ret.stdout.split(b'\n')[0].decode('utf-8'))
    ret = _run(['git','rev-parse','HEAD'],stdout=_PIPE,stderr=_PIPE)
    if ret.returncode:
        raise RuntimeError(ret.stderr.decode('utf-8'))
    hash=ret.stdout.split(b'\n')[0].decode('utf-8')
    ret = _run(['git','diff-index','--quiet','HEAD','--'],stdout=_PIPE,stderr=_PIPE)
    dirty=bool(ret.returncode)
    return Description(dict(tag=vtag,post=post,hash=hash,dirty=dirty))

if __name__=='__main__':
    print(versiontag().version())
