range, loops
regex
Type conversions, tuple to list and reverse


Good practices:

- Do not assign a value to a variable inside a code-block (if, case, cond, with, do etc.) which
is decalred/initialized outside the code-block. variables in code-block are local scoped to the block

Instead of

    line_no = 50
    result = nil
    # ...
    if (line_no == 50) do
        result = 50
    end
    IO.puts result

Use
    line_no = 50
    result =
        if line_no == 50 do
            50
        else
            nil
    IO.puts result

    line_no = 50
    result =
        case line_no do
            50 -> 50
            true -> nil
    IO.puts result


- 
