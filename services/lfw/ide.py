from pylabs import q, p
from alkira import Alkira
import os

TASKLETS = ('impl/ui/form',
            'impl/ui/wizard')
            
class ide(object):
    def __init__(self):
        self.alkira = Alkira(p.api)
        
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
        
        for dir in q.system.fs.listDirsInDir(fullpath):
            dirname = q.system.fs.getBaseName(dir)
            results.append({"state": "closed" if self._hasChildren(dir) else "leaf",
                            "data": dirname,
                            "attr": {"id": self._getID(project, dir)}})
        
        for file in q.system.fs.listFilesInDir(fullpath, filter="*.py"):
            filename = q.system.fs.getBaseName(file)
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
        return q.system.fs.writeFile(filepath, content)
    
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
            
    @q.manage.applicationserver.expose
    def rename(self, id, name):
        project, relativepath = self._resolveID(id)
        path = q.system.fs.joinPaths(self._getProjectPath(project), relativepath)
        newname = q.system.fs.joinPaths(q.system.fs.getDirName(path), name)
        
        if q.system.fs.exists(newname):
            raise RuntimeError("A file with the same name already exists")
        
        if q.system.fs.isFile(path):
            q.system.fs.renameFile(path, newname)
        elif q.system.fs.isDir(path):
            q.system.fs.renameDir(path, newname)

