# Nim language

### Why Nim:
- Fully Compiled - No VM - All major platforms - High performance
- Deterministic memory management (unlike Java, like C++, Rust), with move semantics.
- Compiles to C like (C, C++, ObjC), Javascript
- Its Pythonic! (if you appreciate beauty in code)
- Mature package manager `nimble`
- Metaprogramming using a macro system to allow manipulation of AST (DSL galore!)
- Cross platform Native UI (using `libui`)
- `karax` - React/Vue like SPA framework using nim
- Easy interop with C FFI (multiple packages to support)

# Installation

```bash
$ curl https://nim-lang.org/choosenim/init.sh -sSf | sh
$ cat "export PATH=/Users/devendrarane/.nimble/bin:$PATH" >> ~/.zshrc
$ source ~/.zshrc
$ choosenim stable
```

# Basics

```nim
# hello.nim
echo "Hello world!"
```

**Build**

`$ nim c hello.nim`


**Run**

`$ ./hello`


**Build and Run**

`$ nim c -r hello.nim`


More options:

```sh
# No verbosity
$ nim c -r --verbosity:0 hello.nim

# Higher verbosity
$ nim c -r --verbosity:2 hello.nim
```


