
def parse_variable_tree(frame):
    block = frame.block()

    variables  = {}
    attributes = {}
    parameters = {}
    globalVars = {} #TODO

    # For c++, also get the current object attributes
    thisVar = None

    while block:
        for symbol in block:
            name = symbol.name

            if symbol.is_variable:

                #TODO implement filter objects
                # Noisy metadata for unsupported Qt types are useless
                if name.find("qt_meta_") != -1:
                    continue

                # Relevant info from this are in pretty printed already
                if name.find("staticMetaObject") != -1:
                    continue

                if not name in variables:
                    variables[name] = symbol.value(frame)

            elif symbol.is_argument and symbol.name == "this":
                thisVar = symbol
            elif symbol.is_argument:
                parameters[name] = symbol.value(frame)
        block = block.superblock

    if thisVar != None:
        t = thisVar.type.unqualified().target()
        obj = thisVar.value(frame).referenced_value()
        fields = t.fields()
        for field in fields:
            try:
                attributes[field.name] = obj[field.name]
            except:
                #TODO add <optimized>
                pass

    return {
        'variables'  : variables,
        'attributes' : attributes,
        'parameters' : parameters,
        'globalVars' : globalVars
    }


def print_variables_from_frame(frame, name, value):
    buf = box_first_line()
    buf += box_last_line()

    tp = value.type

    vis = gdb.default_visualizer(value)

    gdb.write(buf)

class BetterPrinter (gdb.Command):
    """Print a more useful backtrace"""

    def __init__ (self):
        super (BetterPrinter, self).__init__ ("p", gdb.COMMAND_USER)

    def invoke (self, arg, from_tty):
        if arg == None or arg == "":
            return

        f = gdb.selected_frame()

        if not f:
            return

        val = f.read_var(arg)

        if val == None:
            return

        content = parse_variable_tree(f)

        print_variables_from_frame(f, arg, val)

BetterPrinter ()
