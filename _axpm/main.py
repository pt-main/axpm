from .tool import Tool
import sys












class PacketManagerError(Exception):pass











class Main(Tool):
    def __init__(self):
        super().__init__()
        self._name = 'main'

    def work(self, argv: str):
        done = ' '.join(argv[1:])
        self.execute(done) # executing commands


def work():
    tool = Main()  
    tool.work(sys.argv)