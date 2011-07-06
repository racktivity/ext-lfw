def main(q, i, p, params, tags):
    import sqlalchemy
    from sqlalchemy import MetaData, Table, create_engine
    from sqlalchemy.orm import sessionmaker
    import math
    import re

    sqlselect = params['sqlselect']
    rows = params['rows']
    table = params['table']
    schema = params['schema']
    dbconnection = params.get('dbconnection', '')
    link = params.get('link', '')
    _search = params.get('_search', '')
    nd = params.get('nd', '')
    page = params.get('page', 1)
    sidx = params.get('sidx', '')
    sord = params.get('sord', '')
    applicationserver_request = params.get('applicationserver_request', '')
    service = params['service']

    localdb = False
    cfgfilepath = service.db_config_path
    q.logger.log('FILE IS %s' % cfgfilepath, 1)
    if q.system.fs.exists(cfgfilepath):
        inifile = q.tools.inifile.open(cfgfilepath)
        section = 'db_%s' % dbconnection
        if inifile.checkSection(section):
            dbserver = inifile.getValue(section, 'dbserver')
            dblogin = inifile.getValue(section, 'dblogin')
            dbpassword = inifile.getValue(section, 'dbpasswd')
            dbname = inifile.getValue(section, 'dbname')
        else:
            localdb = True
    else:
        localdb = True
    if localdb:
        dbname = 'sampleapp'
        dbserver = '127.0.0.1'
        dblogin = q.manage.postgresql8.cmdb.rootLogin
        dbpassword = q.manage.postgresql8.cmdb.rootPasswd

    start = (int(page) - 1) * int(rows)
    pagefields = list()

    #sqlalchemy stuff
    engine = create_engine('postgresql://%s:%s@%s/%s' % (dblogin, dbpassword, dbserver, dbname))
    connection = engine.connect()

    comp = re.compile(".*from(?P<end>.*)", re.I)
    countquery = comp.sub("select count(*) as count from \g<end>", sqlselect)
    if sidx:
        sqlselect += " ORDER BY %s %s" % (sidx, sord)
    sqlselect += ' LIMIT %s OFFSET %s' % (rows, start)

    t = engine.text(countquery)
    totalrowcount = t.execute().fetchone()[0]
    t = engine.text(sqlselect)
    output = t.execute()
    result = output.fetchall()

    data = dict()
    data['columns'] = output.keys()
    data['page'] = page
    data['total'] = int(math.ceil(totalrowcount/float(rows)))
    data['records'] = rows
    data['rows'] = list()

    for index, pageobj in enumerate(result):
        data['rows'].append({'id': index + 1, 'cell': list(pageobj)})
    params['result'] = data
