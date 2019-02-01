import os, shutil

media_fmt = ['.mkv', '.mp4', '.avi', '.rmvb', '.mp3', '.m4a']
isMedia = lambda x: have(x.lower()).any(*media_fmt)
fiindFmt = lambda x: have(x.lower()).which(*media_fmt)
deformat = lambda x: x[:-len(fiindFmt(x))]

class rename:
    def __init__(self, path = ''):
        '''Default path is set to "D:\\Media".'''
        self.path = default_path = 'D:\\Media\\'
        if path:
            path = path[have(path).start('\\'):].strip()
            self.path = os.path.normcase(path)
        if not os.path.exists(self.path):
            if not have(self.path).start(default_path) and os.path.exists(default_path+self.path):
                self.path = default_path+self.path
            else:
                raise Exception('Path does not exist!~')
        os.chdir(self.path)
        self.dir = [ file for file in os.listdir() if isMedia(file)]

    def remove(self, *args):
        '''Remove the occurences of some string from a files' name in self.path.'''
        if args == ():
            print('Please input the string that you want to remove!')
            return
        for file in self.dir:
            new_name = deformat(file)
            if len(args) == 1 and type(args[0]) == int:
                new_name = new_name[args[0]:]
            else:
                for arg in args:
                    if type(arg) != str:
                        arg = repr(arg)
                    new_name = new_name.replace(arg, '')
            new_name+ = fiindFmt(file)
            if new_name != file and new_name in self.dir:
                print(new_name+' already exists!')
            else:
                os.rename(file, new_name)
        self.succeed()

    def replace(self, old, new = ''):
        '''Replace all the occurence of old with new.'''
        for file in self.dir:
            new_name = deformat(file).replace(old, new) + fiindFmt(file)
            if new_name != file and new_name in self.dir:
                print(f'{new_name} already exists!')
            else:
                os.rename(file, new_name)
        self.succeed()

    def move(self, dst, *args):
        '''Move files from self.path to dst.
           Put common occurences in args if file names are featured.'''
        dst = os.path.normcase(dst)
        for file in self.dir:
            if have(file).all(*args):
                shutil.move(f'{self.path}\\{file}', dst)
        self.succeed()

    def delete(self, *args):
        '''Delete files in self.path.
           Put common occurences in args if file names are featured.'''
        for file in self.dir:
            if isMedia(file) and have(deformat(file)).all(*args):
                os.remove(file)
        self.succeed()

    def succeed(self):
        self.dir = [file for file in os.listdir() if isMedia(file)]
        print('成功啦~')

if __name__ == '__main__':
    r = rename('C:\\Users\\Seaky\\Music\\iTunes\\iTunes Media\\Music\\Victor Oladipo\\Songs for You')
    r.remove(3)
##    r.move('D:\\Media\\Music\\Chinese', '.mp3')
##    r.replace(old = 'Game.of.Thrones.',
##              new = 'Game of Thrones ')
##    r.delete('.mp4.')

