def main(q, i, p, params, tags):
    import pygraphviz as pgv
    import base64
    import StringIO
    graphDot_str = params['graphDot_str']

    graphDot_str = graphDot_str.replace("&gt;", ">")
    G = pgv.AGraph(string=graphDot_str)
    G.layout(prog='dot')
    rawimage = StringIO.StringIO()
    G.draw(rawimage, 'gif')
    rawimage.buf = ''
    img_b64 = base64.b64encode(rawimage.getvalue())
    params['result'] = img_b64

