from .basics.pypm import PyPm
from .basics.abstr import abstract_executable
import time, threading, os


class Python(abstract_executable):
    def __init__(self, Output):
        super().__init__()
        self.out = Output
        self._name = 'python'
        self.py = PyPm()
        self.commands = {
            'install': {'commnd': self.install, 'min_args': 1},
            '-i':'install',

            'parallel_install': {'commnd': self.install_parallel, 'min_args': 1},
            '-pi': 'parallel_install',

            'pip': {'commnd': self.pip, 'min_args': 1},

            'python': {'commnd': self.python, 'min_args': -1},
            '-s': 'python', # self
            '-self': 'python',

            'package':{'commnd': self.package, 'min_args': 1},

            'project':{'commnd': self.project, 'min_args': 1},

            'help': {'commnd': self.help, 'min_args': 0},
            '-h': 'help'
        }
    
    def install_module(self, module):
        self.out.output(f"=== [Installing '{module}' ...] ===", 
            self.out.color('yellow'),
            self.out.color('bold'))
        self.py.install(module)
        self.out.output(f"=== [Installing '{module}' succes...] ===", 
            self.out.color('CYAN'),
            self.out.color('bold'))
    
    def help(self):
        text = \
f'''PIP
    install (-i) : install python module with pip
    parallel_install (-pi) : parallel module instalation with pip 
    pip : work with pip

PYTHON
    python (-self) : work with python

FILES
    package : create folder with python package
        arg name : name of packeage
    project : create python project
        arg name : name of package
        arg license : license for project

OTHER
    help (-h) : show that message'''
        self.out.output(
            self.out.text_to_frame(text)
        )

    def install(self, *args):
        start = time.time()
        for module in args: self.install_module(module)
        self.out.output(f'=== [Installing done...] ===', 
                            self.out.color('green'),
                            self.out.color('bold'))
        end = time.time()
        self.out.notification(f'Instalation done. All modules installed by {round(end-start, 1)}s.', 'bright_green')

    def install_parallel(self, *args):
        start = time.time()
        threads: list['threading.Thread'] = []
        self._temp = 0
        def install_thread(module):
            self._temp += 1
            self.install_module(module)
            self._temp -= 1
        for module in args: 
            thr = threading.Thread(target=install_thread, args=[module])
            thr.start()
            threads += [thr]
        while self._temp > 1: time.sleep(0.5)
        for thr in threads: thr.join()
        self.out.output(f'=== [Installing done...] ===', 
                            self.out.color('green'),
                            self.out.color('bold'))
        end = time.time()
        self.out.notification(f'Instalation done. All modules installed by {round(end-start, 1)}s.', 'bright_green')


    def pip(self, *args):
        command = ' '.join(args)
        self.py.pip(command)

    def python(self, *args):
        command = ' '.join(args) if args else ''
        self.py.py(command)

    def package(self, *args):
        args = self.parse(args, 
                          ['$name', 'name'], 
                          {'name': 'package'})
        name = args['name']
        self.out.notification(
                    f'Starting to create python packacge {name}...',
                    'yellow'
                )
        if not os.path.exists(name):
            try:
                os.mkdir(name)
                self.out('Dir created...', self.out['green'])
                curr = os.getcwd()
                os.chdir(name)

                with open(f'__init__.py', 'w') as init:
                    init.write('# init file for pakage')
                self.out('Init file created...', self.out['green'])

                with open(f'main.py', 'w') as main:
                    main.write('# main file for package')
                self.out('Main file created...', self.out['green'])

                with open(f'package.md', 'w') as package:
                    package.write('# Package info and description')
                self.out('Package description file created...', self.out['green'])

                os.chdir(curr)
                self.out.notification(
                    f'Package {name} was created succesfuly.',
                    'bright_green'
                )
            except Exception as e:
                self.out(f'Error in package [{name}] create: \n    {e}', 'red')
                return
        else: 
            self.out.notification(
                f'Error in package create: Directory is already exist.', 
                'red'
            )
            return
    


    def project(self, *args):
        args = self.parse(args, 
                          ['$name', 'name', 'license'], 
                          {'name': 'project', 'license': 'mit'})
        license = str(args['license']).upper()
        name = str(args['name'])
        self.out.notification(
                    f'Starting to create python project.',
                    'yellow'
                )
        if not os.path.exists(name):
            try:
                os.mkdir(name)
                self.out('Project dir created...', self.out['green'])
                curr = os.getcwd()
                os.chdir(name)

                def file(name, content):
                    with open(name, 'w') as main:
                        main.write(content)
                    self.out(f'{name} file created...', self.out['green'])

                def pack(name):
                    os.mkdir(name)
                    with open(f'{name}/__init__.py', 'w') as main:
                        main.write(f'# init file for {name} package')
                    self.out(f'Init-{name} file created...', self.out['green'])
                
                file('README.md', f'# {name}')
                file('setup.py', '# setup project file \nfrom setuptools import setup, find_packages')
                file('LICENSE', f'license: {license}')
                
                pack('tests')
                pack('src')

                self.out.notification(
                    f'Project {name} was created succesfuly.',
                    'bright_green'
                )

                os.chdir(curr)
            except Exception as e:
                self.out(f'Error in project create', 'red')
                return
        else: 
            self.out.notification(
                f'Error in project create: Directory is already exist.', 
                'red'
            )
            return