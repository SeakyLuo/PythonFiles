import os, shutil

class Checker:
    def __init__(self, src: str, dst: str, copy: bool = True, update: bool = True):
        self.__filesToCopy = []
        self.__filesCopied = []
        self.__foldersToCopy = []
        self.__foldersCopied = []
        self.__filesToUpdate = []
        self.__filesUpdated = []
        self.__filesToRemove = []
        self.__filesRemoved = []
        self.__foldersToRemove = []
        self.__foldersRemoved = []
        self.__src = src
        self.__dst = dst
        self.__copy = copy
        self.__update = update
        self.again(src, dst, copy, update)

    def again(self, src: str = None, dst: str = None, copy: bool = None, update: bool = None):
        if src != None: self.__src = src
        if dst != None: self.__dst = dst
        if copy != None: self.__copy = copy
        if update != None: self.__update = update
        self.__check(src, dst, copy, update)
        if not copy:
            print(f'待复制文件：{len(self.__filesToCopy)}项')
        if not update:
            print(f'待更新文件：{len(self.__filesToUpdate)}项')
        if self.__filesToRemove:
            print(f'待移除文件：{len(self.__filesToRemove)}项')
        if self.__foldersToRemove:
            print(f'待移除文件夹：{len(self.__foldersToRemove)}项')
        

    def __check(self, src, dst, copy, update):
        src_list = os.listdir(src)
        dst_list = os.listdir(dst)
        for item in src_list:
            src_item = os.path.join(src, item)
            dst_item = os.path.join(dst, item)
            if item.startswith('~$'):
                print(f'在{src}中检测到临时文件：{item}，已跳过')
                continue
            if os.path.isdir(src_item):
                if item in dst_list:
                    self.__check(src_item, dst_item, copy, update)
                else:
                    if not copy or not self.__copyFolder(src_item, dst_item):
                        self.__foldersToCopy.append((src_item, dst_item))
            else:
                if item in dst_list:
                    src_time = os.path.getmtime(src_item)
                    dst_time = os.path.getmtime(dst_item)
                    if src_time > dst_time:
                        if not update or not self.__update(src_item, dst_item):
                            self.__filesToUpdate.append((src_item, dst_item))
                else:
                    if not copy or not self.__copyFile(src_item, dst):
                        self.__filesToCopy.append((src_item, dst))
        for item in set(dst_list) - set(src_list):
            path = os.path.join(dst, item)
            if os.path.isdir(path):
                self.__foldersToRemove.append(path)
            else:
                self.__filesToRemove.append(path)

    def __copyFile(self, src, dst) -> bool:
        try:
            shutil.copy2(src, dst)
            print(f'{src}已复制')
            self.__filesCopied.append((src, dst))
            return True
        except Exception as e:
            print(e)
            return False

    def __copyFolder(self, src, dst) -> bool:
        try:
            shutil.copytree(src, dst)
            print(f'{src}已复制')
            self.__foldersCopied.append((src, dst))
            return True
        except Exception as e:
            print(e)
            return False

    def __update(self, src, dst) -> bool:
        try:
            shutil.copy2(src, dst)
            print(f'{src}已更新')
            self.__filesUpdated.append((src, dst))
            return True
        except Exception as e:
            print(e)
            return False

    def __removeFile(self, path) -> bool:
        try:
            os.remove(path)
            print(f'{path}已删除')
            self.__filesRemoved.append(path)
            return True
        except Exception as e:
            print(e)
            return False

    def __removeFolder(self, path) -> bool:
        try:
            shutil.rmtree(path)
            print(f'{path}已删除')
            self.__foldersRemoved.append(path)
            return True
        except Exception as e:
            print(e)
            return False

    def copyFiles(self, skip = set()):
        failures = []
        for i, (src, dst) in enumerate(self.__filesToCopy):
            if src in skip or dst in skip:
                continue
            if not self.__copyFile(src, dst):
                failures.append((src, dst))
        self.__filesToCopy = failures
        return self

    def copyFolders(self, skip = set()):
        failures = []
        for src, dst in self.__foldersToCopy:
            if src in skip or dst in skip:
                continue
            if not self.__copyFolder(src, dst):
                failures.append((src, dst))
        self.__foldersToCopy = failures
        return self

    def update(self, skip = set()):
        failures = []
        for src, dst in self.__filesToUpdate:
            if src in skip or dst in skip:
                continue
            if not self.__update(src, dst):
                failures.append((src, dst))
        self.__filesToUpdate = failures
        return self

    def removeFiles(self, skip = set()):
        failures = []
        for path in self.__filesToRemove:
            if path in skip:
                continue
            if not self.__removeFile(path):
                failures.append(path)
        self.__filesToRemove = failures
        return self

    def removeFolders(self, skip = set()):
        failures = []
        for path in self.__foldersToRemove:
            if path in skip:
                continue
            if not self.__removeFolder(path):
                failures.append(path)
        self.__foldersToRemove = failures
        return self

    def __print(self, lst, tMsg, fMsg):
        if lst:
            print(tMsg.format(len(lst)))
            if type(lst[0]) == str:
                for path in lst:
                    print(path)
            else:
                for src, dst in lst:
                    print(src)
        else:
            print(fMsg)

    def filesToCopy(self):
        self.__print(self.__filesToCopy, '待复制文件：{0}项', '没有待复制的文件')

    def filesCopied(self):
        self.__print(self.__filesCopied, '已复制文件：{0}项', '没有已复制的文件')

    def foldersToCopy(self):
        self.__print(self.__foldersToCopy, '待复制文件夹：{0}项', '没有待复制的文件夹')

    def foldersCopied(self):
        self.__print(self.__foldersCopied, '已复制文件夹：{0}项', '没有已复制的文件夹')

    def filesToUpdate(self):
        self.__print(self.__filesToUpdate, '待更新文件：{0}项', '没有待更新的文件')

    def filesUpdated(self):
        self.__print(self.__filesUpdated, '已更新文件：{0}项', '没有已更新的文件')

    def filesToRemove(self):
        self.__print(self.__filesToRemove, '待移除文件：{0}项', '没有待移除的文件')

    def filesRemoved(self):
        self.__print(self.__filesRemoved, '已移除文件：{0}项', '没有已移除的文件')

    def foldersToRemove(self):
        self.__print(self.__foldersToRemove, '待移除文件夹：{0}项', '没有待移除的文件夹')

    def foldersRemoved(self):
        self.__print(self.__foldersRemoved, '已移除文件夹：{0}项', '没有已移除的文件夹')

if __name__ == '__main__':
    c = Checker(r'C:\Users\Seaky\Desktop\Pics',
                r'E:\Pics',
                False,
                False)
