List functions

Most of list is covered in basics, functions, recursion chapters
```elixir
List.foldl([1,2,3], "", fn value, acc -> "#{value}(#{acc})" end)
# -> "3(2(1()))"
List.foldr([1,2,3], "", fn value, acc -> "#{value}(#{acc})" end)
# -> "1(2(3()))"
```

Note: Replace is a costly operation
```elixir
List.replace_at([1,2,3,4,4,6], 4, 5)
# -> [1, 2, 3, 4, 5, 6]
```
List.keyfind only gives the first occurence
```elixir
List.keyfind([{:rane, 34, "python"}, {:amitu, 36, "rust"}, {:deepak, 35, "python"}], :rane, 0)
# -> {:rane, 34, "python"}
List.keyfind([{:rane, 34, "python"}, {:amitu, 36, "rust"}, {:deepak, 35, "python"}], "python", 2)
# -> {:rane, 34, "python"}
```
Others: List.keyreplace, List.keydelete

Data structures:

    - Maps: Fast key-value lookup
    - Keyword: Non-unique keys, Ordered
    - Struct: Fixed number of fields

Keywords:
- Since they are ordered and lookups work only for atoms, they are often used as context to functions

```elixir
defmodule Canvas do
    @defaults [ fg: "black", bg: "white", font: "Merriweather" ]

    def draw_text(text, options \\ []) do
        options = Keyword.merge(@defaults, options)

        IO.puts "Drawing text #{inspect(text)}"
        IO.puts "Foreground: #{options[:fg]}"
        IO.puts "Background: #{Keyword.get(options, :bg)}"
        IO.puts "Font: #{Keyword.get(options, :font)}"
        IO.puts "Pattern: #{Keyword.get(options, :pattern, "solid")}"
        IO.puts "Style: #{inspect Keyword.get_values(options, :style)}"
    end
end
Canvas.draw_text("hello", fg: "red", style: "italic", style: "bold")
```

Map:
```elixir
map = %{ name: "Dave", likes: "Programming", where: "Dallas" }
Map.keys map          # -> [:likes, :name, :where]
Map.values map        # -> ["Programming", "Dave", "Dallas"]
map[:name]            # -> "Dave"
map.name              # -> "Dave"
map1 = Map.drop map, [:where, :likes]     # -> %{name: "Dave"}
map2 = Map.put map, :also_likes, "Ruby"
# -> %{also_likes: "Ruby", likes: "Programming", name: "Dave", where: "Dallas"}
Map.keys map2         # -> [:also_likes, :likes, :name, :where]
Map.has_key? map1, :where     # -> false
{ value, updated_map } = Map.pop map2, :also_likes
# -> {"Ruby", %{likes: "Programming", name: "Dave", where: "Dallas"}}
Map.equal? map, updated_map   # -> true


person = %{ name: "Dave", height: 1.88 }
> %{ name: a_name } = person   # ->  assigns a_name to value of person.name
> %{ something: a_name } = person   # -> MatchError

> %{ name: _, height: _ } = person  # ->  matches, does not give MatchError
```
NOTE: You cannot BIND keys, only values can be bound via pattern matching, this also happens to be a good practice in other languages

List Comprehension
```elixir
people = [
    %{ name: "abhas", department: "aero", city: "kota"  },
    %{ name: "shyam", department: "aero", city: "patna" },
    %{ name: "hemant", department: "chem", city: "vizag" },
    %{ name: "rahul", department: "chem", city: "indore" },
    %{ name: "akhil", department:  "chem", city: "kota" },
]
```

```elixir
aero_guys = for person = %{ department: dept} <- people, dept == "aero", do: person
```

- The generator clause bind each map in the list to person and binds the department to dept
- the filter selector only those dept where dept value is "aero", do returns the matches

```elixir
item = List.first people 
# -> item = %{city: "kota", department: "aero", name: "abhas"}

for key <- [:city, :name] do
  %{ ^key => value } = item
  value
  end
# -> ["kota", "abhas"]
```


Updates on Map:
```elixir
new_map = %{ old_map | key1 => value1,  key2 = value2, ...}
```
Notes: This doesn't support adding new keys, can only update old keys


Struct:

- They are like typed maps, keys cannot be added later and has default values and behaviours

```elixir
defmodule Attendee do

    defstruct name: "", paid: false, over_18: true

    def may_attend_after_party(attendee = %Attendee{}) do
        attendee.paid && attendee.over_18
    end

    def print_vip_badge(%Attendee{name: name}) when name !=
        IO.puts "Very cheap badge for #{name}"
    end

    def print_vip_badge(%Attendee{}) do
        raise "missing name for badge"
    end

end
```
```elixir
s1 = %Subscriber{}                           
# ->  %Subscriber{name: "", over_18: true, paid: false}
s2 = %Subscriber{ name: "Dave" }              
# ->  %Subscriber{name: "Dave", over_18: true, paid: false}
s3 = %Subscriber{ name: "Mary", paid: true }  
# -> %Subscriber{name: "Mary", over_18: true, paid: true}
s3.name       #-> "Mary
```

- Updating
```elixir
s4 = %Subscriber{ s3 | name: "Marie"}"        
# -> %Subscriber{name: "Marie", over_18: true, paid: true}
Attendee.may_attend_after_party(s4)
```


Nested Structs

```elixir
defmodule Customer do
    defstruct name: "", company: ""
end

defmodule BugReport do
    defstruct owner: %Customer{}, details: "", severity: 1
end
```
```elixir
report = %BugReport{owner: %Customer{name: "Dave", company: "Pragmatic"}, details: "broken" }
```
- Accessing attributes
```elixir
report.owner.company
```

- Modifying a nested attribute is PAINFUL
```elixir
report = %BugReport{ report | owner: %Customer{ report.owner | company: "PragProg" }}
```

- Elixir gives a macro to do the above
NOTE: Macros generate the same erlang code in elixir during compile time

```elixir
put_in(report.owner.company, "PragProg")
# OR
put_in(report[:owner][:company], "PragProg")

update_in(report.owner.name, &("Mr." <>  &1))    
# -> runs a lambda on the variable
# OR
update_in(report[:owner][:name], &("Mr." <> &1))
```

put_in and update_in also offer non-macro runtime code to access fields in runtime
```elixir
get_in(report, [:owner, :name])
put_in(report, [:owner, :name, :first], "Dev")
```

Access module (awesome module to put/update)

```elixir
cast = [
    %{
        character: "Buttercup",
        actor: %{
            first: "Robin",
            last: "Wright"
        },
        role: "princess"
    },
    %{
        character: "Westley",
        actor: %{
            first: "Cary",
            last: "Elwes"
        },
        role: "farm boy"
    }
]
```

```elixir
get_in(cast, [Access.all(), :character])      
# -> ["Buttercup", "Westley"]
> get_in(cast, [Access.at(1), :role])           
# -> "farm boy"

get_and_update_in(cast, [Access.all(), :actor, :last], fn (val) -> {val, String.upcase(val)} end) 
# -> Makes last name all caps

get_in(cast, [Access.all(), :actor, Access.elem(1)])      
# -> ["Wright", "Elwes"]

IO.inspect get_and_update_in(cast, [Access.key(:buttercup), :role], fn (val) -> {val, "Queen"} end)  
# -> Changes buttercup's role to Queen

{popped_value, rest_} = Access.pop(%{name: "Elixir", creator: "Valim", type: "Superhuman"}, :name)
# -> popped_value = "Elixir", rest = %{creator: "Valim", type: "Superhuman"}
```

Sets (implemented as MapSet)

```elixir
set1 = 1..5 |> Enum.into(MapSet.new)
set2 = 3..8 |> Enum.into(MapSet.new)
MapSet.member? set1, 3    # -> true
MapSet.union set1, set2   # -> MapSet<[1, 2, 3, 4, 5, 6, 7, 8]>
```

- MapSet.intersection, MapSet.subset etc.

Note: Dont use structs a lot, its more of a OOP concept and can/should be avoided in Elixir


Functionality Collection

- Enum implements tons of functionality around list, and work on anyone who implements a "Eumerable" Protocol

- Enum.to_list, Enum.map, Enum.concat, Enum.at, Enum.filter, Enum.reject, Enum.sort, Enum.take, Enum.take_every, Enum.take_while etc.

```elixir
l = 1..10
Enum.take l, 3                                        
# -> [1, 2, 3]

Enum.take_every l, 3                                  
# -> [1, 3, 5]     Take every 3rd element

Enum.take_while [1,2,3,4,5,6,2,1], &(&1 < 4)          
# -> [1, 2, 3]     Take till a condition matches

Enum.all? l, &(&1 < 4)                                
# -> false

Enum.any? l, &(&1 < 4)                                
# -> true

Enum.zip [:a, :b, :c], [1, 2, 3]                      
# -> [a: 1, b: 2, c: 3]

Enum.reduce 1..100, &(&1 + &2)                        
# -> 5050

Enum.reduce ["Lets", "find", "the", "longest", "word", "here"], fn word, longest ->
    if String.length longest >= String.length word do
        longest
    else
        word
```

- Deal a hand of cards
```elixir
import Enum
deck = for rank <- '23456789TJKQA', suit <- 'CDHS', do [suit, rank]
hands = deck |> shuffle |> chunk(13)
```

Streams

- Streams are list implemented like yeild in python
- Great when data is too large to fit in memory or arriving in due time
- Best fit for data from IO operations
- Use in scenarios where all data in a Enumerable is not required for procession at one time
- Bad when data is small and can be processed in a List easily without major memory overhead


To find the longest word in dictionary, without streams
```elixir
IO.puts File.read!("/usr/share/dict/words")             
# -> reads all file in one go
    |> String.split
    |> Enum.max_by(&String.length/1)

# with Streams
IO.puts File.open!("/usr/share/dict/words")         # -> creates a file handle (doesn't read yet)
    |> IO.stream(:line)                             # -> creates a stream, little slow, but good on memory
    |> Enum.max_by(&String.length/1)

# Better, directly use file stream to read shortcut
IO.puts File.stream!("/usr/share/dict/words") |> Enum.max_by(&String.length/1)
```

- Behaves exactly like Enumerables
```elixir
[1,2,3,4]           # -> This can be a stream or a Enum. Larger the better, or IO stream
    |> Stream.map(&(&1*&1))
    |> Stream.map(&(&1+1))
    |> Stream.filter(fn x -> rem(x,2) == 1 end)
    |> Enum.to_list
```

Streams works best for large dataset. e.g.

```elixir
Enum.map(1..10_000_000, &(&1+1)) |> Enum.take(5)      # -> Take more than 10 seconds to run
Stream.map(1..10_000_000, &(&1+1)) |> Enum.take(5)    # -> Runs instantly
```

Stream methods:
- Cycle
```elixir
Stream.cycle(~w{ green white }) |>        # -> generator to create a infinite list of ["green", "white", "green", "white", "green"....]
    Stream.zip(1..5) |>                   # -> zips it to list [1,2,3,4,5] till the stream is over
    Enum.map(fn {class, value} ->
        "<tr class='#{class}'><td>#{value}</td></tr>\n" end) |>
    IO.puts
```
Output:
```html
<tr class="green"><td>1</td></tr>
<tr class="white"><td>2</td></tr>
<tr class="green"><td>3</td></tr>
<tr class="white"><td>4</td></tr>
<tr class="green"><td>5</td></tr>
```

- Stream.repeatedly
Takes a function and invokes it each time a new value is wanted.
```elixir
Stream.repeatedly(&:random.uniform/0) |> Enum.take(3)     
# -> Generates 3 random numbers
```
- Stream.unfold
Uses functions to generate a list, functions takes 2 values to generate the 3rd and so on (like fibonacci)

```elixir
Stream.unfold({0,1}, fn {f1,f2} -> {f1, {f2, f1+f2}} end) |> Enum.take(8)
```