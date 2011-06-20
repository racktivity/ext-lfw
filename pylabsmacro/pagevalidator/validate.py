__author__ = "incubaid"
#!/usr/bin/env python
from pylabs.InitBaseCore import q
import re
linkRe = re.compile("/[a-zA-Z0-9]*/#/[a-zA-Z0-9/]*")
macroRe = re.compile("\[\[([a-zA-Z0-9 =]+)\]\]")

def macroExists(macro, space):
    if q.system.fs.isFile("/opt/qbase5/www/lfw/js/macros/%s.js"%macro):
        return True
    if q.system.fs.isDir("/opt/qbase5/lib/python/site-packages/alkira/tasklets/pylabsmacro/%s/"%macro):
        return True
    return q.system.fs.isFile("/opt/qbase5/pyapps/%s/impl/portal/jsmacros/%s.js"%(space, macro))

def linkExists(link, client):
    linkparts = link.split("/", 4)[1:]
    if len(linkparts) == 4:
        appname, hashmark, space, page = linkparts
    elif len(linkparts) == 3:
        appname, hashmark, space = linkparts
        page = "Home"
    else:
        raise Exception("Page %s is invalid "%link)
    return client.pageExists(space, page)

def getLinks(body):
    return linkRe.findall(body)

def getMacros(body):
    return macroRe.findall(body)

def getPageReport(client, space, name, recursive = False, showValid = True):
    result = list()
    page = client.getPage(space, name)
    #Check links
    links = getLinks(page.content)
    for link in links:
        ok = linkExists(link, client)
        if ok and not showValid:
            continue
        result.append((space + "/" + page.name, "link", link, ok))

    #Check Macros
    macros = getMacros(page.content)
    for macro in macros:
        ok = macroExists(macro, space)
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
