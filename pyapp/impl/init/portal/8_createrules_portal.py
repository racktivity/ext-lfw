def main(q, i, p, params, tags):
    from alkira import Alkira
    api = p.application.getAPI(params["appname"], context=q.enumerators.AppContext.APPSERVER)
    alk = Alkira(api)
    alk.createDefaultRules()
