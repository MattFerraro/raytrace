

def dump(system, fp):
	string = dumps(system)
	fp.write(string)

def dumps(system):
    output = "Prescription:\n"
    elements = ["    " + str(x) for x in system]
    output += "\n".join(elements)
    return output



def loads(string):
    print string
