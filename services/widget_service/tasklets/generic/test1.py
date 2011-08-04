def main(q, i, params, tags):

    t = params.get('tags')

    labels = ''.join(['*    %s\n' % l for l in t.labels])
    tags = ''.join(['*    %s = %s\n' % (k, v) for k, v in t.tags.iteritems()])

    result = """
#### Tags
%(tags)s

#### Labels
%(labels)s
""" % {'tags': tags, 'labels': labels}

    params['result'] = result

def match(q, i, params, tags):

    return 'debug' in params['tags'].labels
