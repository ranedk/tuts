# try do - rescue - after - end
Error handling
```elixir
try do
  opts
  |> Keyword.fetch!(:source_file)
  |> File.read!()
rescue
  e in KeyError -> IO.puts("missing :source_file option")
  e in File.Error -> IO.puts("unable to read source file")
after
  IO.puts("This can be used for cleanup")
end
```
## Custom exceptions
```elixir
defmodule ExampleError do
  defexception message: "an example error has occurred"
end
```

# Read about Protocols
https://elixirschool.com/en/lessons/advanced/protocols/

# Read about Macros
https://elixirschool.com/en/lessons/advanced/metaprogramming/#macros

# Behaviours
https://elixirschool.com/en/lessons/advanced/behaviours/
