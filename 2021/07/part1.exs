defmodule Part1 do
  def get_alignment_cost(positions, target) do
    Enum.map(
      positions,
      fn x ->
        abs(x - target)
      end
    )
    |> Enum.sum()
  end

  def find_cheapest_alignment(positions) do
    avg = (Enum.sum(positions) / length(positions)) |> Float.round()

    Enum.reduce_while(0..Enum.max_by(positions, fn x -> abs(avg - x) end), nil, fn i, acc ->
      targets = [avg + i, avg - i] |> Enum.dedup()

      new_min =
        Enum.map(targets, fn n ->
          Part1.get_alignment_cost(positions, n)
        end)
        |> Enum.min()

      if new_min < acc do
        {:cont, new_min}
      else
        {:halt, acc}
      end
    end)
    |> IO.inspect()
  end
end

IO.gets(nil)
|> String.trim
|> String.split(",", trim: true)
|> Stream.map(&String.to_integer(&1))
|> Enum.to_list
|> Part1.find_cheapest_alignment
