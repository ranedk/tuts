# Pragmas

Pragmas are like `annotations` in Java. They give compiler extra information to act on. There are lots of `pragmas` and some are filling in for beta-features that may be implemented better in future.

## Pure Pragmas

These are hints to the compiler/linker with no semantic effects on the source code. A different compiler could decide to not support the pragma and give the same results. [noInit, requiresInit, deprecated, noReturn, acyclic, shallow...]
