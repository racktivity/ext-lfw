__author__ = "incubaid"

import time
from alkira.alkira import getOsisViewsMap

def main(q, i, p, params, tags): #pylint: disable=W0613
    osisViewsMap = getOsisViewsMap()
    pageTable = osisViewsMap['page']['table']
    spaceTable = osisViewsMap['space']['table']
    MAXTIME = 50
    start = time.time()
    macro_tags = params['tags'].tags
    alk = params['service'].alkira

    space = macro_tags['space']
    pagename = macro_tags['page']
    updatetime = float(macro_tags['updatetime'])
    query = """select page.guid
               from %(pageTable)s as page
               join %(spaceTable)s as space on page.space = space.guid
               where space.name = %(space)s and page.name = %(pageName)s;
               """ % {'space': space, 'pageName': pagename, 'pageTable' : pageTable, 'spaceTable' : spaceTable}

    result = alk.connection.page.query(query)
    if result:
        pageguid = result[0]['guid']
        while time.time() < start + MAXTIME:
            page = alk.connection.page.get(pageguid)
            if not page.creationdate:
                break
            newtime = float(page.creationdate)
            if newtime > updatetime:
                updatetime = newtime
                break
            time.sleep(1)
    params['result'] = updatetime
