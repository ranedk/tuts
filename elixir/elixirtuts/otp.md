# Open Telecom Platform
Set of tools and services which create a more structured and easy way to manage processes on erlang.
Its vast and there are lots of libraries. We will cover essentials.

Application contains Processes. Processes have behaviors. Each behavior has its own process.
Behaviours are standard patterns e.g. "Finite state machine", "Event handler", "Server", "Supervisor" etc.

# OTP server (GenServer)
A server should manage its request queues, response, processes etc.
`$ mix new sequence`
`$ cd sequence; mkdir lib/sequence`
Create a file `server.ex`
```elixir
defmodule Sequence.Server
    use GenServer   # use GenServer behavior

    # when server starts, defines the state {:ok, state}
    def init(initial_number) do
        {:ok, initial_number}
    end

    # When request comes, handle_call gets <request>, <client pid>, <current_state>
    # It must reply with <reply>, <state>, <new_state>
    def handle_call(:next_number, _from, current_number) do
        {:reply, current_number, current_number + 1}
    end
```
Running the projects
```
$ iex -S mix
iex> {:ok, pid} = GenServer.start_link(Sequence.Server, 100)       # init call
iex> GenServer.call(pid, :next_number)      # 100
iex> GenServer.call(pid, :next_number)      # 101
iex> GenServer.call(pid, :next_number)      # 102
```
If you don't want a response, but only change the server state
```elixir
def handle_cast({:incr, delta}, current_number) do
    {:noreply, current_number + delta}
end
```
#`$ start_link` magic
Can help you debug and get stats.
```elixir
# To trace the flow
iex> {:ok,pid} = GenServer.start_link(Sequence.Server, 100, [debug: [:trace]])

# To get stats
iex> {:ok,pid} = GenServer.start_link(Sequence.Server, 100, [debug: [:statistics]])
# Run some code
iex> :sys.statistics pid, :get   # will give you stats of the code run above

# To turn sys on and off
iex> :sys.trace pid, true
iex> :sys.trace pid, false

# To get status of a process
iex> :sys.get_status pid
```

Instead of using pids, you can name servers.
```elixir
iex> { :ok, pid } = GenServer.start_link(Sequence.Server, 100, name: :seq)
iex> GenServer.call(:seq, :next_number)
iex> GenServer.call(:seq, :next_number)
iex> :sys.get_status :seq
```
For more details on the 6 callbacks provided by GenServer, refer docs

# Code structuring
There are 3 parts to the code.
- Server
- Wrapper to call server interface
- Implementation of the business logic

You can put all 3 into separate files in the `lib/sequence` folder

sequence.ex
```elixir
defmodule Sequence do
    @server Sequence.Server

    def start_link(current_number) do
        GenServer.start_link(@server, current_number, name: @server)
    end

    def next_number do
        GenServer.call(@server, :next_number)
    end

    def increment_number(delta) do
        GenServer.cast(@server, {:increment_number, delta})
    end
end
```

server.ex
```elixir
defmodule Sequence.Server do
    use GenServer
    alias Sequence.Impl

    def init(initial_number) do
        { :ok, initial_number }
    end

    def handle_call(:next_number, _from, current_number) do
        { :reply, current_number, Impl.next(current_number) }
    end

    def handle_cast({:increment_number, delta}, current_number) do
        { :noreply, Impl.increment(current_number, delta) }
    end

    def format_status(_reason, [ _pdict, state ]) do
        [data: [{'State', "My current state is '#{inspect state}', and I'm happy"}]]
    end
end
```

impl.ex
```elixir
defmodule Sequence.Impl do

    def next(number), do: number + 1
    def increment(number, delta), do: number + delta

end
```



