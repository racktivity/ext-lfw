import os 
import re

def main (q,i,p,params,tags):
    from alkira.sync_md_to_lfw import sync_to_alkira
    sync_to_alkira(params['appname'])

