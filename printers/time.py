import time

class TimeTPrinter:
    def __init__(self, val):
        self.val = val
        self.type = gdb.lookup_type ("int")

    def to_string(self):
        value = str(time.ctime(int(self.val.cast(self.type))))
        return str(self.val.cast(self.type))+" ("+value+")"

def lookup_type (val):
    if str(val.type) == 'time_t':
        return TimeTPrinter(val)
    return None

gdb.pretty_printers.append (lookup_type)
