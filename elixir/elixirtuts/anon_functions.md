Functions:
- Anonymous functions:

fn
    parameter-list -> body
    parameter-list -> body
    parameter-list -> body
end

- parameter-list is matched and they are not input parameters in the regular sense.
- The function handle_open takes two parameters, which are output of a File.open (<:ok/:error>, <file_contents/error_text>)

> handle_open = fn
>   {:ok, file} -> "File data: #{IO.read(file, :line)}"
>   {_, error} -> "Error: #{:file.format_error(error)}"
> end

> handle_open.(File.open("code/intro/hello.exs"))   # -> "Read data: IO.puts \"Hello, World!\"\n"
> handle_open.(File.open("nonexistent"))            # -> "Error: no such file or directory"


Functions returning functions

> hello = fn ->
>     fn ->
>         "Hello"
>     end
> end

> hello.().()

Closures

> multiply = fn n -> (fn a -> n*a end) end

> double = multiply.(2)
> double.(11)    # -> 22

> triple = multiply.(3)
> triple.(11)    # -> 33


Functions can take other functions as parameters
> times_2 = fn n -> n * 2 end
> apply = fn (fun, value) -> fun.(value) end
> apply.(times_2, 6)     # -> 12


Functional aspects of language
> Enum.map [1,2,3,4,5], fn n -> n * 2 end

Note:
- In case of a closure, you might want to pin the variable for a match. use the ^variable notation

& shortcuts

> add_one = &(&1 + 1)       # -> same as add_one = fn (n) -> n + 1 end
> multipler = &(&1 * &2)    # -> &1 means the first param, &2 means second param and so on

> divrem = &{ div(&1, &2), rem(&1, &2) }  # -> tuples as functions
> divrem.(19, 4)    # -> {4, 3}

> divrem = &[ div(&1, &2), rem(&1, &2) ]  # -> List as functions
> divrem.(19, 4)    # -> [4, 3]

> s = &"bacon and #{&1}"    # -> String as functions
> s.("custard")     # -> bacon and custard"

> if_ends_with = &~r/.*#{&1}$/
> res = "cat" =~ if_ends_with.("t")   # -> true

> Enum.map [1,2,3,4], &(&1 * 2)  # -> [2, 4, 6, 8]


