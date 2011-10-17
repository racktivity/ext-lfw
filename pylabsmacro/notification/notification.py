__author__ = "incubaid"


def main(q, i, p, params, tags):
    import time
    MAXTIME = 50
    start = time.time()
    macro_tags = params['tags'].tags
    alkira = params['service'].alkira

    space = macro_tags['space']
    pagename = macro_tags['page']
    updatetime = float(macro_tags['updatetime'])
    query = "select page.guid from ui_page.ui_view_page_list as page join ui_space.ui_view_space_list as space on page.space = space.guid where space.name = '%s' and page.name = '%s';" % (space, pagename)
    result = alkira.connection.page.query(query);
    if result:
        pageguid = result[0]['guid']
        while time.time() < start + MAXTIME:
            page = alkira.connection.page.get(pageguid)
            if not page.creationdate:
                break
            newtime = float(page.creationdate)
            if newtime > updatetime:
                updatetime = newtime
                break
            time.sleep(1)
    params['result'] = updatetime
