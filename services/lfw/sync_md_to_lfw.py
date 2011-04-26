#!/usr/bin/python
from pylabs import q, p
import optparse
import os, re
import functools

def sync_to_alkira(appname, path=None):
    from pylabs import p, q
    MD_PATH = ''
    if not path:
        MD_PATH = q.system.fs.joinPaths(q.dirs.baseDir, 'pyapps', options.appname, 'portal', 'spaces')
    else:
        MD_PATH = path
    serverapi = p.application.getAPI(appname,context=q.enumerators.AppContext.APPSERVER)
    connection = p.application.getAPI(appname).action
    macros_homepage = None
    
    for folder in q.system.fs.listDirsInDir(MD_PATH):
        files = q.system.fs.listFilesInDir(folder, filter='*.md', recursive=True)
        space = folder.split(os.sep)[-1]
    
        for f in files:
            name = q.system.fs.getBaseName(f).split('.')[0]
            content = q.system.fs.fileGetContents(f)
    
            # Check if page exists
            #f = connection.ui.page.getFilterObject()
            #f.add('ui_view_page_list', 'name', name, True)
            #f.add('ui_view_page_list', 'space', space, True)
            page_info = connection.ui.page.find(name=name, space=space, exact_properties=("name", "space"))
            if len(page_info['result']) > 1:
                raise ValueError('Multiple pages found ? ' )
            elif len(page_info['result']) == 1:
                page = connection.ui.page.getObject(page_info['result'][0])
                save_f = functools.partial( connection.ui.page.update, page.guid )
            else:
                page = serverapi.model.ui.page.new()
                page.name = name
                page.space = space
                page.category = 'portal'
                save_f = connection.ui.page.create
    
            if name.startswith('Macro') and name not in ['Macros_Home', 'Macros']:
                if not macros_homepage:
                    #check if Macros_Home page is already created, then get its guid to set it as parent guid to other macro pages
                    macros_page_info = connection.ui.page.find( name = 'Macros_Home', space = space ) 
                    if len(macros_page_info ['result'] ) == 1:
                        macros_homepage = connection.ui.page.getObject(macros_page_info['result'][0])
                page.parent = macros_homepage.guid if macros_homepage else None
    
            # content
            page.content = content if content else 'empty'
    
            # tags
            if page.tags:
                t = page.tags.split(' ')
            else:
                t = []
            tags = set(t)
    
            # page and space 
            tags.add('space:%s' % space)
            tags.add('page:%s' % name)
    
            # split CamelCase in tags
            for tag in re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', name).strip().split(' '):
                tags.add(tag)
    
            p.tags = ' '.join(tags)
            save_f (page.name, page.space, page.category, page.parent, page.tags, page.content)


if __name__ == "__main__":

    from pylabs.InitBase import q, p
    sync_parser = optparse.OptionParser()

    sync_parser.add_option('--path', '-p', dest='path', help='The path to the Markdown files you want to sync.')
    sync_parser.add_option('--appname', '-n', dest='appname', help='The name of the application for which you want to sync files.')

    (options, args) = sync_parser.parse_args()

    if not options.appname:
        q.errorconditionhandler.raiseError('Application name must be given.')

    sync_to_alkira(options.appname, options.path)

