defmodule Link2 do
    import :timer, only: [ sleep: 1 ]

    # sad_function crashes after 500 milliseconds
  def sad_function(run_id) do
        send run_id, "Hi from sad"
        sleep 3000
        exit(:boom)
    end

    def run_loop do
      receive do
          {:EXIT, from_pid, :normal} ->        # when sad exits normally
              IO.puts("Linked function exited normally")
          {:EXIT, from_pid, reason} ->        # when sad crashes, run gets a message
              IO.puts("Linked function crashed with reason: #{reason}")
          msg ->
              IO.puts "MESSAGE RECEIVED: #{inspect msg}"
          after 1000 ->
              IO.puts "Nothing happened as far as I am concerned"
      end
      run_loop()
    end

    def run do
        # trap the link exit, if you remove this, run crashes and run_loop
        # doesn't get the crash message in receive loop
        Process.flag(:trap_exit, true)
        # sid = spawn_monitor(Link2, :sad_function, [self()])
        sid = spawn_link(Link2, :sad_function, [self()])
        run_loop()
    end
end

import :timer, only: [ sleep: 1 ]
spawn(Link2, :run, [])
sleep 100000
