# Specifications (poor man's typings)

```elixir
# Defines a function, which takes an integer and returns an integer
@spec sum_product(integer) :: integer
def sum_product(a) do
  [1, 2, 3]
  |> Enum.map(fn el -> el * a end)
  |> Enum.sum()
end
```

# Custom types
If a function takes a complex input, you can define the spec of the input only for that function as
```elixir
@spec sum_times(integer, %Examples{first: integer, last: integer}) :: integer
def sum_times(a, params) do
  for i <- params.first..params.last do
    i
  end
  |> Enum.map(fn el -> el * a end)
  |> Enum.sum()
  |> round
end
```
> Note: `Example` struct is available only to `sum_times` function

This approach is fine for one-off structures which are only associated to a function.
A more generic type definition is which can be used elsewhere is:

```elixir
defmodule Examples do                   # Module Example
  defstruct first: nil, last: nil       # has struct with default values nil

  @type t(first, last) :: %Examples{first: first, last: last}
  # This defines the a generic type where first and last can take any values

  @type t :: %Examples{first: integer, last: integer}
  # This defines the a type where first and last must be integers
end
```
Usage: The above allows the following types:
```Elixir
@spec sum_times(integer, Examples.t()) :: integer
# sum_times must take Example with {integer, integer}, since "type t" without parameters
# wants only integer, integer type

@spec sum_times(integer, Examples.t(atom, integer)) :: integer
# sum_times must take {atom, integer} struct form, since "type t(first, second)" defines
# generic type


```
