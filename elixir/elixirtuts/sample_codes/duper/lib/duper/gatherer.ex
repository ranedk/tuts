defmodule Duper.Gatherer do

  use GenServer

  @me Gatherer

  # API

  def start_link(worker_count) do
    GenServer.start_link(__MODULE__, worker_count, name: @me)
  end

  def done() do
    GenServer.cast(@me, :done)
  end

  def result(path, hash) do
    GenServer.cast(@me, {:result, path, hash})
  end

  # Server

  def init(worker_count) do
    Process.send_after(self(), :kickoff, 0)
    {:ok, worker_count}
  end

  def handle_cast(:done, _worker_count = 1) do
    report_results()
    System.halt(0)
  end

  def handle_cast(:done, worker_count) do
    {:noreply, worker_count - 1}
  end

  def handle_cast({:result, path, hash}, worker_count) do
    # Duper.Results holds the results that is gathered
    Duper.Results.add_hash_for(path, hash)
    {:noreply, worker_count}
  end

  def handle_info(:kickoff, worker_count) do
    IO.puts "Kicking off..."
    1..worker_count
    |> Enum.each(fn n -> Duper.WorkerSupervisor.add_worker(n) end)
    IO.puts "Worker count: #{worker_count}"
    {:noreply, worker_count}
  end

  defp report_results() do
    IO.puts "Results:\n"
    Duper.Results.find_duplicates()
    |> Enum.each(&IO.inspect/1)
  end


end
