__author__ = "incubaid"

def main(q, i, p, params, tags):
    macroPath  = q.dirs.baseDir + "www/lfw/js/macros/"
    macros = q.system.fs.listFilesInDir(macroPath, filter="*.js")
    pyappMacrosPath = q.system.fs.joinPaths(q.dirs.pyAppsDir, p.api.appname, "impl", "portal", "jsmacros")
    macros.extend(q.system.fs.listFilesInDir(pyappMacrosPath, filter="*.js"))

    result = []
    for i in xrange(0, len(macros)):
        macroFile = macros[i]

        macro = { "name": q.system.fs.getBaseName(macroFile).split(".")[0] }

        f = open(macroFile)
        for line in f:
            if line.startswith("//@metadata"):
                line = line.replace("//@metadata", "")
                metaList = line.split("=")

                header = metaList[0].strip()
                value = metaList[1].strip()
                macro[header] = value
            else:
                break
        f.close()

        result.append(macro)

    params['result'] = sorted(result, key=lambda macro: macro["name"])
