__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    rootobject = params['rootobject']
    values = {'name': rootobject.name,
              'tags': rootobject.tags,
              'repository': rootobject.repository.url,
              'repo_username': rootobject.repository.username,
              'order': rootobject.order}

    osis.viewSave(params['domain'], params['rootobjecttype'], params['rootobjecttype'], rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'space' and params['domain'] =='ui'
