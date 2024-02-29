import dataclasses
import os


@dataclasses.dataclass
class ModuleSource:
    uri: str
    contents: str = ""


class FileSource(ModuleSource):
    def __init__(self, *path_elems: str):
        src = os.path.join(*path_elems)
        if not os.path.isabs(src):
            p = os.getcwd()
            src = os.path.join(p, src)
        super().__init__(f"file://{src}")


class TextSource(ModuleSource):
    def __init__(self, text: str):
        super().__init__("repl:text", text)


class UriSource(ModuleSource):
    def __init__(self, uri: str):
        super().__init__(uri)
