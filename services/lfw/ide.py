from pylabs import q, p
from alkira import Alkira
import os
import hashlib
from osis.store.OsisDB import OsisDB
import itertools
import sys

GUIDMAP = [8, 4, 4, 4, 12]
EXTENSIONS = (".py", ".html", ".js", ".txt", ".md", ".cfg", "")

TASKLETS = ['impl/action',
            'impl/actor',
            'impl/authenticate',
            'impl/authorize',
            'impl/init',
            'impl/osis',
            'impl/schedule',
            'impl/setup',
            'impl/ui']



class ide(object):
    def __init__(self, tasklets=[]):
        basedir = os.path.join(q.dirs.pyAppsDir, p.api.appname)
        self._authenticate = q.taskletengine.get(os.path.join(basedir, 'impl', 'authenticate'))
        self._authorize = q.taskletengine.get(os.path.join(basedir, 'impl', 'authorize'))

        self.tasklets = tasklets
        self.alkira = Alkira(p.api)
        self.connection = OsisDB().getConnection(p.api.appname)

        #
        # Normally this part isn't needed because we have the Auth service but because we cannot call the service
        # from inside the authorize tasklet (because this is implemented in the main thread of the appserver).
        # So we just do the same as the Auth service is doing and then use the backend directly.
        #

        #load auth backend
        config = q.tools.inifile.open(q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "cfg", "auth.cfg"))
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "auth_backend"))
        backend = __import__(config.getValue("auth", "backend"), level=1)
        self.authBackend = getattr(backend, "BACKEND")()

    def checkAuthentication(self, request, domain, service, methodname, args, kwargs):
        q.logger.log("HEADERS from ide.checkAuthentication %s" % str(request._request.requestHeaders))
        tags = ('authenticate',)
        params = dict()
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = "ide." + methodname
        params['args'] = args
        params['kwargs'] = kwargs
        params['result'] = True
        self._authenticate.execute(params, tags=tags)
        return params.get('result', False)

    def checkAuthorization(self, criteria, request, domain, service, methodname, args, kwargs):
        tags = ('authorize',)
        params = dict()
        params['criteria'] = criteria
        params['request'] = request
        params['domain'] = domain
        params['service'] = service
        params['methodname'] = "ide." + methodname
        params['args'] = args
        params['kwargs'] = kwargs
        params['result'] = True

        #
        # Normally this part isn't needed because we have the Auth service but because we cannot call the service
        # from inside the authorize tasklet (because this is implemented in the main thread of the appserver).
        # So we just do the same as the Auth service is doing and then use the backend directly.
        #
        tags += ('authbackend', )
        params['authbackend'] = self.authBackend


        self._authorize.execute(params, tags=tags)
        return params.get('result', False)

    def _resolveID(self, id):
        pieces = id.split(os.path.sep)
        project = self.alkira.getProject(pieces.pop(0))
        return project, q.system.fs.joinPaths(*pieces) if pieces else ""

    def _getID(self, project, path):
        projectpath = q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, project.path)
        id = path.replace(projectpath, "")
        id = id.lstrip("/")
        return q.system.fs.joinPaths(project.name, id)

    def _hasChildren(self, path):
        return bool(q.system.fs.walk(path, return_folders=1))

    def _getProjectPath(self, project):
        return q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, project.path)

    def _IDtoGUID(self, id):
        md5 = hashlib.md5(id)
        hash = md5.hexdigest()
        parts = []
        li = 0
        for i in GUIDMAP:
            part = hash[li:li + i]
            if len(part) != i:
                part += "0" * (i - len(part))
            parts.append(part)
            li += i

        return "-".join(parts)

    def _filter(self, file):
        return os.path.splitext(file)[1] in EXTENSIONS

    def _updateFileIndex(self, id, content):
        guid = self._IDtoGUID(id)
        name = q.system.fs.getBaseName(id)
        self.connection.viewSave("ui", "_index", "global_index_view", guid, guid, {'name': name,
                                                                                   'content': content,
                                                                                   'url': 'ide://%s' % id})

    def _updateDirIndex(self, id):
        project, relativepath = self._resolveID(id)
        fullpath = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        for file in q.system.fs.walk(fullpath, 1):
            if not self._filter(file):
                continue
            self._updateFileIndex(self._getID(project, file), q.system.fs.fileGetContents(file))


    def _deleteIndex(self, id):
        url = "ide://%s" % id
        self.connection.runQuery("delete from ui__index.global_index_view where url LIKE '%s%%'" % url)

    def _touchTasklets(self, project, relativepath):
        fullpath = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        for td in itertools.chain(TASKLETS, self.tasklets):
            ftd = q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, td)
            if fullpath.startswith(ftd):
                q.system.fs.createEmptyFile(q.system.fs.joinPaths(ftd, "tasklets_updated"))
                break

    @q.manage.applicationserver.expose_authorized(context={})
    def getProjectNode(self, id="."):
        results = []
        if not id:
            raise RuntimeError("Invalid ID")

        apppath = q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname)
        closed = lambda x: bool(q.system.fs.listDirsInDir(x))

        fullpath = q.system.fs.joinPaths(apppath, id)
        fullpath = os.path.relpath(fullpath)

        for dir in q.system.fs.listDirsInDir(fullpath):
            name = q.system.fs.getBaseName(dir)
            dirid = os.path.relpath(q.system.fs.joinPaths(id, name))
            results.append({"state": "closed" if closed(dir) else "leaf",
                            "data": name,
                            "attr": {"id": dirid}})

        return results

    @q.manage.applicationserver.expose_authorized(context={})
    def createProject(self, name, path):
        self.alkira.createProject(name, path)
        self._updateDirIndex(name)

    @q.manage.applicationserver.expose_authorized(context={})
    def deleteProject(self, name):
        self.alkira.deleteProject(name)
        self._deleteIndex(name)

    @q.manage.applicationserver.expose_authorized(context={})
    def getProjects(self):
        return self.alkira.listProjectInfo()

    @q.manage.applicationserver.expose_authorized(context={})
    def getNode(self, id="."):

        results = []
        if not id:
            raise RuntimeError("Invalid ID")

        if id == ".":
            projects = self.alkira.listProjects()
            for project in projects:
                results.append({"state": "closed",
                                "data": project,
                                "attr": {"id": project,
                                         "rel": "project"}})

            return results

        project, relativepath = self._resolveID(id)
        projectpath = self._getProjectPath(project)
        fullpath = q.system.fs.joinPaths(projectpath, relativepath)

        if q.system.fs.isDir(fullpath):
            for dir in q.system.fs.listDirsInDir(fullpath):
                dirname = q.system.fs.getBaseName(dir)
                results.append({"state": "closed" if self._hasChildren(dir) else "leaf",
                                "data": dirname,
                                "attr": {"id": self._getID(project, dir)}})

            for file in q.system.fs.listFilesInDir(fullpath):
                filename = q.system.fs.getBaseName(file)
                if not self._filter(filename):
                    continue
                results.append({"state": "leaf",
                                "data": filename,
                                "attr": {"id": self._getID(project, file),
                                         "rel": "file"}})

        return results

    @q.manage.applicationserver.expose_authorized(context={})
    def getFile(self, id):
        project, relativepath = self._resolveID(id)
        filepath = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        return q.system.fs.fileGetContents(filepath)

    @q.manage.applicationserver.expose_authorized(context={})
    def setFile(self, id, content):
        project, relativepath = self._resolveID(id)
        filepath = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        q.system.fs.writeFile(filepath, content)
        self._updateFileIndex(id, content)
        self._touchTasklets(project, relativepath)

    @q.manage.applicationserver.expose_authorized(context={})
    def newFile(self, id):
        project, relativepath = self._resolveID(id)
        filepath = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        if q.system.fs.exists(filepath):
            raise RuntimeError("A file with the same name already exists")
        return q.system.fs.writeFile(filepath, "")

    @q.manage.applicationserver.expose_authorized(context={})
    def newDir(self, id):
        project, relativepath = self._resolveID(id)
        dirpath = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        if q.system.fs.exists(dirpath):
            raise RuntimeError("A file with the same name already exists")
        return q.system.fs.createDir(dirpath)

    @q.manage.applicationserver.expose_authorized(context={})
    def delete(self, id):
        project, relativepath = self._resolveID(id)
        path = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        if q.system.fs.isFile(path):
            q.system.fs.removeFile(path)
        elif q.system.fs.isDir(path):
            q.system.fs.removeDirTree(path)
        self._deleteIndex(id)
        self._touchTasklets(project, relativepath)

    @q.manage.applicationserver.expose_authorized(context={})
    def rename(self, id, name):
        project, relativepath = self._resolveID(id)

        path = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        newname = q.system.fs.joinPaths(q.system.fs.getDirName(path), name)
        newid = self._getID(project, newname)

        if q.system.fs.exists(newname):
            raise RuntimeError("A file with the same name already exists")

        self._deleteIndex(id)
        if q.system.fs.isFile(path):
            q.system.fs.renameFile(path, newname)
            self._updateFileIndex(newid, q.system.fs.fileGetContents(newname))
        elif q.system.fs.isDir(path):
            q.system.fs.renameDir(path, newname)
            self._updateDirIndex(newid)

        self._touchTasklets(project, relativepath)

    @staticmethod
    def getAuthorizedFunctions():
        functions = []

        for funcName in dir(ide): # loop over functions of our class
            funcObj = getattr(ide, funcName)
            if getattr(funcObj, "APPLICATIONSERVER_EXPOSE_AUTHORIZED", False):
                #needs authorization
                if hasattr(funcObj, "auth_categories"):
                    categories = getattr(funcObj, "auth_categories")
                    if "context" in categories:
                        functions.append({ "name": "ide." + funcName, "context": categories["context"] })
                    else:
                        functions.append({ "name": "ide." + funcName })

        return functions
