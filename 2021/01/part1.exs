IO.stream(:stdio, :line)
|> Stream.map(fn x -> String.to_integer(String.trim(x)) end)

# Define an accumulator as {previous_number, count_of_increases}
|> Enum.reduce({0, 0}, fn cur, acc ->
  {prev, increase_count} = acc

  if cur > prev and prev != 0 do
    {cur, increase_count + 1}
  else
    {cur, increase_count}
  end
end)
|> elem(1)
|> IO.inspect()
|> (&IO.puts("Part 1 answer: #{&1}")).()
