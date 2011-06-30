__author__ = "incubaid"

def main(q, i, p, params, tags):
    macros = q.system.fs.listFilesInDir(q.dirs.baseDir + "www/lfw/js/macros", filter="*.js")
    for i in xrange(0, len(macros)):
        macro = macros[i]
        macros[i] = q.system.fs.getBaseName(macro).split(".")[0]
    params['result'] = macros
