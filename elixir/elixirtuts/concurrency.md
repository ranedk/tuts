# Concurrency - the proof in the pudding of Elixir
```elixir
defmodule SpawnBasic do
    def greet do
        IO.puts "Hello"
    end
end

# Simple calling
SpawnBasic.greet                 # -> prints "Hello"

# Async calling
pid = spawn(SpawnBasic, :greet, [])    # -> prints "Hello", returns a PID e.g. #PID<0.120.0>
```

## 



