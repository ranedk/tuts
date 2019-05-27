defmodule FibClient do

  def start_server do
    spawn(FibServer, :fib, [self()])
  end

  def run do
    receive do
      {server_pid, :ready} ->
        IO.puts("Server is ready")
        send server_pid, {:evaluate, :random.uniform(15), self()}
      {server_pid, :answer, result} ->
        IO.puts("Server replied: #{result}")
    end
    run()
  end

end
