from pylabs import q

LOCK_DIR_PATH = q.system.fs.joinPaths(q.dirs.varDir, 'lock', 'dcpm')

if not q.system.fs.isDir(LOCK_DIR_PATH):
    q.system.fs.createDir(LOCK_DIR_PATH)

class isLockedException(Exception):
    pass

def aquire_lock(exceptionText, *args):
    fileName = '_'.join(args) + '.lock'
    lockPath = q.system.fs.joinPaths(LOCK_DIR_PATH, fileName)
    if q.system.fs.isFile(lockPath):
        raise isLockedException("%s: %s" % (exceptionText, lockPath))
    q.system.fs.createEmptyFile(lockPath)

def release_lock(*args):
    fileName = '_'.join(args) + '.lock'
    lockPath = q.system.fs.joinPaths(LOCK_DIR_PATH, fileName)
    if q.system.fs.isFile(lockPath):
        q.system.fs.removeFile(lockPath)

def is_locked(*args):
    fileName = '_'.join(args) + '.lock'
    lockPath = q.system.fs.joinPaths(LOCK_DIR_PATH, fileName)
    if q.system.fs.isFile(lockPath):
        return True
    return False

     