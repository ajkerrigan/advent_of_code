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
class FilesystemEntry:
    """A single filesystem object"""

    name: str

    @property
    def type(self):
        raise NotImplemented


@dataclass
class File(FilesystemEntry):
    """A single file in a filesystem"""

    size: int

    @property
    def type(self):
        return "file"


@dataclass
class Directory(FilesystemEntry):
    """A directory in a filesystem

    Directories contain 0 or more children.
    """

    contents: list[FilesystemEntry] = field(default_factory=list)

    @property
    def size(self):
        """The total size of a directory's contents."""
        return sum(c.size for c in self.contents)

    @property
    def type(self):
        return "directory"


def build_filesystem(commands: list) -> dict[str, FilesystemEntry]:
    """Build a filesystem using command output

    Iterate over a list of commands and their
    output, using it to build a dict whose keys
    are path names and values are file/directory
    details.
    """
    fs = {}
    pwd = Directory("/")
    fs[pwd.name] = pwd
    for command, output in commands:
        cmd, *args = command
        match cmd:
            case "ls":
                for line in output:
                    size, name = line
                    entry = str(Path(pwd.name) / name)
                    if size == "dir":
                        pwd.contents.append(fs.setdefault(entry, Directory(entry)))
                    else:
                        pwd.contents.append(
                            fs.setdefault(entry, File(entry, int(size)))
                        )
            case "cd":
                if args[0] == "..":
                    new_pwd = str(Path(pwd.name).parent)
                elif "/" in args[0]:
                    new_pwd = str(Path(args[0]))
                else:
                    new_pwd = str(Path(pwd.name) / args[0])
                pwd = fs.setdefault(new_pwd, Directory(new_pwd))
    return fs


def part1(data: str) -> int:
    """Sum of small directories

    Sum the sizes of all directories whose
    individual sizes are less than 100000.
    """
    parsed = parse_term_output(data)
    fs = build_filesystem(parsed)
    total_size = 0
    for entry in fs.values():
        if not entry.type == "directory":
            continue
        if not (0 < entry.size <= 100000):
            continue
        total_size += entry.size
    return total_size


def part2(data: str) -> int:
    """Delete a directory to save space

    Find the smallest individual directory
    that can be deleted to free up enough space
    to install an update.
    """
    parsed = parse_term_output(data)
    fs = build_filesystem(parsed)
    required_space = 30000000
    total_space = 70000000
    free_space = total_space - fs["/"].size
    space_to_free = required_space - free_space
    candidate_sizes = [
        entry.size
        for entry in fs.values()
        if isinstance(entry, Directory) and entry.size >= space_to_free
    ]
    return min(candidate_sizes)


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
