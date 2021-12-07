defmodule Part1 do
  def advance_days(fish, ndays) do
    IO.inspect({ndays, length(Enum.to_list(fish))})
    case ndays do
      0 ->
        fish

      n when n > 0 ->
        advance_days(
          Enum.flat_map(fish, fn x ->
            case x do
              0 -> [6, 8]
              _ -> [x - 1]
            end
          end),
          n - 1
        )
    end
  end
end

IO.gets(nil)
|> String.trim
|> String.split(",", trim: true)
|> Stream.map(&String.to_integer(&1))
|> Part1.advance_days(80)
|> length
|> IO.inspect
