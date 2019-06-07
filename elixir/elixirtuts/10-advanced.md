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
More like creating generics e.g. List implements Enumerable protocol.
```elixir
to_string("foo")     # "foo"
to_string(":foo")    # ":foo"

to_string({:foo})   # ERROR!
```

Lets extend String interface for tuples e.g. `{:foo}`
```elixir
defimpl String.Chars, for: Tuple do
  def to_string(tuple) do
    interior =
      tuple
      |> Tuple.to_list()
      |> Enum.map(&Kernel.to_string/1)
      |> Enum.join(", ")

    "{#{interior}}"
  end
end

# Usage
# iex> to_string({3.14, "apple", :pie})   # "{3.14, apple, pie}"
```
### Defining a new protocol - Lets call it `to_atom`

```elixir
defprotocol AsAtom do
  def to_atom(data)
end

defimpl AsAtom, for: Atom do
  def to_atom(atom), do: atom
end

defimpl AsAtom, for: BitString do
  defdelegate to_atom(string), to: String
end

defimpl AsAtom, for: List do
  defdelegate to_atom(list), to: List
end

defimpl AsAtom, for: Map do
  def to_atom(map), do: List.first(Map.keys(map))
end
```
### Usage
```elixir
iex> import AsAtom
AsAtom
iex> to_atom("string")
:string
iex> to_atom(:an_atom)
:an_atom
iex> to_atom([1, 2])
:"\x01\x02"
iex> to_atom(%{foo: "bar"})
:foo
```

# Metaprogramming - Read about Quote/Unquote & Macros
https://elixirschool.com/en/lessons/advanced/metaprogramming

# Behaviours
These are basically interfaces or specs. Anyone extending them must implement named functions with proper attributes

Lets implement a behaviour called `Worker`, which implemented `init/1` and `perform/2`
```elixir
defmodule Example.Worker do

  # init function, take state which is a term, and may return 2 types of output tuples
  @callback init(state :: term) :: {:ok, new_state :: term} | {:error, reason :: term}

  # perform signature
  @callback perform(args :: term, state :: term) ::
        {:ok, result :: term, new_state :: term}
        | {:error, reason :: term, new_state :: term}
end
```

Usage:
```elixir
defmodule Example.Downloader do
  @behaviour Example.Worker

  def init(opts), do: {:ok, opts}

  def perform(url, opts) do
    url
    |> HTTPoison.get!()
    |> Map.fetch(:body)
    |> write_file(opts[:path])
    |> respond(opts)
  end

  defp write_file(:error, _), do: {:error, :missing_body}

  defp write_file({:ok, contents}, path) do
    path
    |> Path.expand()
    |> File.write(contents)
  end

  defp respond(:ok, opts), do: {:ok, opts[:path], opts}
  defp respond({:error, reason}, opts), do: {:error, reason, opts}
end
```
