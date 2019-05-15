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

defmodule Ex do

  def first_is_zero?(tuple_or_list)
  when elem(tuple_or_list, 0) == 0
  when hd(tuple_or_list) == 0 do
      true
  end

  def first_is_zero?(tuple_or_list) do
    false
  end

end

IO.puts "0: #{Math.zero?(0)}"
IO.puts "3: #{Math.zero?(3)}"

IO.puts "> tuple #{Ex.first_is_zero?({0, 1, 2, 3, 4})}"
IO.puts "> list #{Ex.first_is_zero?([0, 1, 2, 3, 4])}"
