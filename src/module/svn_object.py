import json
from dataclasses import dataclass, asdict


@dataclass
class SvnObject:
    # 文件名
    name: str = ""
    # SVN 完整路径
    svnPath: str = ""
    # SVN 相对路径
    svnRelativePath: str = ""
    # 电脑实际路径
    # workingPath: str
    # 文件类型 : dir | file
    type: str = ""
    # 上次修改的作者
    lastChangedAuthor: str = ""
    # 上次修改的日期
    lastChangedDate: str = ""
    # 锁的作者
    lockAuthor: str = ""
    # 锁的时间
    lockDate: str = ""
    # 锁的备注
    lockComment: str = ""

    def to_str(self) -> str:
        return (f"SvnObject:\n"
                f"  Name: {self.name}\n"
                f"  SVN Path: {self.svnPath}\n"
                f"  SVN Relative Path: {self.svnRelativePath}\n"
                f"  Type: {self.type}\n"
                f"  Last Changed Author: {self.lastChangedAuthor}\n"
                f"  Last Changed Date: {self.lastChangedDate}\n"
                f"  Lock Author: {self.lockAuthor}\n"
                f"  Lock Date: {self.lockDate}\n"
                f"  Lock Comment: {self.lockComment}")

    def to_json(self):
        return json.dumps(asdict(self))
