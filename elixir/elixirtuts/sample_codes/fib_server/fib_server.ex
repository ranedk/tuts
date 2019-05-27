defmodule FibServer do

  def fib(client) do
    send client, {self(), :ready}
    receive do
      {:evaluate, n, client} ->
        send client, {self(), :answer, fib_calc(n)}
        :timer.sleep(1000)     # random sleep
        fib(client)
      {:shutdown, _} ->
        exit(:normal)
    end
  end

  # The fib logic
  defp fib_calc(0), do: 0
  defp fib_calc(1), do: 1
  defp fib_calc(n), do: fib_calc(n-1) + fib_calc(n-2)

end
