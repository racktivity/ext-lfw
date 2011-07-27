from pylabs import q, p
from alkira import Alkira
import os
import hashlib
from osis.store.OsisDB import OsisDB

GUIDMAP = [8, 4, 4, 4, 12]
EXTENSIONS = [".py", ".html", ".js", ".txt", ""]

class ide(object):
    def __init__(self):
        self.alkira = Alkira(p.api)
        self.connection = OsisDB().getConnection(p.api.appname)
        
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
    
    @q.manage.applicationserver.expose
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
            
            for file in q.system.fs.listFilesInDir(fullpath, filter="*.py"):
                filename = q.system.fs.getBaseName(file)
                if not self._filter(filename):
                    continue
                results.append({"state": "leaf",
                                "data": filename,
                                "attr": {"id": self._getID(project, file),
                                         "rel": "file"}})
        
        return results
    
    @q.manage.applicationserver.expose
    def getFile(self, id):
        project, relativepath = self._resolveID(id)
        filepath = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        return q.system.fs.fileGetContents(filepath)
    
    @q.manage.applicationserver.expose
    def setFile(self, id, content):
        project, relativepath = self._resolveID(id)
        filepath = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        q.system.fs.writeFile(filepath, content)
        self._updateFileIndex(id, content)
    
    @q.manage.applicationserver.expose
    def newFile(self, id):
        project, relativepath = self._resolveID(id)
        filepath = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        if q.system.fs.exists(filepath):
            raise RuntimeError("A file with the same name already exists")
        return q.system.fs.writeFile(filepath, "")
    
    @q.manage.applicationserver.expose
    def newDir(self, id):
        project, relativepath = self._resolveID(id)
        dirpath = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        if q.system.fs.exists(dirpath):
            raise RuntimeError("A file with the same name already exists")
        return q.system.fs.createDir(dirpath)
    
    @q.manage.applicationserver.expose
    def delete(self, id):
        project, relativepath = self._resolveID(id)
        path = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        if q.system.fs.isFile(path):
            q.system.fs.removeFile(path)
        elif q.system.fs.isDir(path):
            q.system.fs.removeDirTree(path)
        self._deleteIndex(id)
            
    @q.manage.applicationserver.expose
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
            

