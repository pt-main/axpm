import time, os, platform

def iterator(iter = [0]):
    iter += [iter[-1] + 1]
    iter = iter[-1]
    return iter

class Utils:
    @staticmethod
    def maxlen(data):
        out = []
        for i in data:
            out.append(len(str(i)))
        return max(out)
    @staticmethod
    def cls():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

class Iteratable:
    def __init__(self, frames: list):
        self.frames = frames
        self.state = 0

    def animate(self):
        index = self.state
        res = self.frames[index if index < len(self.frames) else -1]
        self.state += 1
        return res
    
    def __call__(self, *args, **kwds):
        return self.animate()

class Animations:
    def download_simple_1():
        return ["[    ]", "[=   ]", "[==  ]", "[=== ]", "[ ===]", "[  ==]", "[   =]", "[    ]"]
    def loading_simple_1(operations = 10, length = 10):
        frames = []
        full_at_once = length / operations
        for i in range(1, operations):
            done = (i * full_at_once)
            if done > length: 
                full = round(length - full / i)
            else: full = round(done)
            frames.append('[' + '=' * full + ' ' * (length - full) + ']')
        frames.append('[' + '=' * length + ']')
        return frames
    def loading_better_1(operations = 10, length = 10):
        frames = []
        full_at_once = length / (operations - (1/operations))
        frames.append('0% - 100% [' + ' ' * length + ']')
        for i in range(1, operations):
            done = (i * full_at_once)
            if done > length: 
                full = round(length - full / i)
            else: full = round(done)
            pr = min(round(full / length * 100), 100)
            pr_str = '0' + str(pr) if pr < 10 else str(pr)
            pr2 = 100 - pr
            pr2_str = '0' + str(pr2) if pr2 < 10 else str(pr2)
            procents = f'{pr_str if pr != 0 else 0}% - {pr2_str if pr2 != 0 else 0}%'
            frames.append(procents + ' [' + '=' * full + ' ' * (length - full) + f']')
        frames.append('100% - 0% [' + '=' * length + ']')
        return frames

class Table:
    def __init__(self, size1, size2, data1, data2):
        self.size = [size1+2, size2+2, max(len(data1), len(data2))]
        self.data = [data1, data2]
        self.interface = {}
    
    def create(self, return_b :bool=True):
        self.interface[0] = f'╔{"═" * (self.size[0] + self.size[1] + 1)}╗'
        o = 0
        for i in range(self.size[2]):
            try: 
                text = self.data[1][o]
                length = len(text)
                oth = ' ' * (self.size[1] - length)
            except: text, oth = ' ' * (self.size[1] - 0), ''
            try:
                text1 = self.data[0][o]
                length = len(text1)
                oth1 = ' ' * (self.size[0] - length)
            except: text1, oth1 = ' ' * (self.size[0] - 0), ''
            str = f"║{text1}{oth1}│{text}{oth}║"
            self.interface[i+3]=str
            o += 1
        self.interface[-1] = f'╚{"═" * (self.size[0] + self.size[1] + 1)}╝'
        if return_b:return self.interface
    
    def out(self):
        for i in self.interface:
            print(self.interface[i])

    def set(self, column, line, data):
        self.data[column][line] = data



class color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def set(text, *col):
        data = col if isinstance(col, list) else [col]
        if isinstance(col, tuple):
            nd = []
            for i in col: nd.append(i)
            data = nd
        return f"{' '.join(data)}{text}{color.RESET}"



def download(packets: list, seconds = 0, load_length = 30):
    # will be in pm (packet manager) class
    packets = packets + ['DONE']
    length = map(lambda string: len(string), packets)
    maxlen = max(list(length))
    packets = list(map(lambda string: str(string).center(maxlen, ' '), packets))
    process = len(packets) - 1
    animation = Animations.loading_simple_1(process, load_length)
    animator = Iteratable(animation)
    def anime():
        print(' '*maxlen, end='\r')
        return color.set(str(animator()), color.GREEN)
    def work(i):
        packet = color.set(str(packets[i]), color.BLUE)
        i = i if i != (len(packets) - 1) else " "
        print('\r <--- ' + anime(), end = f' --- [ {str(i).center(4, " ")} | {packet} ] --->\r')
    for i in range(0, process):
        work(i)
        time.sleep(seconds/process)
    work(i + 1)
    print('\n')



def animate_logo():
    frames = ['•', '*', '<>', '<->', '<---->', '<--=-->', '<--xp-->', '<--xpm-->', '<--axpm-->', '-- axpm --', '-  axpm  -'
            ] + (['   axpm    '
            ] * 10) + ['   axpm  ', '>  axpm ', ' > axpm ', '  >axpm', '   >xpm', '   a>pm ', '   ax>m ' , '   axp> ', '   axpm> ', 
            '    axp  ', '     ax ', '      a '] + ['  ' * 10] * 10

    animator = Iteratable(frames)
    for i in range(len(frames)):
        print('\r', animator.animate(), end = '')
        time.sleep(0.07)