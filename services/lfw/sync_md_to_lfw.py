#!/usr/bin/python
from pylabs import q, p
import optparse
from . import Alkira

## NOTE ##
#This file is kept only for backward compatibility, and
#will be delete when no other components is using it

def sync_to_alkira(appname, path=None, sync_space=None, sync_page=None, clean_up=False):
    api = p.application.getAPI(appname, context=q.enumerators.AppContext.APPSERVER)
    alkira = Alkira(api)
    alkira.syncPortal(path, space=sync_space, page=sync_page, cleanup=clean_up)

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

