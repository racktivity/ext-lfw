#!/usr/bin/python
from pylabs import q, p
import optparse
import os, re
import functools

def sync_to_alkira(appname, path=None, sync_space=None, clean_up=False):
    from pylabs import p, q
    
    def deletePages(alkira, sync_space):
            pages = alkira.pageFind(space=sync_space)
            for page in pages:
                alkira.deletePageByGUID(page)
    def pageDuplicate(page):
        page_name = q.system.fs.getBaseName(page)
        if page_name in page_occured:
            q.errorconditionhandler.raiseError("Another page with the name '%s' already exists on this space. Will NOT create/update the following page (%s)"%(page_name, page))
        else:
            page_occured.append(page_name)

    def filterContent(page_content):
        content_dict = {}
        page_lines = page_content.splitlines()
        while page_lines[0].startswith('@metadata'):
            meta_line = page_lines.pop(0)
            meta_line = meta_line.replace('@metadata', "")
            meta_list = meta_line.split('=')

            header = meta_list[0].strip()
            value = meta_list[1].strip()

            content_dict[header] = value

        filtered_content = "\n".join(page_lines)
        content_dict['content'] = filtered_content

        return content_dict

    def createPage(alkira, page_file, parent=None):
        pageDuplicate(page_file)
        name = q.system.fs.getBaseName(page_file).split('.')[0]
        content = q.system.fs.fileGetContents(page_file)
        page_info = alkira.pageFind(name=name, space=spaceguid, exact_properties=("name", "space"))
        
        if len(page_info) > 1:
            raise ValueError('Multiple pages found!')
        elif len(page_info) == 1:
            save_page = functools.partial(alkira.updatePage, spaceguid, name)
            q.console.echo('Updating page: %s'%name, indent=4)
        else:
            save_page = alkira.createPage
            q.console.echo('Creating page: %s'%name, indent=3, withStar=True)
            
        # Setting content and metadata
        page_content_dict = filterContent(content)
        content = page_content_dict.get('content', 'Page is empty.')
        title = page_content_dict.get('title', name)
        order = int(page_content_dict.get('order', '10000'))

        # Creating and setting tags
        tags = page_content_dict.get('tagstring', "").split(" ")
        tags = set(tags)
        tags.add('space:%s' % space)
        tags.add('page:%s' % name)
        
        if name == "Home":
            tags.add('spaceorder:%s' % page_content_dict.get('spaceorder',1000))
        
        for tag in re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', name).strip().split(' '):
            tags.add(tag)
        
        save_page(space=space, name=name, content=content, order=order, title=title, tagsList=tags, category='portal', parent=parent)
        
    def alkiraTree(alkira, folder_paths, root_parent=None):
        for folder_path in folder_paths:
            folder_name = q.system.fs.getBaseName(folder_path).split('.')[0]
            parent_name = folder_name + '.md' 
            parent_path = q.system.fs.joinPaths(folder_path, parent_name)

            if not q.system.fs.exists(parent_path):
                q.errorconditionhandler.raiseError('The directory "%s" does not have a page "%s" specified for it.'%(folder_path, parent_name))

            if root_parent:
                createPage(alkira, parent_path, parent=root_parent)
            else:
                createPage(alkira, parent_path)

            children_files = q.system.fs.listFilesInDir(folder_path, filter='*.md')
            for child_file in children_files:
                if child_file != parent_path:
                    createPage(alkira, child_file, parent=folder_name)

            sub_folders = q.system.fs.listDirsInDir(folder_path)
            if sub_folders:
                alkiraTree(alkira, sub_folders, root_parent=folder_name)

    alkira = q.clients.alkira.getClient("localhost", appname)
    md_path = ''
    if not path:
        md_path = q.system.fs.joinPaths(q.dirs.baseDir, 'pyapps', appname, 'portal', 'spaces')
    else:
        md_path = path
        
    if clean_up:
        deletePages(alkira, sync_space)
        
    if sync_space:
        space_dir = q.system.fs.joinPaths(md_path, sync_space)
        if not q.system.fs.exists(space_dir):
            q.errorconditionhandler.raiseError('Space "%s" does not exist.'%sync_space)
        portal_spaces = [space_dir]
    else:
        portal_spaces = q.system.fs.listDirsInDir(md_path)

    #make the first space is the Admin Space
    portal_spaces = sorted(portal_spaces, lambda x,y: -1 if x.endswith("/Admin") else 1)
    
    for folder in portal_spaces:
        space = folder.split(os.sep)[-1]
        spaceguid = None
        if space not in alkira.listSpaces():
            #create space
            alkira.createSpace(space)
        
        spaceguid = alkira.getSpace(space).guid
            
        q.console.echo('Syncing space: %s' % space)
        
        page_occured = []
        
        
        folder_paths = q.system.fs.listDirsInDir(folder)
        main_files = q.system.fs.listFilesInDir(folder, filter='*.md')

        for each_file in main_files:
            createPage(alkira, each_file)
            
        alkiraTree(alkira, folder_paths)

if __name__ == "__main__":

    from pylabs.InitBase import q, p
    sync_parser = optparse.OptionParser()

    sync_parser.add_option('--path', '-p', dest='path', help='The path to the Markdown files you want to sync.')
    sync_parser.add_option('--appname', '-n', dest='appname', help='The name of the application for which you want to sync files.')
    sync_parser.add_option('--space', '-s', default=None, dest='space', help='The name of the space for which you want to sync files.')

    (options, args) = sync_parser.parse_args()

    if not options.appname:
        q.errorconditionhandler.raiseError('Application name must be given.')

    sync_to_alkira(options.appname, options.path, options.space)

