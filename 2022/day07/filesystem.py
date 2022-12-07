from dataclasses import dataclass, field


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
