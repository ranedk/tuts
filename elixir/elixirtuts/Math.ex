defmodule Math do

    def zero?(0) do
        true
    end

    def zero?(x) when is_number(x) do
        false
    end

    def zero?(x) when is_number(x) and x == 3 do
        true
    end

end

IO.puts "0: #{Math.zero?(0)}"
IO.puts "3: #{Math.zero?(3)}"
IO.puts "0: #{Math.zero?('a')}"
IO.puts "0: #{Math.zero?([1,2,3])}"
