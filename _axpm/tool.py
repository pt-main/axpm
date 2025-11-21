from .core.abstr import abstract_executable
import sys, json as serializer, os, abc, time
from .core.pythpm import Python
from .core.basics.interface import Animations, Iteratable
from .core.ghpm import Github
from .core.basics.interface import animate_logo



version = '0.4.9-A'

    


class Tool(abstract_executable):
    def __init__(self):
        super().__init__()
        self.py = Python(self.out)
        self.gh = Github()
        self._name = 'tool'
        self.commands = {
            'python': {'commnd': self.py.execute, 'min_args': 1},
            'py': 'python',

            'github': {'commnd': self.gh.execute, 'min_args': 1},
            'gh': 'github',

            'pm': {'commnd': self.logo, 'min_args': -1},

            '-0c': {'commnd': self.no_color, 'min_args': 0},
            '-1c': {'commnd': self.all_color, 'min_args': 0},

            'help': {'commnd': self.help, 'min_args': 0},
            '-h': 'help',
            'version': {'commnd': self.version, 'min_args': 0},
            '-v': 'version',
            'about': {'commnd': self.hello, 'min_args': 0},
            'main': 'about',
            'info': 'about',
            
            'install': {'commnd': self.py.install, 'min_args': 1},
            '-i': 'install',
        }

    def version(self):
        self.out(version)
    
    def logo(self, *args): 
        animate_logo()

    def hello(self):
        ops = 90
        seconds = 0.5
        animator = Animations.loading_better_1(ops, 42)
        iterator = Iteratable(animator)
        for i in range(ops):
            print(f'\r{iterator()}', end='')
            time.sleep(seconds/ops)
        text = f'''\n
╔═════════════════════════════════════╦━─────────────╮
║  .d8b.  db    db d8888b. .88b  d88. ║ First alpha  │
║ d8' `8b `8b  d8' 88  `8D 88'YbdP`88 ║ pt-main/pm   │
║ 88ooo88  `8bd8'  88oodD' 88  88  88 ║ 2025         │
║ 88~~~88  .dPYb.  88~~~   88  88  88 ║              │
║ 88   88 .8P  Y8. 88      88  88  88 ║              │
║ YP   YP YP    YP 88      YP  YP  YP ║              │
╠═════════════════════════════════════╣ tool for     │
┃ Advanced X-platform Package Manager ┃ every        │
│          development by pt          │ developer    │
╰─────────────────────────────────────┴──────────────╯
'''
        length = len(text)
        exec_time = 1
        for i in str(text):
            self.out.output(text=i, end='', flush=True)
            time.sleep(exec_time/length)
        ver = f"Version: {self.out.colored(version, self.out.color('green'))}"
        self.out.output(ver)

        
    
    @property
    def help_comands(self):
        return f'''
╭──────────────────────────────────────────────────╮
│ ○ ○ ◉                                    ╔══════╗│
╰──────────────────────────────────────────╣ main ╠╯
┌──────────────┳───────────────────────────╩══════╩┐
│ help         ┃ show that message                 │
│ -h           ┃                                   │
├──────────────╋───────────────────────────────────┤
│ about        ┃ show welcome & about message      │
│ main         ┃                                   │
├──────────────╋───────────────────────────────────┤
│ -0c          ┃ turn on colors highlight          │
│ -1c          ┃ turn off colors highlight         │
├──────────────╋───────────────────────────────────┤
│ install      ┃ install python module             │
│ -i           ┃ with pip                          │
├──────────────╋───────────────────────────────────┤
│ python       ┃ access to Python                  │
│ --py         ┃                                   │
├──────────────╋───────────────────────────────────┤
│ github       ┃ acess to github                   │
│ --gh         ┃                                   │
└──────────────┻───────────────────────────────────┘
'''
        self.out.output(text)

    def help(self, *args):
        self.out.output(self.help_comands)
    
    def no_color(self, *args):
        self.out.state['colors'] = False
    
    def all_color(self, *args):
        self.out.state['colors'] = True