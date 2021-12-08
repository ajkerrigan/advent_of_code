defmodule Part2 do
  def advance_days(fish_counts, ndays) do
    if ndays == 0 do
      fish_counts
    else
      (tl(fish_counts) ++ [hd(fish_counts)])
      |> List.update_at(6, &(&1 + Enum.at(fish_counts, 0)))
      |> advance_days(ndays - 1)
    end
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
