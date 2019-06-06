# Node - The power of running elixir across multiple machines

`iex> Node.self` gives the name of the node (the machine running one instance of beam vm)
`$ iex --name dev@local` to name a node

# Communication between 2 nodes
Node 1 (start a terminal session)       `$ iex --sname one`
Node 2 (start another terminal session, change to a different directory) `$ iex --sname two`

In Node 1:
```elixir
iex(one@rane)1> Node.connect :two@rane
iex(one@rane)2> fun = fn -> IO.puts(Enum.join(File.ls!, ",")) end
iex(one@rane)3> Node.spawn(:two@rane, fun)
<list of files in the directory two@rane is running>
```

In Node 2:
```elixir
iex(two@rane)1> fun = fn -> IO.puts(Enum.join(File.ls!, ",")) end
iex(two@rane)2> Node.list
<list of all nodes connected to Node 2, that is Node 1>
iex(two@rane)3> Node.spawn(:one@rane, fun)
<list of files in the directory one@rane is running>
```

`Node.spawn` returns the pid of the process which is spawned on the other node.
The two nodes will have different pid sequences. <Node-ID>.<Process-Id>.<Creation-Tag>
The local node will always have a <Node-ID> 0

## Security
To make node interaction secure, a cookie is used
`$ iex --sname one --cookie <some-auth-cookie>`
Now, all nodes which have the same cookie can interact

Note: Cookie is transmitted in plain-text, so open networks are not safe

## Global pid-name registry
Instead of managing pids, its better to register them with names in the global registry.
So that processes can interact with each other using names e.g.
A ticker-tocker server-client
```elixir
# Server code - this defines interface to interact with server and also interface to start it.

defmodule Ticker do

    @interval 2000 # 2 seconds
    @name :ticker

    def start do
        pid = spawn(__MODULE__, :generator, [[]])
        # good to register pid with name when starting the process
        :global.register_name(@name, pid)
    end

    # interface to interact with Ticker server
    def register(client_pid) do
        send :global.whereis_name(@name), { :register, client_pid }
    end

    # The Ticker process which sends tickers to connected clients
    def generator(clients) do
        receive do
            { :register, pid } ->
                IO.puts "registering #{inspect pid}"
                generator([pid|clients])

            after @interval ->
                IO.puts "tick"
                Enum.each clients, fn client ->
                    send client, { :tick }
                end
            generator(clients)
        end
    end
end

# Client tocker

defmodule Client do

    def start do
        pid = spawn(__MODULE__, :receiver, [])
        # register client's pid with server
        Ticker.register(pid)
    end

    def receiver do
        receive do
            { :tick } ->
                IO.puts "tock in client"
                receiver()
        end
    end
end
```

## Master - Group leader
`IO.puts` prints on the group leader. To make one of the nodes a group leader
`iex> :global.register_name(:two, :erlang.group_leader)`
