__author__ = "incubaid"

def main(q, i, params, tags):

    t = params.get('tags')

    labels_list = list()
    for l in t.labels:
        labels_list.append("*    %s\n"%l)
    labels = ''.join(labels_list)

    tags_list = list()
    for k, v in t.tags.iteritems():
        tags_list.append('*    %s = %s\n' % (k, v))
    tags = ''.join(tags_list)

    result = """
#### Tags
%(tags)s

#### Labels
%(labels)s
""" % {'tags': tags, 'labels': labels}

    params['result'] = result

def match(q, i, params, tags):
    return 'debug' in params['tags'].labels
