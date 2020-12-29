# Bologna
An ISA with three simple instructions: `incr`, `decr`, and `bz`. See some example programs in the `examples` folder.

## Overview
There are three instructions: `incr`, `decr`, and `bz`.

`incr N`: increment the value at memory address `N` by `1`

`decr N`: decrement the value at memory address `N` by `1`

`bz N`: if the result of the last `incr`/`decr` instruction was `0`, jump to instruction `N` (instructions are 0-indexed)

## Executing programs
`python bologna.py [filename]`
