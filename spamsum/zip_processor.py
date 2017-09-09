from zipfile import ZipFile, is_zipfile
from cStringIO import StringIO


def extract_all(fileobject):
    zipobject = ZipFile(fileobject)
    namelist = sorted(zipobject.namelist())
    return ''.join(zipobject.read(name) for name in namelist)


# XXX consider changing semantics to "file/data loader"
def process_zip(s):
    fileobject = StringIO(s)

    if is_zipfile(fileobject):
        return extract_all(fileobject)
    else:
        return s


if __name__ == '__main__':
    from sys import argv
    path = argv[1]
    s = open(path).read()
    print process_zip(s)
