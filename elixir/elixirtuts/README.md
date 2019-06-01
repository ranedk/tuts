# Quick review of everything Elixir

# Installation
On ubuntu, do not do apt install. Instead,
```shell
$ wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
$ sudo dpkg -i erlang-solutions_1.0_all.deb

$ wget https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc
$ sudo apt-key add erlang_solutions.asc

$ sudo apt-get update
$ sudo apt-get install elixir erlang-dev erlang-parsetools erlang-observer
```

# BASICS

Functional language, awesome concurrency => multi-core and multi-machines
Bad with string manipulation
As good as php/python in general efficiency
In Elixir, when you call a function in a different module, you are actually sending values to a process

iex -> elixir interactive mode (like python repl ipython)

# iex basics:
```elixir
# help
> h(List.first)

# typeof
> i "hello"

# to run a external script named file.ex inside `iex`
> c("file.ex")
```

# Running standalong scripts
```bash
$ elixirc file.ex
```

# Function calls:
```elixir
length('hello rane') # -> 10
length 'hello rane'  # -> 10
```

# Basic types:
- nil
- integer, float
- atom/symbol
    - must start with colon e.g. :status or :code
    - used like named constants for status, state
- list e.g. [1, 2, 3, 4]
- tuple e.g. {1, 2, 3, 4}
- range 1..10
- regex ~r{regexp}opts  (PCRE, perl 5 compatible)
- Binary <<1, 2>>

Type check methods:
- `is_atom`
- `is_list`
- `is_tuple`
- `is_binary`
- `is_bitstring`

# Booleans (true/false/nil)
- apart from nil and false, everything else evaluates to true
- Are internally atoms(symbols)

```elixir
is boolean(false)   # -> true
is_atom(true)       # -> true
```

# List Elements

## Tuples:
```elixir
size {1, 2, 3}  # -> 2
```
- Stored as continous memory

- Fast for index access
```elixir
elem {1,2,3, :rane, {5,6}}, 4  ->  {5, 6}
```

- Updating tuple is expensive, requires copying the tuple in memory
```elixir
put_elem {1,2,3, :rane, {5,6}}, 3, 10  ->  {1, 2, 3, 10, {5, 6}}
```

- Good for fixed set of elements


## Lists:
```elixir
length [1, 2, 3]  # -> 3
```
- Stored as linked lists
- Updating is fast, accessing Nth element is slow
- Accessing first element is fast
- Most used general purpose list

```elixir
[head | tail ] = [1, 2, 3, 4, 5, 6, 7]
# ->  head = 1 and rest of it is tail
length [head | tail]  ->  6
# -> head should be a single element, tail must be a list

# Head and tail separation can be done after many elements too:
[first, second, third | tail ] = [1, 2, 3, 4, 5, 6, 7]
# -> first=1 second=2 third=3 tail=[4, 5, 6, 7]

[1, 2, 3, 4 | [5, 6, 7]]  # ->  [1,2,3,4,5,6,7]
```
- Enum and List module provides utilities for Enumerables (doesn't work on tuples)
```elixir
Enum.at [10, 20, 30], 0  ->  10
List.flatten [1, 2, [3, 4, [5, 6]], [7]]  ->  [1, 2, 3, 4, 5, 6, 7]
```

# Lookup elements

## Keyword Lists
Key-Value pairs (key is neccessarily an *atom* and *not unique*):
- List of Tuples with first element as an atom is represented as a Dict (python like lookup structure)

```elixir
d = [{:a, 1}, {:b, 2}]  ->  [a: 1, b: 2]
# -> The space after : is required here unlike python
# or
d = [a: 1, b: 2]  # equivalent to above
Keyword.get d, :b  -> 2
Keyword.get d, :c  -> nil
```

- If function takes Dict as last argument
```elixir
if 3 * 2 == 6, [do: "OK"]
```
- is same as
```elixir
if 3 * 2 == 6, do: "OK"
```
- Side note: which if you want to put brackets like other boring languages
```elixir
if(3 *2  == 6, [do: "OK"])
```
- Can be used when calling functions e.g.
```elixir
DB.save record, [ {:use_transaction, true}, {:logging, "HIGH"} ]
# OR
DB.save record, use_transaction: true, logging: "HIGH"
```
- These are multi-valued so
```elixir
l = [a: 1, b: 2, a: 3, a: 4]
Keyword.get_values l, :a   #-> [1, 3, 4]
```
- In operator
```elixir
{:a, 1} in [a: 1, b: 2]  #-> true
```

## Maps (key-value pairs) %{ key => value, key => value }

- Behave like normal python dictionaries (*unique keys*, all possible types)

```elixir
states = %{ "AL" => "Alabama", "WI" => "Wisconsin" }
states["AL"]
```

- In operator
```elixir
{"AL", "Alabama"} in states     # -> true
"AL" in states                  # -> true
```

- If keys are atoms:
```elixir
status = %{:success => 200, :not_found => 404}
# OR
status = %{success: 200, not_found: 404}

status[:success]    # -> 200
# OR
status.success      # -> 200
```

> NOTE: Use Keyword lists for parameters, command line options etc. If you need a data structure, use Map

# Strings (double quote):

```elixir
# String interpolation/templating:
name = "rane"
"Hello #{name}"

# String are bytes (supports unicode etc)
is_binary("hello")  -> true
byte_size("hello")  -> 5
byte_size("hellö") -> 6

is_bitstring("hello") -> true
bit_size("hello")  -> 40

# Binary representation of string "abc" is
"abc" == <<97, 98, 99>>  -> true
```

# Char "list" (single quotes)
```elixir
is_binary('rane')  # -> false
is_list('rane')    # -> true
length 'rane'      # -> 4
length 'hellö'     # -> 5

'abc' == [97, 98, 99]   # -> true
# Ascii integer value of letters using ?
?a  ==  97         # -> true
# So above can be written as
'abc' == [?a, ?b, ?c]  # -> true

# Also, by binary representation of strings concept
"abc" == <<?a, ?b, ?c>>
```
- Since these are printable characters, elixir does the conversion of [97, 98, 99] to 'abc' and <<97, 98, 99>> to "abc"
- this doesn't happen for non-printable ascii codes e.g. [97, 98, 99, 1] and <<97, 98, 99, 1>> have no equivalent string representations

> NOTE: Unless you want to iterate, do not use single quote strings

# String manipulation:

Elixir provides tons of string manipulation methods like:
-`capitalize`
-`at`
-`downcase`
-`codepoints` (split string into list of string)
-`duplicate` (repeat)
-`ends_with?`
-`first`
-`last`
-`length`
-`pad_leading`
-`pad_trailing`
-`replace`
-`reverse`
-`slice`
-`split`

# Sigils:
Use case:
- Textual representation
- Start with ~

## Regex sigils:
```elixir
regex = ~r/foo|bar/
"foo" =~ regex                # -> true
"bat" =~ regex                # -> false

"HELLO" =~ ~r/hello/i         # -> true   i is the regex modifier, like PCRE
```
- Sigils support multiple delimiters e.g.
```elixir
~r/hello/       # ->  /
~r|hello|       # ->  |
~r"hello"       # ->  "
~r'hello'       # ->  '
~r(hello)       # ->  ()
~r[hello]       # ->  []
~r{hello}       # ->  {}
~r<hello>       # ->  <>
```

```elixir
# String sigils
~s(this is a string with "double" quotes, not 'single' ones)
# -> "this is a string with \"double\" quotes, not 'single' ones"

# Character sigils
~c(this is a char list containing 'single quotes')
# -> 'this is a char list containing \'single quotes\''

# Word lists
~w(foo bar bat)
# -> default, without modifier ["foo", "bar", "bat"]

~w(foo bar bat)s
# -> with string modifier ["foo", "bar", "bat"]

~w(foo bar bat)c
# -> with character modifier  ['foo', 'bar', 'bat']

~w(foo bar bat)a
# -> with atom modifer [:foo, :bar, :bat]

~D[2019-03-25]          # Date object

~T[12:19:56.123]        # Time object

~N[2019-03-25 12:34:34.434]     # Raw Date time object
```

- Use cases

documentation:
```elixir
@doc ~S"""
Converts double-quotes to single-quotes.

## Examples

    iex> convert("\"foo\"")
    "'foo'"

"""
def convert(...)
```

# Functions:
## Anonymous functions:

```elixir
fn
    parameter-list -> body
    parameter-list -> body
    parameter-list -> body
end
```

```elixir
x = fn(a, b) -> a * b end
# OR (without parenthesis)
x = fn a,b -> a * b

x.(3, 2) == 6       # true, dot operator to call anonymous functions

swap = fn {a, b} -> {b, a} end
swap.({1, 10})      # ->  {10, 1}
```

# Operators:
- div for integer division
- rem for remainder
- \+  -  /  *

```elixir
# Union ++
[1, 2, 3] ++ [3, 4, 5]  # -> [1, 2, 3, 3, 4, 5]

# Set Substraction
[1, 2, 3, 4] -- [3, 4, 5, 6]  # -> [1, 2]

# In Operator (only on lists, not tuples)
1 in [1, 2, 3, 4]   # -> true

# String Concatenation
"Hello" <> " " <> "World"  # -> "Hello World"

# Pure Boolean (and or not)
true and true  # -> true
true and not true # -> false

# Strictly takes only booleans
1 and true
# ERROR -> ** (BadBooleanError) expected a boolean on left-side of "and", got: 1

1/0
# ERROR -> ** (ArithmeticError) bad argument in arithmetic expression :erlang./(1, 0)

false and 1/0       # -> false
# ->  Like python, if false, leave the other side of AND

true or 1/0         # -> true
# -> Like python, is true, leave the other side of OR
```

# Mixed Boolean (&& || !)

> NOTE: Everything is true except false and nil
```elixir
1 && 3 && 2     # ->  2
3 || 1/0        # -> 3
0 || 1/0        # -> 0
nil && 1/0      # -> nil

# nil and false are not the same
nil == false    # -> false
```
# Comparison `=, !=, ===, !==, <=, >=, < and >`
    - `===` is stict .. e.g. when comparing int and float
    - You can compare between different data types (which is weird, should never be done), but `number < atom < reference < functions < port < pid < tuple < list` (reference, port and pid are data types)
```elixir
{1} > 10           # ->  true
[100] > {5000}     # -> true
```

# Pattern matching:
- Too many things are accomplished using pattern matching e.g.

```elixir
[first | rest]  = [10, 20, 30, 40, 50]
{num, atom, str} = {10, :in_process, "rane"}
```
- lhs and rhs have to be of same type (list or tuple)
- number of parameters have to be same on both sides
- Interesting use is to match function output as :ok or :error e.g.

```elixir
{:ok, result} = {:ok, 3}
# -> when function given output

{:ok, result} = {:error, :bad_input}
# ->  when function given error
```
- String pattern matching
```elixir
[a, b, c] = "ran"
# -> a,b,c get ascii codes for 'r', 'a', 'n' respectively

<<a, b, c>> = 'ran'
# -> a,b,c get ascii codes for 'r', 'a', 'n' respectively
```
To get, first letter of a string:
```elixir
<<a:: integer, b:: binary>> = "rane is cool"
# ->  a is ?r and b is "ane is cool"
```

# Unicode:
- A string in Elixir is a binary which is encoded in UTF-8

```elixir
size "héllò"
# -> 7 - returns the number of bytes

> String.length "héllò"
# -> 5 - returns the number of characters as perceived by humans
```
> NOTE: Generally, `size` is to be used when length is pre-calculated, `length` is to be used when length is calculated at runtime

- To split string into list of strings
```elixir
String.codepoints "héllò"   # ->  ["h", "é", "l", "l", "ò"]

<< eacute :: utf8, rest :: binary >> = "épa"
# split head and tail

IO.puts eacute  # -> 233

IO.puts << eacute :: utf8 >>  # -> "é"
# Give utf8 encoded string representation

IO.puts rest    # -> "pa"
```

# Control blocks

## If block (if - do - else - end):

```elixir
if <condition> do
    <expression>
else
    <expression>
end
```

If case of confusion, just add brackets where needed

Different ways to frame if/else:

1)
```elixir
x = if x > 5 do
    5
else
    10
end
```

2)
```elixir
x = if x > 5, do: 5
```
3)
```elixir
x = if x > 5, do: 5, else: 10
```

## If-Unless-Do-Else

- unless is if-not (in other languages)
```elixir
x = if x > 5, do: 5  # make x 5 if its greater than 5

x = if x > 5, do: 5, else: x

x = unless x > 5, do: 5  # make x 5 if x is not greater than 5

x = unless x > 5, do: 5, else: x

# multi-line
if x > 5 do
    5
else
    x
end
```
## Switch-Case: (cond, do, true, end), break is implicit

```elixir
cond do
    x > 5 ->
        5
    x > 8 ->
        8
    x > 10 ->
        10
    true ->
        100
end
```

*Pattern matching:*
- "=" is not a assignment operator but a patten matching operator
```elixir
x = 1   ->  Match x to 1
^x = 1  ->  Match "value of x" to 1

# Pin x and match pattern
^x = 2  -> Gives MatchError, since value of x is not 2
```
- Basically, this acts as an assertion

> Note: Use underscore to ignore values (just like python)
> Note: If a variable is unused, elixir raises a Warning, which can be gotten rid of by starting the variable name with underscore
```elixir
[h | _] = [10, 20, 30, 40]
```

- The following code warns that head is not used
```elixir
def len([ head | tail ]), do: 1 + len(tail)

# We can fix it with underscore as
def len([ _head | tail ]), do: 1 + len(tail)
```
> Note: Function calls are not allowed on LHS of match

## Case:
- Works like switch case (break is implicit), but pattern matching makes assignments possible
- Different from cond (above), since cond does good-old boolean evaluation, case does pattern matching
```elixir
case { 1, 2, 3} do
{4, 5, 6} -> "This won't match
{ 1, x, 3} -> "This matches and x is assigned to 2"
_ -> "This matches all values"
end
```

### Case Guards: `when`, conditions that need to be met along with case
```elixir
case { 1, 2, 3 } do
    { 4, 5, 6 } -> "This won’t match"
    { 1, x, 3 } when x > 0 -> "This will match and assign x"
    _ -> "No match"
end

# Match errors to as case

case File.open("case.ex") do
    { :ok, file } -> IO.puts "First line: #{IO.read(file, :line)}"
    { :error, reason } -> IO.puts "Failed to open file: #{reason}"
end
```
- Guards can only have limited expressions (quite a lot are supported), https://hexdocs.pm/elixir/master/guards.html
#### Use case for Guards
    - *Polymorphism*
        ```elixir
        defmodule Exercise do
            def first_is_zero?(tuple_or_list) do
                if elem(tuple_or_list, 0) == 0 or hd(tuple_or_list) == 0 do
                true
            end

            def first_is_zero?(tuple_or_list) do
                false
            end
        end

        # This won't work since calling elem on list or hd on tuple raises exception

        defmodule Exercise do
            def first_is_zero?(tuple_or_list)
                when elem(tuple_or_list, 0) == 0 or hd(tuple_or_list) == 0 do
                true
            end

            def first_is_zero?(tuple_or_list) do
                false
            end
        end
        # This also won't work since when will evaluate both, and in case of error
        # make the whole statement false

        defmodule Exercise do
            def first_is_zero?(tuple_or_list) do
                when elem(tuple_or_list, 0) == 0
                when hd(tuple_or_list) == 0 do
                    true
                end
            end

            def first_is_zero?(tuple_or_list) do
                false
            end
        end

        # When used as Guards, errors are not raised
        # You should use multiple guards instead of OR conditions

        Tmp.first_is_zero?({0,1,2,3})           # -> true
        Tmp.first_is_zero?([0,1,2,3])           # -> true
        Tmp.first_is_zero?([11, 12, 13, 14])    # -> false
        ```

> NOTE: Guards should be used to put a validation/constraint on arguments.

> NOTE: Must not have complicated conditions or logic

> NOTE: Use guards to pass different types to a function (list, tuple, int) and derive different behavior

## Functions:

- Anonymous functions also behave as case statements
```elixir
f = fn
    x, y when x > 0 -> x + y
    x, y -> x * y
end
```
- Functions do not mutate variables outside function scope

## Send & Receive:
- In Elixir, you can spawn a process (erlang's light weight process) and using its PID to send and receive tasks to it

```elixir
# Get the current process id
current_pid = self
# Spawn another process that will send a message to current_pid
spawn fn ->
    send current_pid, { :hello, self }
end

# Collect the message
receive do
    { :hello, pid } ->
        IO.puts "Hello from #{inspect(pid)}"
    after
        1000 ->
        IO.puts "Waiting without message for last 1000 seconds"
end
```

# Try-Catch:
```elixir
try do
    throw 13
catch
    number -> number
end

# Try catch is generally not used. Also support guards and after

try do
    throw 13
catch
    nan when not is_number(nan) -> nan
after
    IO.puts "Didn’t catch"
end
```
- In case "catch" doesn't catch it, "after" gets executed and exception thrown brings the whole program comes down!!!!
- Variables inside try-catch are not accessible outside the code block
- Good practice is to use this as an expression

```elixir
{ x, y } = try do
    x = calculate_some_value()
    y = some_other_value()
    { x, y }
catch
    _ -> { nil, nil }
end
```
In case of exception, x and y are nil

## Calling function from Erlang

```elixir
# :<erlang_module>.<function> <params> e.g.

:lists.flatten [1, 2, [3, 4, [5, 6], 7]]
:math.sin :math.pi
```

## Misc
```elixir
# Range
r = 4..20
first..last = r  # -> first is 4, last is 20
Enum.max r    # -> 20

# Date

{:ok, d1} = Date.new(2019, 1, 3)
Date.day_of_week(d1)  # -> 4
Date.add d1, 7        # -> ~D[2019-01-10]

d2 = ~D[2019-01-03]
# This requires proper format, ~D[2019-1-3] will give error

d2 == d1                          # -> true

d3 = Date.add d2, 10
date_range = Date.range(d3, d2)
Enum.count date_range             # -> 11

~D[2019-01-05] in date_range      # -> true

# Time

{:ok, t1} = Time.new(8, 40, 40)
t2 = ~T[08:40:40]
Time.add t1, 120   # -> ~T[08:42:40.000000]
# 120 is in seconds default

Time.add t1, 120000, :milliseconds    # -> ~T[08:42:40.000000]

# Datetime and NaiveDateTime
# TODO - Complete the usage
```

With block
- Helps in creating a local scope, so temporary variables do not pollute global scope. E.g.

```elixir
content = "Now is the time"
lp =
    with {:ok, file} = File.open("/etc/passwd"),
        content = IO.read(file, :all),
        :ok = File.close(file),
        [_, uid, gid] = Regex.run(~r/^_lp:.*?:(\d+):(\d+)/m, content)
        # -> = can be replaced by <- (see below)
        do
            "Group: #{gid}, User: #{uid}"
        end

# With can also return nil instead of "Matching Error" e.g.
result = with {[1, 2, 3], :rane} = {[1, 2, 3], :rane}, do: :success
# -> result now equals :success

result = with {[1, 2, 3, 4], :rane} = {[1, 2, 3], :rane}, do: :success
# -> MatchError

result = with {[1, 2, 3, 4], :rane} <- {[1, 2, 3], :rane}, do: :success
# -> result now equal nil, no MatchError raised

# With Better indentation
lp =
    with (
        {:ok, file} = File.open("/etc/passwd"),
        content = IO.read(file, :all),
        :ok = File.close(file),
        [_, uid, gid] <- Regex.run(~r/^_lp:.*?:(\d+):(\d+)/m, content)
    )
    do: "Group: #{gid}, User: #{uid}"
```

Exceptions:

General rule is to let Elixir raise exceptions automatically. If you want to raise an exception, you can use
```elixir
raise "Giving up"
# -> ** (RuntimeError) Giving up

raise RuntimeError
# -> ** (RuntimeError) runtime error

raise RuntimeError, message: "override message"
# -> ** (RuntimeError) override message
```
Avoid raising exceptions in general. VM takes care of those things properly.
