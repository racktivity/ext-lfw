__author__ = "racktivity"
__tags__ = 'macro', 'generic'

def main(q, i, params, tags):

    result = """
# Demo Generic

This content is _generated_ in a *tasklet*

-----
    """
    params['result'] = result 

def match(q, i, params, tags):

    return 'demo' in params['tags'].labels
