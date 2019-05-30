defmodule Sequence.Server do
  use GenServer

  def init(initial_number) do
    {:ok, initial_number}
  end

  def handle_call(:next_number, _client, initial_number) do
    {:reply, initial_number, initial_number + 1}
  end

end
