import os
import re

def main (q,i,p,params,tags):
    from alkira.sync_md_to_lfw import sync_to_alkira
    sync_to_alkira(params['appname'])

    # Change the ownership of the space management pages on disk:
    spacesDir = q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, 'portal/spaces/Admin/Settings/Spaces')
    if q.system.fs.isDir(spacesDir):
        config = q.config.getConfig('main').get('main', {})
        user = config.get('user')
        group = config.get('group')
        if user and group:
            q.system.unix.chown(spacesDir, user, group, recursive=True)
