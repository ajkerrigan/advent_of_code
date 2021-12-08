defmodule Part2 do
  def advance_days(fish_counts, ndays) do
    Enum.reduce(1..ndays, fish_counts, fn _, acc ->
      (tl(acc) ++ [hd(acc)])
      |> List.update_at(6, &(&1 + Enum.at(acc, 0)))
    end)
  end
end

start =
  IO.gets(nil)
  |> String.trim()
  |> String.split(",", trim: true)
  |> Stream.map(&String.to_integer(&1))
  |> Enum.frequencies()

fish_counts =
  for i <- 0..8 do
    Access.get(start, i, 0)
  end

Part2.advance_days(fish_counts, 256)
|> Enum.sum()
|> IO.inspect()
