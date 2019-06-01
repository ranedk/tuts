# Tasks, the real Async - Await

If you want simpler things and dont want to use the complexities for `send` `spawn`, this is cool.

```elixir
defmodule Fib do
    def of(0), do: 0
    def of(1), do: 1
    def of(n), do: Fib.of(n-1) + Fib.of(n-2)
end

IO.puts "Start the task"
worker = Task.async(fn -> Fib.of(20) end)
IO.puts "Do something else"
IO.puts "Wait for the task"
result = Task.await(worker)         # waits till async task is done
IO.puts "The result is #{result}"
```

If a task with `Task.async` has crashed, you will get an error when you call `Task.await`
Instead, if we use `Task.start_link`, the process which has `Task.await` will crash immediately if task crashes.

You can even start a Task directly in a supervisor
```elixir
children = [
    { Task, fn -> do_something_extraordinary() end }
]

Supervisor.start_link(children, strategy: :one_for_one)
```
Or use `use Task` to make any module a Task module
```elixir
defmodule MyApp.MyTask do
    use Task

    def start_link(param) do
        Task.start_link(__MODULE__, :thing_to_run, [ param ])
    end

    def thing_to_run(param) do
        IO.puts("Doing something nice!")
    end
end
```

# Agents

Agent is a store which can store state, that can be accessed from any node!
```elixir
{ :ok, count } = Agent.start(fn -> 0 end)   # set the state, when you start the agent, count contains pid of the agent process

Agent.get(count, &(&1))     # Get a value of state, &(&1) just return the state value, you can run a function, before getting the value

Agent.update(count, &(&1+1))    # Update the value of state

# Instead of a pid, you can give the agent a name and use it
Agent.start(fn -> 1 end, name: Sum)     # Sum is the name

Agent.get(Sum, &(&1))       # get value of sum

Agent.update(Sum, &(&1+99)) # update Sum
```
You can use `Agent` directly into a module, without using a state variable e.g.
```elixir
# Word frequency example
defmodule Frequency do

    # When starting the app, set initial value of agent to empty map
    # name the agent as the name of the module
    def start_link do
        Agent.start_link(fn -> %{} end, name: __MODULE__)
    end

    # When a word is added, update the Agent directly
    def add_word(word) do
        Agent.update(__MODULE__, fn map ->  Map.update(map, word, 1, &(&1+1)) end)
    end

    # When you want to read the count of a word, get it directly from the agent
    def count_for(word) do
        Agent.get(__MODULE__, fn map -> map[word] end)
    end

    # Get all words
    def words do
        Agent.get(__MODULE__, fn map -> Map.keys(map) end)
    end
end
```




