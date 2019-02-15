file = open('exemplo_2.txt', 'r+')

# Pipeline stages constants
FETCH_INSTRUCTION = 0
DECODE_INSTRUCTION = 1
CALC_OPERANDS = 2
FETCH_OPERANDS = 3
EXECUTE_INSTRUCTION = 4
WRITE_OPERANDS = 5

class Register:
    def __init__(self, esp):
        self.registers = {'ebp': 0, 'eax': 0, 'temp': 0, 'temp2': 0, 'esp': esp}

    def get_value(self, register):
        return self.registers[register]

    def movl(self, register1, register2):
        if register2.isdigit():
            self.registers[register1] = register2
        else:
            self.registers[register1] = self.registers[register2]

    def addl(self, register1, register2):
        if register2.isdigit():
            self.registers[register1] += int(register2)
        else:
            self.registers[register1] = int(self.registers[register1]) + int(self.registers[register2])

    def incl(self, register):
        self.registers[register] = int(self.registers[register]) + 1

    def print_register(self):
        for x in self.registers:
            print('%7s' % x, end='')
        print()
        for x in self.registers:
            print('%7s' % self.registers.get(x), end='')
        print()


class Instructions:
    instructions = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    @staticmethod
    def new_instruction(instruction, args):

        # Return the instruction object.
        return {'instruction': instruction, 'args': args}

    def read_instruction(self, line):
        # Remove comments
        line = line.split('//')[0]
        # Clean the str.
        line = line.replace('\t', ' ')
        line = line.replace(',', ' ')
        # Get a list of commands.
        line = line.split()

        # Get the instruction object.
        instruction = self.new_instruction(line[0], line[1:])

        # Save instruction on list.
        self.add_instruction(instruction)

    def get_instruction(self, index):
        return self.instructions[index]

    def get_len(self):
        return len(self.instructions)




def execute(command, registers):
    if command['instruction'] == 'jmp':  # Unconditional jump
        return command['args'][0]
    elif command['instruction'] == 'movl':
        registers.movl(command['args'][0], command['args'][1])
        return None
    elif command['instruction'] == 'addl':
        registers.addl(command['args'][0], command['args'][1])
        return None
    elif command['instruction'] == 'incl':
        registers.incl(command['args'][0])
        return None

    return None


class Tags:
    tags = []

    def add_tag(self, tag, line):
        self.tags.append(self.new_tag(tag, line))

    def print_tags(self):
        print(self.tags)

    @staticmethod
    def new_tag(tag, line):
        # Clean the tag.
        tag = tag.replace(':', '')
        tag = tag.replace('\t', '')
        tag = tag.replace(' ', '')

        # Return the tag object.
        return {'tag': tag, 'line': line}

    def get_line(self, tag):
        for t in self.tags:
            if t['tag'] == tag:
                return t['line']

        return None


class Command:
    def __init__(self, command):
        self.command = {'command': command, 'stage': 0}

    def get_stage(self):
        return self.command['stage']

    def get_command(self):
        return self.command['command']

    def next_stage(self):
        self.command['stage'] += 1

    def print(self):
        print(self.command)


class Pipeline:
    def __init__(self):
        self.pipeline = []
        self.matrix = []
        self.matrix.append([])
        self.matrix[0].append('FI')
        self.matrix[0].append('DI')
        self.matrix[0].append('CO')
        self.matrix[0].append('FO')
        self.matrix[0].append('EI')
        self.matrix[0].append('WO')

    def print_pipeline(self):
        for x in self.matrix:
            for y in x:
                print('%7s' % y, end='')
            print()

    def add_print(self, stage, command):
        self.matrix[-1][stage] = command

    def add_command(self, command):
        self.pipeline.append(Command(command))

    def exec_pipeline(self, registers):
        response = None

        self.matrix.append([])
        for x in range(0,6):
            self.matrix[-1].append('')

        # Iterate over pipeline commands and change her states
        for c in self.pipeline:

            # Just go to the next step.
            if c.get_stage() < EXECUTE_INSTRUCTION:
                # c.print()
                self.add_print(c.get_stage(), c.get_command()['instruction'])
                c.next_stage()

            # Execute the command
            elif c.get_stage() == EXECUTE_INSTRUCTION:
                response = execute(c.get_command(), registers)
                self.add_print(c.get_stage(), c.get_command()['instruction'])
                print('response: ', response)
                c.next_stage()

            # Command end, remove them.
            else:
                self.add_print(c.get_stage(), c.get_command()['instruction'])
                self.pipeline.pop(0)

        self.print_pipeline()

        return response

    def clean_pipeline(self):
        # Remove any command that not execute yet
        for l in range(FETCH_INSTRUCTION, WRITE_OPERANDS):
            self.pipeline.pop(1)


class Interpreter:

    def __init__(self, code, esp):
        self.registers = Register(esp)
        self.code = code.split('\n')
        self.instructions = Instructions()
        self.pipeline = Pipeline()
        self.tags = Tags()
        self.line = 0
        self.max_line = 0

    def parse_code(self):

        # Parse all the lines and store in the vectors.
        for line in self.code:
            self.parse_line(line)

        # Store the last line.
        self.max_line = self.line
        # Reset the line counter.
        self.line = 0

    def parse_line(self, line):
        # Read the instruction from the string.
        if line[0] == '\t' or line[0] == ' ':
            self.instructions.read_instruction(line)
            self.line += 1
            pass

        # Read the tag from the string.
        else:
            self.tags.add_tag(line, self.line)

    def run_cycle(self):
        # Add new instruction to pipeline
        if self.line < self.max_line:
            self.pipeline.add_command(self.instructions.get_instruction(self.line))

        tag = self.pipeline.exec_pipeline(self.registers)
        print()
        print('-' * 42)
        self.registers.print_register()
        print('-' * 42)
        print('\n')

        if tag is None:
            self.line += 1

        # Jump for the tag
        else:
            # Clean the pipeline
            self.pipeline.clean_pipeline()

            # Go to the new line
            self.line = self.tags.get_line(tag)
            print('new line', self.line)


esp = int(input("Enter a value to esp: "))

# Some test code
i = Interpreter(file.read(), esp)



i.parse_code()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()
i.run_cycle()