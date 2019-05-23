defmodule Link2 do
    import :timer, only: [ sleep: 1 ]

    # sad_function crashes after 500 milliseconds
  def sad_function(run_id) do
        send run_id, "Hi from sad"
        receive do
          msg ->
              IO.puts "Message to sad #{msg}"
          after 1000 ->
              IO.puts "sad running"
          end
        sad_function(run_id)
    end

    def run_loop do
      sleep 5000
      exit(:run_died)
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
