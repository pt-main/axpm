import sys, os, platform



class PyPm:
    def __init__(self):
        self.full_ver = sys.version
        spl = sys.version.split('.')
        self.ver = '.'.join(spl[:2]) + '.' + '.'.join(spl[2:3]).split(' ')[0]
        self._sys = platform.system()
        self.pyname = 'python' if not self._sys.startswith('Darwin') else 'python3'
    def py(self, command: str):
        return os.system(f'{self.pyname} {command}')
    def pym(self, command: str):
        return os.system(f'{self.pyname} -m {command}')
    def pip(self, command: str):
        return self.pym(f'pip {command}')
    def install(self, package):
        return self.pip(f'install {package}')
    