defmodule Chain do

    # counter receives and send to next pid
    def counter(next_pid) do
        receive do
            n ->
                send next_pid, n + 1
        end
    end

    # create "n" processes async
    def create_processes(n) do
        code_to_run = fn (_,send_to) ->
            spawn(Chain, :counter, [send_to])
        end

        # Cool way to use reduce to spawn and get the last process
        last = Enum.reduce(1..n, self(), code_to_run)

        # start the count by sending a zero to the last process
        send(last, 0)

        # and wait for the result to come back to us
        # using a is_integer guard since some beam VMs have a bug
        # where they send a message to mark process completion
        receive do
            final_answer when is_integer(final_answer) ->
                "Result is #{inspect(final_answer)}"
        end
    end

    # timer is erlang module, tc calculates the time to run
    def run(n) do
        :timer.tc(Chain, :create_processes, [n])
        |> IO.inspect
    end
end

Chain.run(100000)
