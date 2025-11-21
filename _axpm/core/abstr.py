import os, abc, json as serializer
from .output import OutputSystem


debug = False

def print_debug(*args, sep = ' '):
    if debug: print(*args, sep=sep)


class abstract_executable(abc.ABC):
    def __init__(self):
        super().__init__()
        self.home_path = os.path.expanduser('~')
        self.config_path = self.home_path + '/'
        self.config_name = 'pm_config.json'
        self.out: OutputSystem = OutputSystem()
        self._name = 'abstr'

    @property
    def data(self):
        return {
            'out.state': self.out.state
        }

    def save(self):
        data = self.data
        path = os.getcwd()
        os.chdir(self.config_path)
        try:
            with open(self.config_name, 'w', encoding='utf-8') as file:
                serializer.dump(data, file, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
        os.chdir(path)
    
    def load(self):
        path = os.getcwd()
        os.chdir(self.config_path)
        try:
            with open(self.config_name, 'r', encoding='utf-8') as file: 
                data = serializer.load(file)
            self._load(data)
        except FileNotFoundError:
            print("Config file not found, creating default...")
            self.save()
        except serializer.JSONDecodeError as e:
            print(f"Error reading config file: {e}")
        except Exception as e:
            print(f"Error loading config: {e}")
        os.chdir(path)
    
    def _load(self, data):
        self.out.state = data['out.state']
    
    def execute(self, argv: str, *args):
        try:
            print_debug('--- ARGS', argv)
            self.load()
            spl = argv.split(' ') + list(args)
            command = spl[0] # parse command
            args = spl[1:] # parse arguments
            print_debug(self._name)
            print_debug(f'begin === {args} [{argv}]')
            if command in list(self.commands.keys()): # continue if command exist
                try: 
                    print_debug('start === ')
                    def exec(cmnd: dict, args):
                        args = [] if args == [''] else args
                        print_debug(f'args === [{args}]')
                        print_debug('exec started ===')
                        if cmnd['min_args'] > len(args): 
                            print_debug('exec started === 2')
                            required = f' ( {cmnd["args"]} )' if 'args' in cmnd.keys() else ''
                            self.out.output(f"'{command}' command requires at least one argument{required}.", self.out.color('yellow'))
                            return
                        print_debug(f'command execution [{command}]')
                        cmnd['commnd'](*args) # trying to execute command
                    cmnd = self.commands[command]
                    print_debug('exec === ', cmnd)
                    if isinstance(cmnd, dict):
                        print_debug('exec === dict')
                        exec(cmnd, args)
                    else:
                        cmnd = self.commands[cmnd]
                        print_debug('exec === alias', cmnd)
                        exec(cmnd, args)
                    self.save() # save if succes
                    print_debug(f'END === {args}, {command}')
                except Exception as e: 
                    self.out.warning('error')
                    self.out.output(f'Execution command error: [\n    {e}\n    {e.args}]', self.out.color('bright_red'))
            else:
                self.out.warning('Unknown command')
                command = self.out.colored(command, self.out.color('bright_red'))
                print(f'Unknown command [{command}]. Type [{self.out.colored("-h", self.out.color("blue"))}] for help.')
        except KeyboardInterrupt:
            self.out.warning('Exiting...')
            quit()
        except Exception as e:
            self.out.notification(['Unknown error.', e], self.out.color('bright_red'))
        finally:
            if debug: self.out(self.out.colored(f'All done in {self._name}...', self.out['green']))
    
    def parse(self, args: list, pattern: list, defaults: dict = None):
        if defaults is None: defaults = []
        if not isinstance(args, (list, tuple)): 
            raise ValueError('Args must be list or tuple')
        args = list(args)
        res = {}
        pattern_noname_parsed = []
        i: str
        for i in args:
            if i.startswith('--'):
                spl = i[2:].split(':')
                if len(spl) > 1:
                    res[spl[0]] = ':'.join(spl[1:])
                else:
                    res[spl[0]] = None
            else:
                for local_i in pattern:
                    if local_i.startswith('$'):
                        if local_i not in pattern_noname_parsed:
                            arg = local_i[1:]
                            pattern_noname_parsed.append(local_i)
                            break
                        else: arg = args.index(i); break
                res[arg] = i
        result = {}
        for i in res.keys():
            result[i] = defaults[i] if res[i] == None and i in defaults.keys() else res[i]
        for i in defaults.keys():
            if i not in result.keys():
                result[i] = defaults[i]
        return result