# Define an accumulator as {previous, count_of_increases}
Enum.reduce(IO.stream(:stdio, :line), {0, 0}, fn cur, acc ->
  i = String.to_integer(String.trim(cur))

  {prev, increases} = acc

  case i > prev do
    true when prev != 0 ->
      {i, increases + 1}

    _ ->
      {i, increases}
  end
end)
|> elem(1)
|> IO.inspect()
|> (&IO.puts("Part 1 answer: #{&1}")).()
