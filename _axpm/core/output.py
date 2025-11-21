from .basics.interface import *











class OutputSystem:
    def __init__(self):
        self.state = {}
        self.state['colors'] =  True

    def output(self, text: str, *colors, end: str = '\n', flush: bool = False):
        text = str(text)
        print(self.colored(text, *colors) if colors else text, end=end, flush=flush)
        return self
    
    def colored(self, text: str, *colors):
        return color.set(str(text), *colors) if self.state['colors'] else text
    
    def color(self, color_name: str):
        if color_name:
            if ';' in color_name or '\n' in color_name: 
                raise ValueError(f'You can only select color. Your input code:\n   {color_name}')
            return eval(f'color.{color_name.upper()}', globals(), globals())
    
    def warning(self, text, color = 'red'):
        add = str(text).center(21, ' ')
        text = f'''
┌─────────────────────┐
│       WARNING:      │
│{add}│
└─────────────────────┘'''
        self.output(text, [self.color(i) for i in color] if isinstance(color, (list, tuple)) else self.color(color))

    def notification(self, text, color: list['str'] | str = 'green'):
        def parse(text):
            max = Utils.maxlen(text) + 6
            up = f'┌{"─" * max}┐'
            lines = []
            for i in text:
                lines += ['│' + str(i).center(max) + '│']
            lines = '\n'.join(lines)
            down = f'└{"─" * max}┘'
            text = f'''{up}\n{lines}\n{down}'''
            return text
        if isinstance(text, str):
            text = parse(text.split('\n'))
        elif isinstance(text, (list, tuple)):
            text = parse(text)
        else: self.notification('Unkwnown type of text to create notification.', 'red')
        if isinstance(color, list): 
            colors = []
            if color:
                for i in color: color.append(self.color(i))
        else: 
            colors = self.color(color)
        self.output(text, colors if color else None)
    
    def text_to_frame(self, text):
        if isinstance(text, (list, tuple)): pass
        elif isinstance(text, str): text = text.split('\n')
        else: self.notification('Unkwnown type of text to create framized text.', 'red')
        max_ln = Utils.maxlen(text) + 2
        res = [f'┌{"─" * max_ln}┐']
        max_ln -= 2
        for i in text:
            res += ['│ ' + i + (' ' * (max_ln-len(i))) + ' │']
        res += [f'└{"─" * (max_ln + 2)}┘']
        return '\n'.join(res)
    
    def __getitem__(self, name):
        return self.color(name)
    
    def __call__(self, text: str, *colors, end: str = '\n', flush: bool = False):
        self.output(text, *colors, end=end, flush=flush)
        return self