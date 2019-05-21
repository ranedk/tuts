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
