import argparse

def preprocess(program):
    labels = {}
    instructions = []
    lines = [ line.strip().lower().split() for line in program.split('\n') ]
    for line in lines:
        if line[0] == '#label':
            labels[line[1]] = len(instructions)
        else:
            instructions.append(line)
    for instr in instructions:
        if instr[0] == 'bz' and not instr[1].isnumeric():
            if instr[1] in labels:
                instr[1] = str(labels[instr[1]])
            else:
                print('Unrecognized label: ' + instr[1])
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
    argparser.add_argument('file')
    args = argparser.parse_args()
    filename = args.file
    with open(filename) as progfile:
        program = progfile.read().strip()
        instructions = preprocess(program)
        endState = execute(instructions)
        print(endState)
