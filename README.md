# Bologna
An ISA with three simple instructions: `incr`, `decr`, and `bz`. See some example programs in the `examples` folder.

## Overview
There are three instructions: `incr`, `decr`, and `bz`.

`incr N`: increment the value at memory address `N` by `1`

`decr N`: decrement the value at memory address `N` by `1`

`bz N`: if the result of the last `incr`/`decr` instruction was `0`, jump to instruction `N` (instructions are 0-indexed)

## Executing programs
`python bologna.py [filename]`

## Preprocessor
Bologna makes use of a preprocessor, which makes writing programs much easier.
The preprocessor currently supports labeling points in the program and naming
memory addresses. In the future, macros will be added to the preprocessor to
allow code reuse.

### Labels
Using labels means the programmer doesn't have to manually keep track of
instruction numbers when using the `bz` instruction. The line `#LABEL
SOME_LABEL` tells the preprocessor that the label `SOME_LABEL` should be
associated with the instruction number of the next instruction. Elsewhere in the
program, the line `bz SOME_LABEL` will jump to the instruction labeled by
`SOME_LABEL`. Labels can be referred to throughout the entire program, and
cannot be defined more than once.

### Names
Keeping track of what is stored at each memory location can get difficult, so
the preprocessor allows naming memory addresses. The line `#NAME 0 INPUT` maps
the name `INPUT` to memory address `0`. This name can later be used in `incr`
and `decr` instructions, so `incr INPUT` gets rewritten by the preprocessor as
`incr 0`. Names can be referred to from anywhere in the program (so you can use
names in instructions before defining the name), and a name cannot be defined
more than once. The same memory address can be referred to by multiple names,
but this should be avoided and is subject to change.
