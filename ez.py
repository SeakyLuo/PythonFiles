import os
import datetime
import time
import urllib.request, urllib.parse
import platform
import threading, subprocess, zipfile, ntpath, shutil
from json import loads, dumps
from atexit import register
from collections.abc import Iterable
from collections import Counter
from functools import reduce
from types import GeneratorType

desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
DataTypeError = TypeError('Unsupported data type.')

def summation(iterable):
    '''Call the __add__ or update function of the iterable.'''
    if isinstance(iterable, GeneratorType):
        iterable = list(iterable)
        typ = type(iterable[0])
    else:
        typ = type(iterable[0])
    if '__add__' in dir(typ):
        return reduce(typ.__add__, iterable)
    if 'update' in dir(typ):
        def u(a, b):
            a.update(b)
            return a
        return reduce(u, iterable)
    raise DataTypeError

def countLines(path, filetype):
    '''Count the lines of all the files with the specified type in the path.'''
    count = 0
    for item in os.listdir(path):
        directory = os.path.join(path, item)
        if os.path.isdir(directory):
            for script in os.listdir(directory):
                if script.endswith(filetype):
                    count += fread(os.path.join(directory, script), False).count('\n')
        elif os.path.isfile(item) and item.endswith(filetype):
            count += fread(directory, False).count('\n')
    return count

class Settings:
    '''Recommend passing __file__ to file'''
    def __init__(self, file, settingsName = 'settings.json'):
        self.path = os.path.dirname(file)
        self.settingsName = settingsName
        self.settingsFile = os.path.join(self.path, self.settingsName)
        self.load()
        register(self.save)

    def setdefault(self, key, value):
        return self.settings.setdefault(key, value)

    def set(self, key, value):
        self.__setitem__(key, value)

    def setSettingOptions(self, settingOptions):
        for key in self.settings.copy():
            if key not in settingOptions:
                del self.settings[key]

    def get(self, key, default):
        return self.settings.get(key, default)

    def __getitem__(self, key):
        return self.settings[key]

    def __setitem__(self, key, value):
        self.settings[key] = value

    def __str__(self):
        return str(self.settings)

    def __repr__(self):
        return repr(self.settings)

    def load(self):
        try:
            self.settings = loads(fread(self.settingsFile, False))
        except (FileNotFoundError, TypeError):
            self.settings = {}

    def save(self):
        fwrite(self.settingsFile, dumps(self.settings))

def tryEval(string):
    '''Use eval() without dealing with exceptions.'''
    try: return eval(string)
    except: return string

def translate(string, to_l = 'zh', from_l = 'en'):
    '''Translate string from from_l language to to_l language'''
    if not string: return ''
    header = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
    flag = 'class="t0">'
    query = urllib.parse.quote(string, encoding = 'utf-8')
    url = "https://translate.google.cn/m?hl=%s&sl=%s&q=%s" % (to_l, from_l, query)
    request = urllib.request.Request(url, headers = header)
    page = urllib.request.urlopen(request).read().decode('utf-8')
    target = page[page.find(flag) + len(flag):]
    target = target.split("<")[0]
    target = sub(target, "&#39;", "'")
    return target

def handlepy(directory, func, reminder = False):
    ''' Do something, meaning that func(directory), to a py file or a folder of py files.
        func must has exactly one argument filename.
        '''
    if os.path.isfile(directory) and directory.endswith('.py'):
        if reminder:
            print('File detected')
        func(directory)
    elif os.path.isdir(directory):
        if reminder:
            print('Folder detected')
        for file in os.listdir(directory):
            if file.endswith('.py'):
                if reminder:
                    print(file)
                func(os.path.join(directory, file))
    else:
        raise Exception('Invalid directory!')

def exportpy(directory, withConsole, zipFile = True, reminder = False):
    '''Exports a GUI python app.'''
    ## Add '-noconfirm' ?
    path = os.path.dirname(directory)
    args = ['pyinstaller', '--onefile', '--distpath', path, '--workpath', path, '--specpath', path, '--noconsole']
    if withConsole:
        args.pop()
    def export(filename):
        subprocess.run(args + [filename])
        if not zipFile: return
        currDir = os.getcwd()
        path, file = ntpath.split(filename)
        os.chdir(path)
        prefix = find(file).before('.py')
        zipname = prefix + '.zip'
        with zipfile.ZipFile(zipname, 'w') as zipFile:
            for f in [prefix + '.exe', prefix + '.spec']:
                zipFile.write(f)
                os.remove(f)
            for f in os.listdir(prefix):
                zipFile.write(os.path.join(prefix, f))
            shutil.rmtree(prefix)
        os.chdir(currDir)
    threading.Thread(target = lambda directory, func, reminder: handlepy(directory, func, reminder), \
                     args = (directory, export, reminder)).start()

def py2pyw(directory, pywname = '', reminder = False):
    ''' Converts a py file or a folder of py files to pyw files.
        pywname is the of pyw file and is only available when converting a file.
        pywname is empty, set to pyw filename wil be set to the name of py file.'''
    suffix = '.pyw'
    if pywname and not pywname.endswith(suffix): pywname += suffix
    threading.Thread(target = lambda directory, func, reminder: handlepy(directory, func, reminder), \
                     args = (directory, lambda filename: fwrite(pywname or filename + 'w', fread(filename, False)), reminder)).start()

def rmlnk(path = None):
    ''' Remove "- 快捷方式"'''
    for folder in os.listdir(path):
        folder = os.path.join(path, folder)
        if folder.endswith('.lnk'):
            os.rename(folder, folder.replace(' - 快捷方式', ''))

def chdt():
    '''Change current directory to Desktop'''
    os.chdir(desktop)

def copyToClipboard(text):
    ''' Copy text to clipboard. I don't care about Linux.'''
    text = str(text)
    system = platform.system()
    if system == 'Windows':
        try:
            from win32 import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
        except ModuleNotFoundError:
            # Solution: https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard-on-windows-using-python/
            from tkinter import Tk
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(text)
            r.update() # now it stays on the clipboard after the window is closed
            r.destroy()
    elif system == 'Darwin':
        process = subprocess.Popen('pbcopy', env = {'LANG': 'en_US.UTF-8'}, stdin = subprocess.PIPE)
        process.communicate(text.encode('utf-8'))

## abbreviation
cpc = copyToClipboard

def checkfolders(folder1, folder2):
    '''Check whether folder1 is exactly the same as folder2'''
    l1 = os.listdir(folder1)
    l2 = os.listdir(folder2)
    if l1 != l2:
        return False
    for f in l1:
        p1 = os.path.join(folder1, f)
        if os.path.isdir(p1):
            p2 = os.path.join(folder2, f)
            if not checkfolders(p1, p2):
                return False
    return True

def findFilePath(filename, path = ''):
    '''Default path: All
       Find the first occurence only.
       Use smaller range to have faster searching speed.'''
    if not path:
        c = findFilePath(filename, 'C:\\')
        if c:
            return c
        d = findFilePath(filename, 'D:\\')
        if d:
            return d
        return False
    path = os.path.normcase(path)
    try:
        filelist = os.listdir(path)
    except PermissionError:
        return
    if filename in filelist:
        return path
    for f in filelist:
        p = os.path.join(path, f)
        if os.path.isdir(p):
            result = findFilePath(filename, p)
            if result:
                return result
    return False

def timer(func, iterations = 1000, *args):
    '''If func has arguments, put them into args.'''
    t = time.time()
    for i in range(int(iterations)):
        func(*args)
    return time.time() - t

def fread(filename, evaluate = True, coding = 'utf8'):
    '''Read the file that has the filename.
        Set evaluate to true to evaluate the content.
        Default coding: utf8.'''
    file = open(filename, encoding = coding)
    content = file.read()
    if evaluate:
        try: content = eval(content)
        except: pass
    file.close()
    return content

def fwrite(filename, content, mode = 'w', coding = 'utf8'):
    ''' Write the file that has the filename with content.
        Default mode: "w"
        Default coding: utf8.'''
    file = open(filename, mode, encoding = coding)
    if type(content) != str:
        content = repr(content)
    file.write(content)
    file.close()

def fcopy(src, dst, coding = 'utf8'):
    '''Copy a file.
       Requires source directory(src) and destination directory(dst).
       Default coding: utf8.'''
    filename = src[:find(src).last('\\')]
    fwrite(dst if dst.endswith(filename) else os.path.join(dst, filename), fread(src, coding), coding = coding)

def advancedSplit(obj, *sep):
    '''Can have multiple seperators.'''
    if sep == () or len(sep) == 1:
        return obj.split(*sep)
    word = ''
    lst = []
    for ch in obj:
        word += ch
        f = contains(word, *sep)
        if f:
            word = without(word, *f)
            if word:
                lst.append(word)
                word = ''
    if word:
        lst.append(word)
    return lst
##abbreviation
asplit = advancedSplit

def similar(obj1, obj2, capital = True):
    '''Check the similarities of two strings.
        Set capital to False to ignore capital.'''
    def grade(o1, o2):
        ## Let o1 >= o2
        if o1 == o2:
            return 1
        if o1 == '' or o2 == '':
            return 0
        len_o1 = len(o1)
        len_o2 = len(o2)
        score = len_o2 / len_o1
        if score == 1:
            result = sum((i == j) + (i != j) * (i.lower() == j.lower()) * 0.9 for i, j in zip(o1, o2)) / len_o1
            return eval(format(result, '.4f'))
        if len_o2 <= 15 and score > 0.6:
            ps = list(reversed(find(o2).power_set() + [o2]))
            maxLen = 0
            for i, sub in enumerate(ps):
                subLen = len(sub)
                if sub in o1 and maxLen < subLen:
                    maxLen = subLen
                try:
                    if i < 2 ** len(o2) - 2 and maxLen > len(ps[i + 1]):
                        break
                except IndexError:
                    break
            else:
                return 0
            score = maxLen / len_o1
        if o2.lower() in o1.lower():
            if o2 in o1:
                if o1.startswith(o2):
                    score *= 1.5
                else:
                    pass
            else:
                score *= 0.9
        else:
            d1, d2 = find(o1).count(), find(o2).count()
            sd = set(d2.keys()).difference(set(d1.keys()))
            if len(sd) == len(d2):  ##完全不一样
                return 0
            for key in d1:
                if key in d2:
##                    score *= (d2[key] / d1[key]) ** ((d1[key] >= d2[key]) * 2 - 1)
                    if d1[key] > d2[key]:
                        score *= d2[key]/d1[key]
                    else:
                        score *= d1[key]/d2[key]
            score *= 1 - sum([d2.get(item) for item in sd ]) / len_o2
##            不乘0.8的话similar('12345678', '23')跟similar('12345678', '24')都是0.25
##          可以用距离
            score *= 0.8
        return eval(format(score, '.4f'))

    if type(obj1) != str or type(obj2) != str:
        raise DataTypeError
    if not capital:
        obj1 = obj1.lower()
        obj2 = obj2.lower()
    if len(obj1) >= len(obj2):
        return grade(obj1, obj2)
    else:
        return grade(obj2, obj1)

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def similar2(obj1, obj2, capital = True):
    '''Check the how similar string obj1 to obj2 is using Levenshtein Distance.
        Set capital to False to ignore capital.'''
    if capital:
        obj1 = obj1.lower()
        obj2 = obj2.lower()
    ld = levenshteinDistance(obj1, obj2)
    return 1 - ld / len(obj2)    

def predir():
    '''Go back to the parent folder (not root).'''
    path = os.getcwd()
    os.chdir(path[:find(path).last('\\')])

def isMultiple(obj1, obj2):
    '''Check whether obj1 is the multiple of obj2'''
    type1 = type(obj1)
    assert type1 == type(obj2), 'Inconsistent data type'
    if type1 == int: return obj1 % obj2 == 0
    length1 = len(obj1)
    length2 = len(obj2)
    if length1 % length2:
        return False
    return all(obj1[i:i + length2] == obj2 for i in range(0, length1, length2))

def contains(obj, *args):
    return any(arg in obj for arg in args)

class find:
    '''A helper class which finds something in the object.'''
    def __init__(self, obj):
        self.type = type(obj)
        self.empty = self.type()
        self.obj = obj
        if not isinstance(obj, Iterable):
            print('Unsupported data type automatically is converted to str.')
            self.obj = repr(obj)
            self.type = str

    def before(self, occurrence):
        '''Return the obj before the occurrence.'''
        try:
            return self.obj[:self.obj.index(occurrence)]
        except:
            raise DataTypeError

    def after(self, occurrence):
        '''Return the obj after the occurrence.'''
        try:
            return self.obj[self.obj.index(occurrence) + (self.type != str or len(occurrence)):]
        except:
            raise DataTypeError

    def all(self, occurrence):
        '''Find all the occurring indices in an obj.'''
        if self.type == str:
            return [ idx for idx in range(len(self.obj)) if self.obj[idx:].startswith(occurrence) ]
        try:
            return [ idx for idx in range(len(self.obj)) if self.obj[idx] == occurrence ]
        except:
            raise DataTypeError

    def nth(self, occurrence, nth = 1):
        '''Find the nth occurring index in an obj.'''
        try:
            return self.all(occurrence)[nth - 1]
        except IndexError:
            return -1

    def between(self, obj1 = None, obj2 = None):
        '''Return the obj between obj1 and obj2 (not included).
           Start from the first occurrence.'''
        try:
            start = 0
            if obj1 != None:
                start = self.obj.index(obj1) + (len(obj1) if self.type == str else 1)
            end = self.obj[start:].index(obj2) + start if obj2 != None else None
            return self.obj[start:end]
        except ValueError:
            return self.empty
        except:
            raise DataTypeError

    def consecutive(self):
        '''Count the longest consecutive occurrences.'''
        if self.type == dict:
            raise DataTypeError
        maxStreak = streak = 1
        for i, ch in enumerate(self.obj):
            if i > 0:
                if ch == self.obj[i - 1]:
                    streak += 1
                else:
                    if streak >= maxStreak:
                        maxStreak = streak
                    streak = 1
        return maxStreak

    def distance(self, obj1 = None, obj2 = None):
        '''Find the distance between obj1 and obj2.'''
        return len(self.between(obj1, obj2))

    def key(self, value):
        '''Find all the keys with the value.'''
        if self.type != dict:
            raise DataTypeError
        return tuple(k for k in self.obj if self.obj[k] == value)

    def last(self, occurrence):
        '''Find the last occurring index in an obj.'''
        return self.all(occurrence)[-1]

    def power_set(self):
        '''Find all the subs of obj except the empty sub and itself.
           This fuction returns a list because set is not ordered.'''
        length = len(self.obj)
        return [self.obj[j:j + i] for i in range(1, length) for j in range(length + 1 - i)]

    def count(self):
        '''Calls collections.Counter'''
        return dict(Counter(self.obj))

##flatten = lambda x:[y for l in x for y in flatten(l)] if isinstance(x, list) else [x]
def flatten(items, ignore_types = (str, bytes)):
    '''Flattens an iterable if not ignored.'''
    typ = type(items)
    def generator(items):
        for item in items:
            if isinstance(item, typ):
                yield from flatten(item)
            else:
                yield item
    return items if isinstance(items, ignore_types) else typ(generator(items))

def rmdup(obj):
    '''Return a list without duplicates.'''
    new = []
    for i in obj:
        if i not in new:
            new.append(i)
    return type(obj)(new)

def without(obj, *args):
    '''Return an obj without elements of args.'''
    typ = type(obj)
    generator = (i for i in obj if i not in args)
    if typ in [list, tuple]:
        return type(obj)(generator)
    if typ == str:
        for arg in args:
            obj = obj.replace(arg, '')
        return obj
    if typ == dict:
        return { k: obj[k] for k in obj if k not in args }
    if typ in [set, frozenset]:
        return obj.difference(args)
    raise DataTypeError

def replaceWith(obj, withObject, *args):
    argList = []
    for arg in args: argList += [arg, withObject]
    return sub(obj, *argList)

def substitute(obj, *args):
    '''obj supported data type: str, tuple, list, set.
       Usage: substitute([1, 2, 3, 4], 1, 2, 2, 3) // Returns [3, 3, 3, 4]
       Abbreviation: sub'''
    num = len(args)
    if num == 0:
        return
    if num % 2:
        raise Exception('Incorrect number of words')
    typ = type(obj)
    if typ == str:
        new = obj
        for i in range(0, num, 2):
            new = new.replace(str(args[i]), str(args[i + 1]))
    else:
        if typ in [tuple, list]:
            new = typ()
        else:
            raise DataTypeError
        for item in obj:
            for i in range(0, num, 2):
                if item == args[i]:
                    item = args[i + 1]
            if typ == set:
                new.add(item)
            else:
                new = new.__add__(typ([item]))
    return new

##abbreviation
sub = substitute

def formatted():
    '''请叫我套路生成器'''
    fmt = input('Please input your format sentence with variables replaced by {}.\n>>> ')
    while fmt.find('{}') == -1:
        fmt = input('Please type in at least 1 pair of {}!\n>>> ')
    else:
        fmtlst = fmt.split('{}')
        printlst = []
        while True:
            printstr = ''
            var = input('Please input your variables seperated with only 1 space or comma below. No input will stop this function.\n>>> ')
            varlst = advancedSplit(var)
            if not var:
                break
            if len(varlst) == 1:
                varlst *= fmt.count('{}')
            elif len(varlst) != fmt.count('{}'):
                print('Incorrect number of variables!')
                continue
            for i in range(len(varlst)):
                printstr += fmtlst[i]+varlst[i]
            if len(fmtlst) == len(varlst)+1:
                printstr += fmtlst[-1]
            printlst.append(printstr)
        seperation = input('Input Sentence Seperator. Default: \'\\n\'.\n>>> ') or '\n'
        print('\nResult:\n\n' + seperation.join(printlst) + '\n\n')

#abbreviation
fmt = formatted

def delta_days(date1, date2 = None):
    '''Return the days difference between two dates.
       Date must be in the format of YYYYMMDD.
       If date2 is None, then it will be regarded as today.'''
    year = lambda x: x // 10000
    month = lambda x:(x % 10000) // 100
    day = lambda x: x % 100
    start = datetime.datetime(year(date1), month(date1), day(date1))
    end = datetime.datetime(year(date2), month(date2), day(date2)) if date2 else datetime.datetime.today()
    delta = abs((end - start).days + 1)
    return delta
