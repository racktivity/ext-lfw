import os

from pylabs import q

LOCK_DIR_PATH = os.path.join(q.dirs.varDir, 'lock')


if not os.path.isdir(LOCK_DIR_PATH):
    os.mkdir(LOCK_DIR_PATH)


class IsLockedException(Exception):
    pass


def acquire_lock(exceptionText, *args):
    fileName = '_'.join(args) + '.lock'
    lockPath = os.path.join(LOCK_DIR_PATH, fileName)
    try:
        f = os.open(lockPath, os.O_CREAT | os.O_EXCL)
        os.close(f)
    except OSError:
        raise IsLockedException("%s: %s" % (exceptionText, lockPath))


def release_lock(*args):
    fileName = '_'.join(args) + '.lock'
    lockPath = os.path.join(LOCK_DIR_PATH, fileName)
    try:
        os.unlink(lockPath)
    except OSError:  # if not present, ignore
        pass


def is_locked(*args):
    fileName = '_'.join(args) + '.lock'
    lockPath = os.path.join(LOCK_DIR_PATH, fileName)
    return os.path.isfile(lockPath):
