# coding=utf-8
import os
import sys
import hashlib
import functools
import qiniu

qn = qiniu.auth.Auth("A6QIIrx3TJ2f9QOUi3ozdUvCsWhoOoJUYLhRJO6z", "0EBm9OhxKiXWYTExqDUhSemN1qZBReci6BauDF6l")


def get_md5(object):
    with open(object, "rb") as fp:
        md5 = hashlib.md5()
        for bufer in iter(functools.partial(fp.read, 4096), b""):
            md5.update(bufer)
        return md5.hexdigest()


def get_ext(object):
    return os.path.splitext(object)[1]


def qn_upload(object):
    if os.path.isfile(object):
        remote = get_md5(object) + get_ext(object)
        token = qn.upload_token("upload", remote)
        ret = qiniu.put_file(token, remote, object)[0]
        # check
        assert ret["key"] == remote
        assert ret["hash"] == qiniu.etag(object)
        print("http://cloud.jacksao.wang/%s" % ret["key"])
    else:
        print("not file")


def cli(object=sys.argv):
    if len(object) == 1:
        print("usage: upload file")
    else:
        qn_upload(object[1])


if __name__ == "__main__":
    cli()
