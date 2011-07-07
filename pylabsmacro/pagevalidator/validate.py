__author__ = "incubaid"
import re
from pylabs import q
linkRe = re.compile('<a +href *= *"([^"]*)"')
macroRe = re.compile("\[\[([a-zA-Z0-9 =]+)\]\]")

JSMACROS_GPATH = q.system.fs.joinPaths(q.dirs.baseDir, "www", "lfw", "js", "macros")
JSMACROS_LPATH = q.system.fs.joinPaths(q.dirs.pyAppsDir, "%s", "impl", "portal", "jsmacros")
PYMACROS_GPATH = q.system.fs.joinPaths(q.dirs.baseDir, "lib", "python", "site-packages", "alkira", "tasklets", "pylabsmacro")

def macroExists(macro, appname):
    join = q.system.fs.joinPaths
    if  q.system.fs.isFile(join(JSMACROS_GPATH, "%s.js"%macro)):
        return True
    if q.system.fs.isDir(join(PYMACROS_GPATH, macro)):
        return True
    return q.system.fs.isFile(JSMACROS_LPATH%appname, "%s.js"%macro)

def linkExists(link, client):
    external = ["http://", "https://", "ftp://", "ftps://"]
    for pre in external:
        if link.startswith(pre):
            return "external"
    
    linkparts = link.split("/", 4)[1:]
    if len(linkparts) == 4:
        appname, hashmark, space, page = linkparts
    elif len(linkparts) == 3:
        appname, hashmark, space = linkparts
        page = "Home"
    else:
        raise Exception("Page %s is invalid "%link)
    if appname != p.api.appname: 
        client = q.clients.alkira.getClient("localhost", appname)
    return "valid" if client.pageExists(space, page) else "invalid"
    

def getLinks(body):
    return linkRe.findall(body)

def getMacros(body):
    return macroRe.findall(body)

def getPageReport(client, space, name, recursive = False, showValid = True):
    import markdown
    
    result = list()
    page = client.getPage(space, name)
    body = markdown.markdown(page.content)
    #Check links
    links = getLinks(body)
    for link in links:
        result = linkExists(link, client)
        if result in ("valid", "unknown") and not showValid:
            continue
        result.append((space + "/" + page.name, "link", link, result))

    #Check Macros
    macros = getMacros(page.content)
    for macro in macros:
        ok = macroExists(macro, appname)
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
               "[%s](%s)"%(item[2], item[2]),
                "OK" if item[3] else "INVALID"
            )
        elif item[1] == "macro":
            html += row%(
                "[%s](%s)"%(parenturl, parenturl),
                "[[%s]]"%(item[2]),
                "OK" if item[3] else "INVALID"
            )
    html += "</TABLE>"
    params['result'] = "%s"%html
