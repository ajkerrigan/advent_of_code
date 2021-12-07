defmodule Day07 do
  def get_alignment_cost(positions, target, part) do
    Enum.map(
      positions,
      fn x ->
        if part == 1 do
          abs(x - target)
        else
          Enum.sum(0..abs(x - target))
        end
      end
    )
    |> Enum.sum()
  end

  def find_cheapest_alignment(positions, part) do
    avg = round(Enum.sum(positions) / length(positions))
    maxdev = Enum.max(Enum.map(positions, fn x -> abs(avg - x) end))

    Enum.reduce_while(0..maxdev, nil, fn i, acc ->
      targets =
        if i == 0 do
          [avg]
        else
          [avg + i, avg - i]
        end

      new_min =
        Enum.map(targets, fn n ->
          Day07.get_alignment_cost(positions, n, part)
        end)
        |> Enum.min()

      if new_min < acc do
        {:cont, new_min}
      else
        {:halt, acc}
      end
    end)
  end
end

positions =
  IO.gets(nil)
  |> String.trim()
  |> String.split(",", trim: true)
  |> Stream.map(&String.to_integer(&1))
  |> Enum.to_list()

IO.puts("Part 1: #{Day07.find_cheapest_alignment(positions, 1)}")
IO.puts("Part 2: #{Day07.find_cheapest_alignment(positions, 2)}")
