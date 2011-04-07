#!/opt/qbase3/bin/python
from pylabs.InitBase import q

import os, re
import osis
from osis.client import OsisConnection
from osis.client.xmlrpc import XMLRPCTransport
import pymodel
from pymodel.serializers import ThriftSerializer

pymodel.init_domain('/opt/qbase5/pyapps/sampleapp/interface/model')
osis.init()

transport = XMLRPCTransport('http://127.0.0.1/sampleapp/appserver/xmlrpc/', 'model')
serializer = ThriftSerializer()
connection = OsisConnection(transport, serializer)
#MD_PATH = q.system.fs.joinPaths(q.dirs.varDir, 'qpackages4', 'files', 'pylabs.org', 'lfw', '1.0', 'generic', 'docs')
MD_PATH = '/opt/qbase5/pyapps/sampleapp/portal/doc/'

macros_homepage = None

for folder in q.system.fs.listDirsInDir(MD_PATH):
    files = q.system.fs.listFilesInDir(folder, filter='*.md', recursive=True)
    space = folder.split(os.sep)[-1]

    for f in files:
        name = q.system.fs.getBaseName(f).split('.')[0]
        content = q.system.fs.fileGetContents(f)

        # Check if page exists
        f = connection.ui.page.getFilterObject()
        f.add('ui_view_page_list', 'name', name, True)
        f.add('ui_view_page_list', 'space', space, True)
        page_info = connection.ui.page.findAsView(f, 'ui_view_page_list')

        if len(page_info) > 1:
            raise ValueError('Multiple pages found ?')

        elif len(page_info) == 1:
            p = connection.ui.page.get(page_info[0]['guid'])
        else:
            p = connection.ui.page.new()
            p.name = name 
            p.space = space
            p.category = 'portal'

        if name.startswith('Macro') and name not in ['Macros_Home', 'Macros']:
            if not macros_homepage:
                #check if Macros_Home page is already created, then get its guid to set it as parent guid to other macro pages
                filter = connection.ui.page.getFilterObject()
                filter.add('ui_view_page_list', 'name', 'Macros_Home', True)
                filter.add('ui_view_page_list', 'space', space, True)
                macros_page_info = connection.ui.page.findAsView(filter, 'ui_view_page_list')
                if len(macros_page_info) == 1:
                    macros_homepage = connection.ui.page.get(macros_page_info[0]['guid'])
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

        connection.ui.page.save(p)
