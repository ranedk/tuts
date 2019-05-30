defmodule Scheduler do

  def run(num_processes, module, func, to_calculate) do
    1..num_processes
    |> Enum.map(fn(_) -> spawn(module, func, [self()]) end)
    |> schedule_process(to_calculate, [])
  end

  def schedule_process(processes, queue, results) do
    receive do
      {:ready, pid} when length(queue) > 0 ->
        [next | tail] = queue
        send pid, {:fib, next, self()}
        schedule_process(processes, tail, results)

      {:ready, pid} ->
        if length(processes) > 1 do
          schedule_process(List.delete(processes, pid), queue, results)
        else
          Enum.sort(results, fn {n1,_}, {n2, _} -> n1 <= n2 end)

      {:answer, number, result, _pid} ->
            schedule_process(processes, queue, [{number, result} | results])

    end
  end

end

