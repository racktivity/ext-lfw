from pylabs import q, p
from actionservice import ActionService

class editor(ActionService):
    def list2jstree(self, appname, path, items, isdir=False):
        result = list()
        for item in items:
            dirfullname = q.system.fs.joinPaths(path, item)
            if dirfullname.startswith("./"):
                dirfullname = dirfullname[2:]
            data = dict()
            data["state"] = "closed" if isdir else "leaf"
            data["data"] = {"children": [],
                            "title": item,
                            "attr":{"href": "#", "onclick":"nodeClicked('" + dirfullname + "');return false"}
                           }
            data["attr"] = { "class":"TreeTitle", "id":dirfullname }
            result.append(data)
        return result
    
    #This function make sure the path doesn't try to access parent items like appname/../../../../etc/
    def checkPath(self, path):
        if path.startswith("..") or path.startswith("/"):
            return False
        if path.find("/..") > 0:
            return False
        return True
    
    @q.manage.applicationserver.expose
    def listPyApps(self, jobguid = "", executionparams = None):
        """        
        list all available applications

        @execution_method = sync

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 list of application names
        @rtype:                  list
        """
        currentapp = p.api.appname
        applist = q.system.fs.listDirsInDir(q.dirs.pyAppsDir, dirNameOnly=True)
        #I want to make current app the first in the list
        idx = applist.index(currentapp)
        if idx > 0:
            applist[idx], applist[0] = applist[0], applist[idx]
        return applist
    
    @q.manage.applicationserver.expose
    def listSpaces(self, appname, jobguid = "", executionparams = None):
        """        
        list all available spaces

        @execution_method = sync

        @param appname:   name of the application
        @type appname:    string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 list of space names
        @rtype:                  list
        """
        if not self.checkPath(appname):
            return None
        return q.system.fs.listDirsInDir(q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, "portal/spaces/"), dirNameOnly=True)
    
    @q.manage.applicationserver.expose
    def listFilesInDir(self, appname, id = ".", jobguid = "", executionparams = None):
        """        
        list all files in a specific directory
        
        @execution_method = sync
        
        @param appname:   name of the application
        @type appname:    string
        
        @param dirname:   name of the direcotry relative to the application path
        @type dirname:    string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:                 list of files in the directory "dirname"
        @rtype:                  list
        """
        dirname = id
        if not self.checkPath(appname) or not self.checkPath(dirname):
            raise ValueError("invalid characters in the application name or path (.. or /) were detected")
        
        path = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, dirname)
        lenpath = len(path)
        result = list(item[lenpath + 1:] for item in q.system.fs.listFilesInDir(path))
        return self.list2jstree(appname, dirname, result, False)
    
    @q.manage.applicationserver.expose
    def listDirsInDir(self, appname, id = ".", jobguid = "", executionparams = None):
        """        
        list all directories in a specific directory
        
        @execution_method = sync
        
        @param appname:   name of the application
        @type appname:    string
        
        @param dirname:   name of the direcotry relative to the application path
        @type dirname:    string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:          list of directories in the directory "dirname"
        @rtype:           list
        """
        dirname = id
        if not self.checkPath(appname) or not self.checkPath(dirname):
            raise ValueError("invalid characters in the application name or path (.. or /) were detected")
        path = q.system.fs.joinPaths(q.dirs.pyAppsDir, appname, dirname)
        result = q.system.fs.listDirsInDir(path, dirNameOnly=True)
        return self.list2jstree(appname, dirname, result, True)
    
    @q.manage.applicationserver.expose
    def importDir(self, appname, space, dirname, jobguid = "", executionparams = None):
        """
        Import directory "dirname" located in the directory of application "appname" into space "space"
        
        @execution_method = sync
        
        @param appname:   name of the application
        @type appname:    string
        
        @param space:   name of the space
        @type space:    string

        @param dirname:   name of the direcotry relative to the application path
        @type dirname:    string

        @param jobguid:          guid of the job if available else empty string
        @type jobguid:           guid

        @param executionparams:  dictionary of job specific params e.g. userErrormsg, maxduration ...
        @type executionparams:   dictionary
        
        @return:          list of directories in the directory "dirname"
        @rtype:           list
        """
        dest = q.system.fs.joinPaths(appname, "portal/spaces/", space)
        if not self.checkPath(dest) or not self.checkPath(dirname):
            raise ValueError("invalid characters in the application name, space or dirname (.. or initial /) were detected")
        dest = q.system.fs.joinPaths(q.dirs.pyAppsDir, path)
        src = q.system.fs.joinPaths(q.dirs.pyAppsDir, dirname)
        
        return True
