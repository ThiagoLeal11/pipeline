file = open('exemplo_1.txt', 'r+')

# Pipeline stages constants
FETCH_INSTRUCTION = 0
DECODE_INSTRUCTION = 1
CALC_OPERANDS = 2
FETCH_OPERANDS = 3
EXECUTE_INSTRUCTION = 4
WRITE_OPERANDS = 5


class Instructions:
    instructions = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    @staticmethod
    def new_instruction(instruction, args):

        # Return the instruction object.
        return {'instruction': instruction, 'args': args}

    def read_instruction(self, line):
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


def execute(command):
    if command['instruction'] == 'jmp':  # Unconditional jump
        return command['args'][0]

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

    def add_command(self, command):
        self.pipeline.append(Command(command))

    def exec_pipeline(self):
        response = None

        # Iterate over pipeline commands and change her states
        for c in self.pipeline:

            # Just go to the next step.
            if c.get_stage() < EXECUTE_INSTRUCTION:
                c.print()
                c.next_stage()

            # Execute the command
            elif c.get_stage() == EXECUTE_INSTRUCTION:
                response = execute(c.get_command())
                print('response: ', response)
                c.print()
                c.next_stage()

            # Command end, remove them.
            else:
                c.print()
                self.pipeline.pop(0)

        print('-'*15)

        return response

    def clean_pipeline(self):
        # Remove any command that not execute yet
        for l in range(FETCH_INSTRUCTION, WRITE_OPERANDS):
            self.pipeline.pop(1)


class Interpreter:

    def __init__(self, code):
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

        tag = self.pipeline.exec_pipeline()

        if tag is None:
            self.line += 1

        # Jump for the tag
        else:
            # Clean the pipeline
            self.pipeline.clean_pipeline()

            # Go to the new line
            self.line = self.tags.get_line(tag)
            print('new line', self.line)


# Some test code
i = Interpreter(file.read())
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
