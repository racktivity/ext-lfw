__author__ = "incubaid"
import re
from pylabs import q, p
linkRe = (re.compile('\[[^\]]*] *\( *([^ \)]*)'), re.compile('\[[^\]]*] *: *([^ \)"]*)'))
macroRe = re.compile("\[\[([a-zA-Z0-9 =]+)\]\]")

JSMACROS_GPATH = q.system.fs.joinPaths(q.dirs.baseDir, "www", "lfw", "js", "macros")
JSMACROS_LPATH = q.system.fs.joinPaths(q.dirs.pyAppsDir, "%s", "impl", "portal", "jsmacros")
PYMACROS_GPATH = q.system.fs.joinPaths(q.dirs.baseDir, "lib", "python", "site-packages", "alkira", "tasklets", "pylabsmacro")

def isExternalLink(linkparts):
    if linkparts[0] in ("ftp:", "ftps:"):
       return True
    if linkparts[0] in ("http:", "https:"):
        if linkparts[-1] == "#":
            return True
        return "#" not in linkparts
    return False

def macroExists(macro, appname):
    join = q.system.fs.joinPaths
    if  q.system.fs.isFile(join(JSMACROS_GPATH, "%s.js"%macro)):
        return True
    if q.system.fs.isDir(join(PYMACROS_GPATH, macro)):
        return True
    return q.system.fs.isFile(JSMACROS_LPATH%appname, "%s.js"%macro)

def linkExists(link, client, currentSpace):
    linkparts = link.split("/")
    if isExternalLink(linkparts):
        return "EXTERNAL"
    
    lenLink = len(linkparts)
    
    if linkparts[0] in ("http:", "https:"):
        #['http:', '', '0.0.0.0', 'test', '#', 'Admin', 'Home']
        if not (7 >= lenLink >= 6) or linkparts[4] != "#":
            return "INVALID"
        if lenLink == 7:
            appname, space, page = linkparts[3], linkparts[5], linkparts[6]
        else:
            appname, space, page = linkparts[3], linkparts[5], "Home"
        
    if linkparts[0] in ('', '.'):
        #['', 'test', '#', 'Admin', 'Home']
        if not (5 >= lenLink >= 4) or linkparts[2] != "#":
            return "INVALID"
        if lenLink == 5:
            appname, space, page = linkparts[1], linkparts[3], linkparts[4]
        else:
            appname, space, page = linkparts[1], linkparts[3], "Home"
    
    elif linkparts[0] == '#':
        #['#', 'Admin', 'Home']
        if not (3 >= lenLink >= 2):
            return "INVALID"
        appname = client.api.appname
        if lenLink == 3:
            space, page = linkparts[1:]
        else:
            space, page = linkparts[1], "Home"
    
    elif lenLink == 1:
        appname = client.api.appname
        space = currentSpace
        page = linkparts[0]
    else:
        return "INVALID"
    if appname != client.api.appname: 
        client = q.clients.alkira.getClient("localhost", appname)
    return "OK" if client.pageExists(space, page) else "MISSING"
    

def getLinks(body):
    result = list()
    for lre in linkRe:
        result += lre.findall(body)
    return result

def getMacros(body):
    return macroRe.findall(body)

def getPageReport(client, space, name, recursive = False, showValid = True):    
    result = list()
    page = client.getPage(space, name)
    #Check links
    links = getLinks(page.content)
    for link in links:
        state = linkExists(link, client, space)
        if result in ("OK", "EXTERNAL") and not showValid:
            continue
        result.append((space + "/" + page.name, "link", link, state))

    #Check Macros
    macros = getMacros(page.content)
    for macro in macros:
        ok = macroExists(macro, p.api.appname)
        if ok and not showValid:
            continue
        result.append((space + "/" + page.name, "macro", macro, ok))

    if recursive:
        for childpage in client.listChildPages(space, name):
            result += getPageReport(client, space, childpage, True)
    return result

def getInvalidLinks(appname, spaces = None, pages = None, showValid = True):
    result = list()
    client = q.clients.alkira.getClient("localhost", appname)
    if not spaces:
        spaces = client.listSpaces()
    
    for space in spaces:
        for page in client.listPages(space):
            if pages and (page not in pages):
                continue
            result += getPageReport(client, space, page, False, showValid = showValid)
    return result

def main(q, i, p, params, tags):
    tags = params["tags"].tags
    appname = p.api.appname
    client = q.clients.alkira.getClient("localhost", appname)
    #
    pages = spaces = None
    showValid = True
    if "pages" in tags:
        pages = list(item.strip() for item in tags["pages"].split(","))
    if "spaces" in tags:
        if tags["spaces"] == "*":
            spaces = client.listSpaces()
        else:
            spaces = list(item.strip() for item in tags["spaces"].split(","))
    if "showvalid" in tags:
		showValid = (tags["showvalid"].lower() == "true")
    #
    if pages or spaces:
        result = getInvalidLinks(appname, spaces, pages, showValid = showValid)
    else:
        result = getPageReport(client, tags["space"], tags["page"], True, showValid = showValid)
    html = "<TABLE><TR><TD>Page</TD><TD>URL</TD><TD>Status</TD></TR>\n"
    row = "<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TR>\n"
    for item in result:
        parenturl = "/%s/#/%s"%(appname, item[0])
        if item[1] == "link":
            html += row%(
                "[%s](%s)"%(parenturl, parenturl),
               "[%s](%s)"%(item[2], item[2]), item[3])
        elif item[1] == "macro":
            html += row%(
                "[%s](%s)"%(parenturl, parenturl),
                "[[%s]]"%(item[2]),
                "OK" if item[3] else "MISSING"
            )
    html += "</TABLE>"
    params['result'] = "%s"%html
