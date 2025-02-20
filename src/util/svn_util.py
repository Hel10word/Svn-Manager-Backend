from urllib.parse import unquote
import subprocess
import xml.etree.ElementTree as ET
from collections import OrderedDict
from datetime import datetime

from src.manager.config_manager import ConfigManager
from src.module.config.config_enum import ConfigEnum
from src.module.manager_exception import ManagerException
from src.module.svn_log_object import SvnLogObject
from src.module.svn_object import SvnObject


class SvnUtil:

    @staticmethod
    def _get_def_user(username: str = None, password: str = None) -> (str, str):
        envConfig = ConfigManager.get(ConfigEnum.ENV)
        if username is None:
            username = envConfig.defUsername
            password = envConfig.defPassword
        if password is None:
            raise ValueError("Password cannot be None.")
        return username, password

    @staticmethod
    def _get_def_svn(path: str = None) -> str:
        envConfig = ConfigManager.get(ConfigEnum.ENV)
        if path is not None:
            svnPath = f"{envConfig.baseSvnUrl}{path}"
        else:
            svnPath = envConfig.baseSvnUrl
        return svnPath

    @staticmethod
    def parse_date(dateStr: str) -> str:
        # SVN日期字符串可能会包含例如“+0800 (周四, 11 7月 2024)”结尾的时区和日期信息。
        # 只解析并返回符合 "%Y-%m-%d %H:%M:%S" 格式的日期部分。
        try:
            # 尝试解析标准SVN日期格式
            dateTimeObj = datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S %z')
        except ValueError:
            # 移除 "(周四, 11 7月 2024)" 这样的非标准结尾后再次尝试
            dateStrCleaned = dateStr.split(' (')[0]  # 截取到时区信息之前的部分
            dateTimeObj = datetime.strptime(dateStrCleaned, '%Y-%m-%d %H:%M:%S %z')
        return dateTimeObj.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def check_connection(username: str = None, password: str = None) -> bool:
        basePath = SvnUtil._get_def_svn()
        username, password = SvnUtil._get_def_user(username=username, password=password)
        try:
            result = subprocess.run(
                ["svn", "info", basePath, "--username", username, "--password", password, "--non-interactive",
                 "--no-auth-cache"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                # encoding='utf-8'
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to connect to SVN: {e.stderr.decode().strip()}")
            return False

    @staticmethod
    def check_access(svnRepoPath: str, username: str = None, password: str = None) -> bool:
        svnUrl = SvnUtil._get_def_svn(path=svnRepoPath)
        username, password = SvnUtil._get_def_user(username=username, password=password)
        try:
            result = subprocess.run(
                ["svn", "list", svnUrl, "--depth", "empty", "--username", username, "--password", password,
                 "--non-interactive", "--no-auth-cache"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                # encoding='utf-8'
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Access denied or path does not exist: {e.stderr.decode().strip()}")
            return False

    @staticmethod
    def list_locked_files(svnRepoPath: str, username: str = None, password: str = None
                          , depth: str = "immediates") -> list[SvnObject]:
        svnUrl = SvnUtil._get_def_svn(path=svnRepoPath)
        username, password = SvnUtil._get_def_user(username=username, password=password)
        try:
            # 使用 svn info 和 --show-locks 参数来获取锁定的文件列表和详细信息
            # -r
            #       HEAD 表示 获取所有人的锁信息 , 因为默认只获取本地锁信息
            # --depth
            #       empty (只包含目录本身,不包含目录下的文件)
            #       files (包含目录和目录下的文件,不包含子目录)
            #       immediates (包含目录和目录下的文件及子目录 , 但不对目录进行递归)
            #       infinity (默认 ; 包含整个目录树)
            result = subprocess.run(
                ["svn", "info", svnUrl, "-r", "HEAD", "--depth", depth, "--username", username, "--password",
                 password, "--no-auth-cache", "--xml"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,  # 确保文本输出模式
                check=True,
                encoding='utf-8'
            )

            lockedObjects = []

            root = ET.fromstring(result.stdout)

            # 遍历所有的 logentry 元素
            for entry in root.findall('entry'):
                name = entry.get('path')
                kind = entry.get('kind')
                svnPath = unquote(entry.find('url').text)
                svnRelativePath = unquote(entry.find('relative-url').text.removeprefix('^'))
                lastCommit = entry.find('commit')
                lastChangedAuthor = ""
                lastChangedDate = ""
                if lastCommit:
                    lastChangedAuthor = lastCommit.find('author').text
                    lastChangedDate = lastCommit.find('date').text.removeprefix('Z')

                lock = entry.find('lock')
                lockAuthor = ""
                lockDate = ""
                lockComment = ""
                if lock:
                    lockAuthor = lock.find('owner').text
                    lockDate = lock.find('created').text.removeprefix('Z')
                    lockCommentObj = lock.find('comment')
                    if lockCommentObj is not None and lockCommentObj.text:
                        lockComment = lockCommentObj.text

                lockedObjects.append(SvnObject(name=name, svnPath=svnPath, svnRelativePath=svnRelativePath, type=kind,
                                               lastChangedAuthor=lastChangedAuthor, lastChangedDate=lastChangedDate,
                                               lockAuthor=lockAuthor, lockDate=lockDate, lockComment=lockComment))

        except subprocess.CalledProcessError as e:
            print(f"Failed to list locked files: {e.stderr.strip()}")
            # return []
            raise ManagerException(message=f"Failed to list locked files: {e.stderr.strip()}")

        return lockedObjects

    @staticmethod
    def lock_files(svnRepoPaths: list[str], username: str = None, password: str = None,
                   comment: str = 'Locking files') -> (list, list):
        """
        Lock multiple files or directories in SVN.
        """

        success = []
        failed = []

        unlockObject = {}
        for svnRepoPath in svnRepoPaths:
            svnObjectList = SvnUtil.list_locked_files(svnRepoPath, username, password, "infinity")
            for svnObject in svnObjectList:
                # 如果文件已经被加锁 则跳过
                if svnObject.lockAuthor:
                    failed.append(svnObject)
                    continue
                # 这儿需要考虑 是否只过滤 文件类型
                if svnObject.type == 'file':
                    unlockObject[svnObject.svnRelativePath] = svnObject
                pass
            pass

        for svnPath, svnObject in unlockObject.items():
            svnUrl = SvnUtil._get_def_svn(path=svnPath)
            try:
                subprocess.run(
                    ["svn", "lock", svnUrl, "--force-log", "-m", comment, "--username", username, "--password",
                     password, "--no-auth-cache"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8'
                )
                success.append(svnObject)
            except subprocess.CalledProcessError as e:
                failed.append(svnObject)
                print(f"Failed to lock file: {svnPath}, Error: {e.stderr.strip()}")
                # return False  # 或收集失败的文件
                # raise ManagerException(message=f"Failed to lock file: {svnPath}, Error: {e.stderr.strip()}")
        return success, failed

    @staticmethod
    def unlock_files(svnRepoPaths: list[str], username: str = None, password: str = None, force: bool = False) -> (list, list):
        """
        Unlock multiple files or directories in SVN.
        """
        lockObject = {}
        for svnRepoPath in svnRepoPaths:
            svnObjectList = SvnUtil.list_locked_files(svnRepoPath, username, password, "infinity")
            for svnObject in svnObjectList:
                # 这儿需要考虑 是否只过滤 文件类型
                if svnObject.lockAuthor:
                    lockObject[svnObject.svnRelativePath] = svnObject
                pass
            pass

        success = []
        failed = []
        for svnPath, svnObject in lockObject.items():
            svnUrl = SvnUtil._get_def_svn(path=svnPath)
            try:
                subprocess.run(
                    ["svn", "unlock", svnUrl, "--username", username, "--password", password, "--no-auth-cache"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8'
                )
                success.append(svnObject)
            except subprocess.CalledProcessError as e:
                failed.append(svnObject)
                print(f"Failed to unlock file: {svnUrl}, Error: {e.stderr.strip()}")
                # raise ManagerException(message=f"Failed to unlock file: {svnUrl}, Error: {e.stderr.strip()}
                continue
        return success, failed

    @staticmethod
    def view_logs(svnRepoPaths: list[str], username: str = None, password: str = None):
        """
        View logs from multiple paths in SVN.
        """
        logEntries = {}
        for svnRepoPath in svnRepoPaths:
            svnUrl = SvnUtil._get_def_svn(path=svnRepoPath)
            try:
                result = subprocess.run(
                    ["svn", "log", "-l", "15", "-v", svnUrl, "--username", username, "--password", password,
                     "--no-auth-cache", "--xml"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8'
                )

                root = ET.fromstring(result.stdout)
                # 初始化存放所有 log entries 的列表

                # 遍历所有的 logentry 元素
                for log in root.findall('logentry'):
                    revision = int(log.get('revision'))
                    author = log.find('author').text
                    date = log.find('date').text.removeprefix('Z')
                    msg = log.find('msg').text

                    # 创建 日志对象
                    logObj = logEntries.get(revision)
                    if logObj is None:
                        logObj = SvnLogObject()
                        logObj.revision = revision
                        logObj.author = author
                        logObj.date = date
                        logObj.comment = msg
                    if logObj.svnPaths is None:
                        logObj.svnPaths = {}
                    if logObj.svnSelectPaths is None:
                        logObj.svnSelectPaths = {}
                    # 遍历所有的 path 元素
                    for path in log.find('paths'):
                        kind = path.get('kind')
                        action = path.get('action')
                        svnPath = path.text
                        if logObj.svnPaths.get(svnPath) is None:
                            logObj.svnPaths[svnPath] = {'action': action, 'type': kind, 'path': svnPath}
                        if svnPath.startswith(svnRepoPath):
                            logObj.svnSelectPaths[svnPath] = {'action': action, 'type': kind, 'path': svnPath}
                    # 更新 日志对象
                    logEntries[revision] = logObj
            except subprocess.CalledProcessError as e:
                # 如果获取日志失败，则将错误信息添加到列表中
                print(f"Failed to get logs for {svnRepoPath}, Error: {e.stderr.strip()}")
                continue

        return OrderedDict(sorted(logEntries.items(), key=lambda x: x[0], reverse=True))
