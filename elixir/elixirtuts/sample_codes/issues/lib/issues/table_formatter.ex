defmodule Issues.TableFormatter do

  # import Enum, only: [each: 2, map: 2, map_join: 3, max: 1]

  def print_table_for_columns(row, headers) do
    table = for r <- row, do: for h <- headers, do: r[h]
    (for row <- [headers | table], do: Enum.join(row, " | "))
    |> Enum.join(" \n ")
  end

end
