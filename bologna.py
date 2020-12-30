import argparse

def preprocess(program):
    labels = {}
    names = {}
    instructions = []
    lines = [ line.strip().lower().split() for line in program.split('\n') ]
    for line in lines:
        if line[0] == '#label':
            if line[1] in labels:
                print('Label already exists: ' + line[1])
                quit()
            labels[line[1]] = len(instructions)
        elif line[0] == '#name':
            if line[2] in names:
                print('Name already exists: ' + line[1])
                quit()
            names[line[2]] = line[1]
        else:
            instructions.append(line)
    for instr in instructions:
        if instr[0] == 'bz' and not instr[1].isnumeric():
            if instr[1] in labels:
                instr[1] = str(labels[instr[1]])
            else:
                print('Unrecognized label: ' + instr[1])
                quit()
        elif (instr[0] == 'incr' or instr[0] == 'decr') and not instr[1].isnumeric():
            if instr[1] in names:
                instr[1] = names[instr[1]]
            else:
                print('Unrecognized name: ' + instr[1])
                quit()
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
        else:
            print('Unknown instruction: ' + inst)
            quit()
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
        program = progfile.read().strip()
        instructions = preprocess(program)
        if args.preprocessor:
            for instr in instructions:
                print(instr[0] + ' ' + instr[1])
            quit()
        endState = execute(instructions)
        print(endState)
