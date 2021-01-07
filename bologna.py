import argparse

class Error:
    def __init__(self, line_no, text):
        self.line_no = line_no
        self.text = text

    def __str__(self):
        return 'Line ' + str(self.line_no) + ': ' + self.text

    def __lt__(self, other):
        return self.line_no < other.line_no

def check_errors(program):
    errors = []
    labels = set()
    names = set()
    for line_no in range(len(program)):
        line = program[line_no]
        if len(line) == 0:
            # Ignore empty lines
            continue
        if line[0] == '#label':
            if len(line) != 2 or line[1].isnumeric():
                errors.append(Error(line_no+1, 'Incorrect label syntax.'))
                continue
            if line[1] in labels:
                errors.append(Error(line_no+1, 'Label ' + line[1] + ' is already defined.'))
            else:
                labels.add(line[1])
        elif line[0] == '#name':
            if len(line) != 3 or line[2].isnumeric():
                errors.append(Error(line_no+1, 'Incorrect name syntax.'))
                continue
            if line[2] in names:
                errors.append(Error(line_no+1, 'Name ' + line[2] + ' is already defined.'))
            else:
                names.add(line[2])
    for line_no in range(len(program)):
        line = program[line_no]
        if len(line) == 0 or line[0] == '#':
            # Ignore empty lines and comments
            continue
        if line[0] == '#label' or line[0] == '#name':
            # preprocessor commands have already been checked
            continue
        elif line[0] == 'bz':
            if len(line) != 2:
                errors.append(Error(line_no+1, 'Incorrect bz syntax.'))
                continue
            if not line[1].isnumeric() and line[1] not in labels:
                errors.append(Error(line_no+1, 'Label ' + line[1] + ' not found.'))
        elif (line[0] == 'incr' or line[0] == 'decr'):
            if len(line) != 2:
                errors.append(Error(line_no+1, 'Incorrect ' + line[0] + ' syntax.'))
                continue
            if not line[1].isnumeric() and line[1] not in names:
                errors.append(Error(line_no+1, 'Name ' + line[1] + ' not found.'))
        else:
            errors.append(Error(line_no+1, 'Unrecognized instruction or preprocessor command.'))
    return sorted(errors)

def preprocess(program):
    labels = {}
    names = {}
    instructions = []
    errors = check_errors(program)
    if len(errors) != 0:
        for error in errors:
            print(error)
        print('Program cannot be ran.')
        quit()
    for line in program:
        if line[0] == '#label':
            labels[line[1]] = len(instructions)
        elif line[0] == '#name':
            names[line[2]] = line[1]
        else:
            instructions.append(line)
    for instr in instructions:
        if instr[0] == 'bz' and not instr[1].isnumeric():
            instr[1] = str(labels[instr[1]])
        elif (instr[0] == 'incr' or instr[0] == 'decr') and not instr[1].isnumeric():
            instr[1] = names[instr[1]]
    return instructions

def execute(instructions):
    mem = {}
    memSize = 0
    last = 0
    pc = 0
    while pc < len(instructions):
        line = instructions[pc]
        inst = line[0]
        arg = int(line[1])
        if inst == 'incr':
            if not arg in mem:
                mem[arg] = 0
                memSize = max(arg+1, memSize)
            mem[arg] += 1
            last = mem[arg]
        elif inst == 'decr':
            if not arg in mem:
                mem[arg] = 0
                memSize = max(arg+1, memSize)
            mem[arg] -= 1
            last = mem[arg]
        elif inst == 'bz':
            if last == 0:
                pc = arg - 1
        pc += 1
    memArray = [ 0 if not addr in mem else mem[addr] for addr in range(memSize) ]
    return memArray

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('file', help='Bologna file')
    argparser.add_argument('-p', '--preprocessor', help='print the preprocessor output and quit', action='store_true')
    args = argparser.parse_args()
    filename = args.file
    with open(filename) as progfile:
        program = [ line.strip().split() for line in progfile.read().strip().lower().split('\n') ]
        instructions = preprocess(program)
        if args.preprocessor:
            for instr in instructions:
                print(instr[0] + ' ' + instr[1])
            quit()
        endState = execute(instructions)
        print(endState)
