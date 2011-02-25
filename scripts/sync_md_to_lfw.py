#!/opt/qbase3/bin/python
from pymonkey.InitBase import q

import os, re
import osis
from osis.client import OsisConnection
from osis.client.xmlrpc import XMLRPCTransport
from osis.model.serializers import ThriftSerializer

osis.init(q.system.fs.joinPaths(q.dirs.baseDir, 'libexec', 'osis'))
transport = XMLRPCTransport('http://127.0.0.1/appserver/xmlrpc/', 'osis_service')
serializer = ThriftSerializer()
connection = OsisConnection(transport, serializer)

MD_PATH = q.system.fs.joinPaths(q.dirs.tmpDir, 'lfw', '1.0', 'docs')

for folder in q.system.fs.listDirsInDir(MD_PATH):
    files = q.system.fs.listFilesInDir(folder, filter='*.md')
    space = folder.split(os.sep)[-1]

    for f in files:
        name = q.system.fs.getBaseName(f).split('.')[0]
        content = q.system.fs.fileGetContents(f)

        # Check if page exists
        f = connection.page.getFilterObject()
        f.add('view_page_list', 'name', name)
        f.add('view_page_list', 'space', space)
        page_info = connection.page.findAsView(f, 'view_page_list')

        if len(page_info) > 1:
            raise ValueError('Multiple pages found ?')

        elif len(page_info) == 1:
            p = connection.page.get(page_info[0]['guid'])
        else:
            p = connection.page.new()
            p.name = name 
            p.space = space
            p.category = 'portal'

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
