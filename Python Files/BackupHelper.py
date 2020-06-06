import os, shutil

class Checker:
    def __init__(self, src: str, dst: str, copy: bool = True, update: bool = True):
        self.filesToCopy = []
        self.filesCopied = []
        self.foldersToCopy = []
        self.foldersCopied = []
        self.filesToUpdate = []
        self.filesUpdated = []
        self.filesToRemove = []
        self.filesToRemove = []
        self.foldersToRemove = []
        self.foldersRemoved = []
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
            print(f'待复制文件：{len(self.filesToCopy)}项')
        if not update:
            print(f'待更新文件：{len(self.filesToUpdate)}项')
        if self.filesToRemove:
            print(f'待移除文件：{len(self.filesToRemove)}项')
        if self.foldersToRemove:
            print(f'待移除文件夹：{len(self.foldersToRemove)}项')


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
                        self.foldersToCopy.append((src_item, dst_item))
            else:
                if item in dst_list:
                    src_time = os.path.getmtime(src_item)
                    dst_time = os.path.getmtime(dst_item)
                    if src_time > dst_time:
                        if not update or not self.__update(src_item, dst_item):
                            self.filesToUpdate.append((src_item, dst_item))
                else:
                    if not copy or not self.__copyFile(src_item, dst):
                        self.filesToCopy.append((src_item, dst))
        for item in set(dst_list) - set(src_list):
            path = os.path.join(dst, item)
            if os.path.isdir(path):
                self.foldersToRemove.append(path)
            else:
                self.filesToRemove.append(path)

    def __copyFile(self, src, dst) -> bool:
        try:
            shutil.copy2(src, dst)
            print(f'{src}已复制')
            self.filesCopied.append((src, dst))
            return True
        except Exception as e:
            print(e)
            return False

    def __copyFolder(self, src, dst) -> bool:
        try:
            shutil.copytree(src, dst)
            print(f'{src}已复制')
            self.foldersCopied.append((src, dst))
            return True
        except Exception as e:
            print(e)
            return False

    def __update(self, src, dst) -> bool:
        try:
            shutil.copy2(src, dst)
            print(f'{src}已更新')
            self.filesUpdated.append((src, dst))
            return True
        except Exception as e:
            print(e)
            return False

    def __removeFile(self, path) -> bool:
        try:
            os.remove(path)
            print(f'{path}已删除')
            self.filesToRemove.append(path)
            return True
        except Exception as e:
            print(e)
            return False

    def __removeFolder(self, path) -> bool:
        try:
            shutil.rmtree(path)
            print(f'{path}已删除')
            self.foldersRemoved.append(path)
            return True
        except Exception as e:
            print(e)
            return False

    def copyFiles(self, skip = set()):
        failures = []
        for i, (src, dst) in enumerate(self.filesToCopy):
            if src in skip or dst in skip:
                continue
            if not self.__copyFile(src, dst):
                failures.append((src, dst))
        self.filesToCopy = failures
        return self

    def copyFolders(self, skip = set()):
        failures = []
        for src, dst in self.foldersToCopy:
            if src in skip or dst in skip:
                continue
            if not self.__copyFolder(src, dst):
                failures.append((src, dst))
        self.foldersToCopy = failures
        return self

    def update(self, skip = set()):
        failures = []
        for src, dst in self.filesToUpdate:
            if src in skip or dst in skip:
                continue
            if not self.__update(src, dst):
                failures.append((src, dst))
        self.filesToUpdate = failures
        return self

    def removeFiles(self, skip = set()):
        failures = []
        for path in self.filesToRemove:
            if path in skip:
                continue
            if not self.__removeFile(path):
                failures.append(path)
        self.filesToRemove = failures
        return self

    def removeFolders(self, skip = set()):
        failures = []
        for path in self.foldersToRemove:
            if path in skip:
                continue
            if not self.__removeFolder(path):
                failures.append(path)
        self.foldersToRemove = failures
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

    def ftc(self):
        '''filesToCopy'''
        self.__print(self.filesToCopy, '待复制文件：{0}项', '没有待复制的文件')

    def fc(self):
        '''filesToCopy'''
        self.__print(self.filesCopied, '已复制文件：{0}项', '没有已复制的文件')

    def fdtc(self):
        '''filesToCopy'''
        self.__print(self.foldersToCopy, '待复制文件夹：{0}项', '没有待复制的文件夹')

    def fdc(self):
        '''filesToCopy'''
        self.__print(self.foldersCopied, '已复制文件夹：{0}项', '没有已复制的文件夹')

    def ftu(self):
        '''filesToCopy'''
        self.__print(self.filesToUpdate, '待更新文件：{0}项', '没有待更新的文件')

    def fu(self):
        '''filesToCopy'''
        self.__print(self.filesUpdated, '已更新文件：{0}项', '没有已更新的文件')

    def ftr(self):
        '''filesToCopy'''
        self.__print(self.filesToRemove, '待移除文件：{0}项', '没有待移除的文件')

    def fr(self):
        '''filesToCopy'''
        self.__print(self.filesToRemove, '已移除文件：{0}项', '没有已移除的文件')

    def fdtr(self):
        '''filesToCopy'''
        self.__print(self.foldersToRemove, '待移除文件夹：{0}项', '没有待移除的文件夹')

    def fdr(self):
        '''filesToCopy'''
        self.__print(self.foldersRemoved, '已移除文件夹：{0}项', '没有已移除的文件夹')

if __name__ == '__main__':
    c = Checker(r'C:\Users\Seaky\Desktop\Media\Music',
                r'D:\Media\\Music',
                False,
                False)
