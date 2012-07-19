__author__ = "incubaid"

#@TODO remove this macro or rework it in a decent way without sleep!

import time
import sqlalchemy

def main(q, i, p, params, tags): #pylint: disable=W0613
    MAXTIME = 50
    start = time.time()
    macro_tags = params['tags'].tags
    alk = params['service'].alkira

    spacename = macro_tags['space']
    pagename = macro_tags['page']
    updatetime = float(macro_tags['updatetime'])

    pageTable = alk.osis.findTable("ui", "page")
    spaceTable = alk.osis.findTable("ui", "space")

    join = [ pageTable.join(spaceTable, pageTable.c.space == spaceTable.c.guid) ]
    where = [ spaceTable.c.name == spacename, pageTable.c.name == pagename ]
    select = sqlalchemy.select([ pageTable.c.guid ], whereclause=sqlalchemy.and_(*where), from_obj=join)

    result = alk.osis.runSqlAlchemyQuery(select).fetch_one()
    if result:
        pageguid = result[0]
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
