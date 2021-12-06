# Define an accumulator as [last_value, [list_of_increasing_values]]
Enum.reduce(IO.stream(:stdio, :line), [0, []], fn cur, acc ->
  i = String.to_integer(String.trim(cur))

  # Set the accumulator's first element to the current number.
  #
  # Prepend the current number to the list in the second element
  # only if it is greater than the previous number.
  case i > hd(acc) do
    true when hd(acc) != 0 ->
      [i, [i | List.last(acc)]]

    _ ->
      [i, List.last(acc)]
  end
end)
|> List.last()
|> IO.inspect()
|> (&(IO.puts("Part 1 answer: #{length(&1)}"))).()
