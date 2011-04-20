#!/usr/bin/python
from pylabs.InitBase import q, p

import optparse
import os, re

sync_parser = optparse.OptionParser()

sync_parser.add_option('--path', '-p', dest='path', help='The path to the Markdown files you want to sync.')
sync_parser.add_option('--appname', '-n', dest='appname', help='The name of the application for which you want to sync files.')

(options, args) = sync_parser.parse_args()

if not options.appname:
    q.errorconditionhandler.raiseError('Application name must be given.')

if options.path:
    MD_PATH = options.path
else:
    MD_PATH = q.system.fs.joinPaths(q.dirs.baseDir, 'pyapps', options.appname, 'portal', 'spaces')

api = p.application.getAPI(options.appname, context=q.enumerators.AppContext.APPSERVER)
connection = api.model.ui

macros_homepage = None

for folder in q.system.fs.listDirsInDir(MD_PATH):
    files = q.system.fs.listFilesInDir(folder, filter='*.md', recursive=True)
    space = folder.split(os.sep)[-1]

    for f in files:
        name = q.system.fs.getBaseName(f).split('.')[0]
        content = q.system.fs.fileGetContents(f)

        # Check if page exists
        f = connection.page.getFilterObject()
        f.add('ui_view_page_list', 'name', name, True)
        f.add('ui_view_page_list', 'space', space, True)
        page_info = connection.page.findAsView(f, 'ui_view_page_list')

        if len(page_info) > 1:
            raise ValueError('Multiple pages found ?')

        elif len(page_info) == 1:
            p = connection.page.get(page_info[0]['guid'])
        else:
            p = connection.page.new()
            p.name = name 
            p.space = space
            p.category = 'portal'

        if name.startswith('Macro') and name not in ['Macros_Home', 'Macros']:
            if not macros_homepage:
                #check if Macros_Home page is already created, then get its guid to set it as parent guid to other macro pages
                filter = connection.page.getFilterObject()
                filter.add('ui_view_page_list', 'name', 'Macros_Home', True)
                filter.add('ui_view_page_list', 'space', space, True)
                macros_page_info = connection.page.findAsView(filter, 'ui_view_page_list')
                if len(macros_page_info) == 1:
                    macros_homepage = connection.page.get(macros_page_info[0]['guid'])
            if macros_homepage:
                p.parent = macros_homepage.guid

        # content
        p.content = content if content else 'empty'

        # tags
        if p.tags:
            t = p.tags.split(' ')
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

        connection.page.save(p)
