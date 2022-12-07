import sys
from dataclasses import dataclass, field
from pathlib import Path


def parse_term_output(data):
    parsed = []
    command, command_output = "", []
    for line in data.strip().splitlines():
        line = line.strip()
        tokens = line.split()
        if tokens[0] == "$":
            if command:
                parsed.append((command, command_output))
            command = tokens[1:]
            command_output = []
        else:
            command_output.append(tokens)
    if command:
        parsed.append((command, command_output))
    return parsed


@dataclass
class Entry:
    name: str


@dataclass
class Directory(Entry):
    contents: list[Entry] = field(default_factory=list)

    @property
    def size(self):
        return sum(c.size for c in self.contents)


@dataclass
class File(Entry):
    size: int


def build_filesystem(commands: list):
    fs = {}
    pwd = Directory("/")
    fs[pwd.name] = pwd
    for command, output in commands:
        cmd, *args = command
        match cmd:
            case "ls":
                for line in output:
                    size, name = line
                    if size == "dir":
                        entry = str(Path(pwd.name) / name)
                        pwd.contents.append(fs.setdefault(entry, Directory(entry)))
                    else:
                        entry = str(Path(pwd.name) / name)
                        pwd.contents.append(
                            fs.setdefault(entry, File(entry, int(size)))
                        )
            case "cd":
                if args[0] == "..":
                    new_pwd = pwd.name.rpartition("/")[0]
                elif "/" in args[0]:
                    new_pwd = args[0]
                else:
                    new_pwd = str(Path(pwd.name) / args[0])
                pwd = fs.setdefault(new_pwd, Directory(new_pwd))
    return fs


def part1(data: str):
    parsed = parse_term_output(data)
    fs = build_filesystem(parsed)
    total_size = 0
    for entry in fs.values():
        if isinstance(entry, File):
            continue
        if not (0 < entry.size <= 100000):
            continue
        total_size += entry.size
    return total_size


def part2(data: str):
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
