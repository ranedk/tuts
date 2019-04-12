Modules and files:

- Create file math.ex, define a module inside it:

defmodule Math do

    def sum(a, b) do
        a + b
    end

    def concatenate(a, b) do
        a ++ b
    end

end

- Compile using
$ elixirc math.ex  # generate Elixir.math.beam

- Project structure
    - ebin - for compiled byte code (*.beam)
    - lib - contains elixir code (*.ex)
    - test - contains test scripts (*.exs)

- Add byte code path to iex, elixir or elixirc
$ iex -pa ebin   # pa stands for "path append"

- Standalone scripts (*.exs)
$ elixir Math.exs   # no byte code generated

- Private functions (defp)

defmodule Math do

    defp sum(a, b) do           # private function Math.sum  will raise undefined error
        a + b
    end

    def concatenate(a, b) do    # public function can be accessed as Math.concatenate
        a ++ b
    end

end


Functions

Note: Function returns the output of the last expression in the function.

defmodule Random do
    def f(x) do
        z = x + 2
    end
end
> v = Random.f 100  # v is 102

defmodule Random do
    def f(x) do
        z = x + 2
        z
    end
end
> v = Random.f 100  # v is 102


defmodule Random do
    def f(x) do
        z = x + 2
        IO.puts z
    end
end
> v = Random.f 100  # print "102", v is :ok


defmodule Math do

    def zero?(0) do
        true
    end

    def zero?(x) when is_number(x) do       # functions support guards
        false                               # If guard doesn't match function is "not defined" for that parameter
    end

    def zero?(x) when is_number(x) and x == 3 do   # Never gets defined/called since the one above always matches
        false
    end
end

- All clauses/definitions of the function are checked till a definition is found.
- The order is top to bottom
- If one definition is found, the rest is ignored

> Math.zero?(0)   # true
> Math.zero?(3)  # false
> Math.zero?('a') # FunctionClauseError

Note: Pattern matching can be used in clever ways e.g.

defmodule Clever do
    def square(n, n), do n*n
end

> Clever.square(5, 6)   # -> Error, this function will take same parameters
> Clever.square(5, 5)   # -> 25


- Default arguments

defmodule Concat do
    def join(a, b, sep \\ " ") do
        a <> sep <> b
    end
end

IO.puts Concat.join("Hello", "world")       # Hello world
IO.puts Concat.join("Hello", "world", "_")  # Hello_world

- Function calls can be default arguments, they get executed only when variable is accessed

defmodule DefaultTest do
    def dowork(x \\ IO.puts "hello") do  # -> will not be evaluated during load time
        x
    end
end

> DefaultTest.dowork "rane" # -> gets overridden, return value is "rane"
> DefaultTest.dowork        # -> gets evaluated, prints "hello", return value is :ok

- Be careful with multiple clauses, possible to be in a situation where one code path
  is never traversed because a preceding clause always matches with default value

- If a function with default values has multiple clauses, it is recommended to create a
separate clause without an actual body, just for declaring defaults e.g.

defmodule Concat do

    def join(a, b \\ nil, sep \\ " ")      # No function body, for default values

    def join(a, b, _sep) when nil?(b) do   # Guard can be used to check if default value was used
        a
    end

    def join(a, b, sep) do
        a <> sep <> b
    end

end

> IO.puts Concat.join("Hello", "world")     #=> Hello world
> IO.puts Concat.join("Hello", "world", "_")  #=> Hello_world
> IO.puts Concat.join("Hello")                #=> Hello


Recursion

- This is the most important part of immutable functional programming
- Since you cannot mutate, you can to use tail recursion i.e. calling the same
  function, till end condition is reached. So recursion becomes very important

- Sum all elements of a list

defmodule Rane do
    def sum([], s) do           # most strict match first
        s
    end
    def sum(l) do
        sum(l, 0)
    end
    def sum([h | t], s) do      # most generic match last, NOTE: argument ungrouping
        s = s + h
        sum(t, s)
    end
end

- Square all elements of a list

    def square([]), do: []
    def square([h | t ]), do: [ h * h | square(t)]


- Creating a map function

    defmodule Rane do
        def mymap(func, []), do: []
        def mymap(func, [h | t]), do: [func.(h) | mymap(func, t)]
    end

> Rane.mymap(&(&1 * 2), [1, 2, 3, 4])   # -> [1, 4, 9, 16]


- Creating a reduce function

    def reduce([], value, _), do: value
    def reduce([head | tail], value, func), do: reduce(tail, func.(head, value), func)

- Lets pattern match a list of list.
    Suppose we have a list of list, each element as [idx, name, dept, age]
    Lets write a function to filter based on dept

```
defmodule Data do

    test = [[1, "Rane", "Aero", 16], [2, "Abhas", "Aero", 17], [3, "Rahul", "Chem", 16], [4, "Akhil", "Chem", 17]]

    def age_filter([], dept), do: []
    def age_filter([[idx, name, dept, age] | tail], age), do: [[idx, name, dept, age] | age_filter(tail, age)]
    def age_filter([_ | tail], age), do: age_filter(tail, age)

    age_filter(test)
end
```

- The above works fine, but in the 2nd definition of age_filter, idx, name, age are not being used, its can be written better as

```
    def age_filter([], dept), do: []
    def age_filter([head = [_, _, dept, _] | tail], age), do: [head | age_filter(tail, age)]
    def age_filter([_ | tail], age), do: age_filter(tail, age)
```

- The Enum module already implements functional stuff like map, reduce, filter etc.
> Enum.reduce([1, 2, 3], 0, fn(x, acc) -> x + acc end)


Imports

- alias
> alias Math.List, as: List    # not Math.List is available as List
> List.first [1, 3, 5]

- If alias is defined inside a function, the alias is valid only in that function

- require (like import)
> require MyModule
> MyModule.run

- import

> import List, only: [duplicate: 2]     # from List module import duplicate/2
> import List, except: [duplicate: 2]   # from List module import everything except duplicate/2
> import List, only: :default           # import all macros and functions, except ones starting with underscore
> import List                           # import everything
> import List only: :functions          # import all functions (not macros)
> import List only: :macros             # import all macros (not functions)

Note: require doesnt change the namespacing, compared to python, require is "import list", import is "from list import *"


Module attributes

defmodule MyServer do
    @vsn 2                  # version attribute, used for hot reloading (if not present, md5 of code in module is used)
end

- Are not directly accessible as MyServer.vsn, but you can create a getter to get value e.g.

defmodule MyServer do
    @vsn 2
    def get_vsn, do: @vsn
end

- Other attributes
    - @moduledoc (documentation of module)
    - @doc (documentation of function or macro)

- Custom attributes
    defmodule Example do
        @author "Dave Thomas"
        def get_author do
            @author
        end
    end
IO.puts "Example was written by #{Example.get_author}"

Pipe Operator

- In functional programming, chaining is a very critical design pattern, so code often looks like
> filing = prepare_filing(sales_tax(Orders.for_customers(DB.find_customers), 2018))

OR

> people = DB.find_customers
> orders = Orders.for_customers(people)
> tax = sales_tax(orders, 2018)
> filing = prepare_filing(tax)

- Elixir gives a syntax sugar on it:
> filing = DB.find_customers
>   |> Orders.for_customers
>   |> sales_tax(2018)
>   |> prepare_filing

> (1..10) |> Enum.map(&(&1*&1)) |> Enum.filter(&(&1 < 40))
