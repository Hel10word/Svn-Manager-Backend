import json
from dataclasses import dataclass, asdict


@dataclass
class SvnLogObject:
    # 版本号
    revision: int = 0
    # 提交包含的 SVN 路径
    svnPaths: dict = None
    # 包含查询的 SVN 路径
    svnSelectPaths: dict = None
    # 提交作者
    author: str = ""
    # 提交日期
    date: str = ""
    # 提交备注
    comment: str = ""

    def to_str(self) -> str:
        return (f"SvnLogObject:\n"
                f"  Revision: {self.revision}\n"
                f"  Svn Paths: {self.svnPaths}\n"
                f"  Author: {self.author}\n"
                f"  Date: {self.date}\n"
                f"  Comment: {self.comment}")

    def to_json(self):
        return json.dumps(asdict(self))
