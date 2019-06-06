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
> Note: Pass any random things to GenServer.call and GenServer will crash! e.g. `GenServer.call(:seq, :bla)`
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

# Supervisors
Managing crashes due to exceptions is painful in any system.
In erlang/elixir supervisors make recovery from crashes easy and robust without losing data.

To include supervisor in a project, start it as
`$ mix new --sup sequence`
With this, mix creates a file named `application.ex` inside `lib/sequence/` which is the supervisor.
We need to tell the application, what needs to be supervised:
```elixir
defmodule Sequence.Application do

    @moduledoc false
    use Application

    def start(_type, _args) do
        children = [                # all processes which need to be watched
            { Sequence.Server, 100},
        ]

        opts = [strategy: :one_for_one, name: Sequence.Supervisor]
        Supervisor.start_link(children, opts)   # link child processes and start Sequence.Server init()
    end
end
```
Now, starting `iex -S mix` will autostart server
```
iex> Sequence.Server.increment_number 3
:ok
iex> Sequence.Server.next_number
103

iex> Sequence.Server.increment_number :bla      # this crashes the process, with a crash report
                                                # But supervisor restarts the process with 100 as initial_number
```
> Note: When supervisor restarts a process, it used the `def start` in `application.ex`, so the state is LOST

## Process and supervisor links
`Supervisor.start_link` takes the processes and `opts` which defines the strategy on crash.
- `:one_for_one` If the server dies, supervisor will restart it
- `:one_for_all` If the server dies, all other processes are terminated and restarted
- `:rest_for_one` if a server dies, the servers that follow it in the list of children are terminated, and then the dying server and those that were terminated are restarted.

> Note: If a process may be terminated by the supervisor, its terminate behaviour needs to be defined as
```elixir
def terminate(_reason, current_number) do
    <logic for termination>
end
```

One way to make sure that server crashes, do not reset the `state` is to start another process and use it to store state. If the _storage process_ crashes, everything crashes and restarts, if the _Sequence process_ closes, only restart the _Sequence process_. So that _storage process_ still has the last `state`.
The `init` of the _Sequence process_ will take no parameter, instead uses _storage process_ state to initialize it

## Worker supervision
Supervisor defines strategy on linking two process workers. But workers also need to define the restart strategy for supervisor:
```elixir
defmodule Sequence.Server do
    use GenServer, restart: :transient      # Worker strategy
```
- `:permanent` - This process should always be running
- `:temporary` - This process is temporary and must never be restarted if the worker dies
- `:transient` - In case of Normal termination, this process must not be restarted, but if dies abnormally, restart it.

> Note: At the very lowest level, it is a list of child specifications. A child spec is an Elixir map. It describes which function to call to start the worker, how to shut the worker down, the restart strategy, the worker type, and any modules apart from the main module that form part of the worker.

> Note: You can create a child spec map using the `Supervisor.child_spec/2` function

