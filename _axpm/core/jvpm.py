from .basics.abstr import abstract_executable
from .java import basicinst

class Java (abstract_executable):
    def __init__(self):
        super().__init__()
        self._name = 'java'
        self.commands = {
            'install':{'commnd': self.install, "min_args": -1},
            'ins':"install",
            'help':{'commnd': self.help, "min_args": -1},
            '-h':'help',
        }
    
    def install(self, *args):
        basicinst(args[0] if args else "25")
    
    def help(self, *args):
        text = \
'''install (ins) : multiplatform java instalation
help (-h) : show help message'''
        self.out.output(
            self.out.text_to_frame(text)
        )