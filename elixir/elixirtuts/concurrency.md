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

## Sending messages between processes
```elixir
defmodule PingPong.CLI do

  def ping() do
    receive do
      {sender, msg} ->
        IO.puts("ping gets #{msg}")
        :timer.sleep(100)
        send sender, {self(), msg + 1}
    end
    ping()
  end

  def pong() do
    receive do
      {sender, msg} ->
        IO.puts("pong gets #{msg}")
        :timer.sleep(100)
        send sender, {self(), msg + 1}
    end
    pong()
  end

  def main(_argv) do
    IO.puts("Setting up table")
    ping_pid = spawn(__MODULE__, :ping, [])
    pong_pid = spawn(__MODULE__, :pong, [])
    send ping_pid, {pong_pid, 0}
    :timer.sleep(2000)
  end

end
```
>Note: Run script using `elixirc pingping.ex`
>Note: Running standalone scripts in elixir as a binary requires you to set up `mix` and then run `mix escript.build`
>Note: You can however run it from repl iex `iex> c("Filename.ex")`

## Time-out if there are no messages
```elixir
receive do
    {:ok, message} ->
        IO.puts message
    after 500 ->
        IO.puts "The sender is delayed"
end
```

## Cool example 1
Lets create `n` elixir processes, such that we give `0` to the first process, it increments and passes it to the next process and so on till all processes have incremented the value one. Also, see the time used to create processes.

```elixir
defmodule Chain do

    # counter receives and send to next pid
    def counter(next_pid) do
        receive do
            n ->
                send next_pid, n + 1
        end
    end

    # create "n" processes async
    def create_processes(n) do
        code_to_run = fn (_,send_to) ->
            spawn(Chain, :counter, [send_to])
        end

        # Cool way to use reduce to spawn and get the last process
        last = Enum.reduce(1..n, self(), code_to_run)

        # start the count by sending a zero to the last process
        send(last, 0)

        # and wait for the result to come back to us
        # using a is_integer guard since some beam VMs have a bug
        # where they send a message to mark process completion
        receive do
            final_answer when is_integer(final_answer) ->
                "Result is #{inspect(final_answer)}"
        end
    end

    # timer is erlang module, tc calculates the time to run
    def run(n) do
        :timer.tc(Chain, :create_processes, [n])
        |> IO.inspect
    end
end

Chain.run(100000)
```
Output: `{323158, "Result is 100000"}`  Takes 323158 microseconds for 100K processes

## Process linking

Often if one process dies, the other doesn't get to know. So if the crashed process was supposed
to send something, the listener would hang forever.

```elixir
defmodule Link2 do
    import :timer, only: [ sleep: 1 ]

    # sad_function crashes after 500 milliseconds
    def sad_function do
        sleep 500
        exit(:boom)
    end

    # spawn_link, link run to sad_function
    def run do
        spawn_link(Link2, :sad_function, [])
        receive do
            msg ->
                IO.puts "MESSAGE RECEIVED: #{inspect msg}"
            after 1000 ->
                IO.puts "Nothing happened as far as I am concerned"
        end
    end
end
Link2.run
```
Running this gives a ERROR
Error output: `** (EXIT from #PID<0.73.0>) :boom`

To Convert this into a message and not an error:
add `Process.flag(:trap_exit, true)` above spawn_link line




