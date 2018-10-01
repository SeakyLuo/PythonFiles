import math
import random
import datetime
import os
import time

desktop='C:\\Users\\Seaky\\Desktop\\'
DataTypeError=Exception('This data type is not supported!')

def rmlnk():
    for folder in os.listdir():
        if endwith(folder, '.lnk'):
            os.rename(folder, folder.replace(' - 快捷方式',''))

def chdt():
    '''Change current directory to Desktop.'''
    os.chdir(desktop)

def copyToClipboard(text):
    from win32 import win32clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()
## abbreviation
cpc=copyToClipboard

def checkfolders(folder1,folder2):
    '''Check whether folder1 is exactly the same as folder2'''
    l1=os.listdir(folder1)
    l2=os.listdir(folder2)
    if l1!=l2:
        return False
    for f in l1:
        p1=os.path.join(folder1,f)
        if os.path.isdir(p1):
            p2=os.path.join(folder2,f)
            if not checkfolders(p1,p2):
                return False
    return True

def findFilePath(filename,path=''):
    '''Default path: All
        Find the first occurence only.
        Use smaller range to have faster searching speed.'''
    if path=='':
        c=findPathFile(filename,'C:\\')
        if c:
            return c
        d=findPathFile(filename,'D:\\')
        if d:
            return d
        return False
    path=os.path.normcase(path)
    try:
        filelist=os.listdir(path)
    except PermissionError:
        return
    if filename in filelist:
        return path
    for f in filelist:
        p=os.path.join(path,f)
        if os.path.isdir(p):
            result=findFilePath(filename,p)
            if result:
                return result
    return False

def timer(func,iterations=1000,*args):
    '''If func has arguments, put them into args.'''
    t=time.time()
    for i in range(int(iterations)):
        func(*args)
    return time.time()-t

def fread(filename,evaluate=True,coding='utf8'):
    '''Read the file that has the filename.
        Set evaluate to true to evaluate the content.
        Default coding: utf8.'''
    file=open(filename,encoding=coding)
    content=file.read()
    if evaluate:
        try:
            content=eval(content)
        except:
            pass
    file.close()
    return content

def fwrite(filename,content,mode='w',coding='utf8'):
    ''' Write the file that has the filename with content.
        Default mode: "w"
        Default coding: utf8.'''
    file=open(filename,mode,encoding=coding)
    if type(content)!=str:
        content=repr(content)
    file.write(content)
    file.close()

def fcopy(src,dst,coding='utf8'):
    '''Copy a file.
        Requires source directory(src) and destination directory(dst).
        Default coding: utf8.'''
    filename=src[:find(src).last('\\')]
    fwrite(dst+['',filename][have(dst).end(filename)],fread(src,coding),coding=coding)

def advancedSplit(obj,*sep):
    '''Can have multiple seperators.'''
    if sep==() or len(sep)==1:
        return obj.split(*sep)
    word=''
    lst=[]
    for i,ch in enumerate(obj):
        word+=ch
        f=find(word).any(*sep)
        if f:
            word=without(word,*f)
            if word:
                lst.append(word)
                word=''
    if word:
        lst.append(word)
    return lst
##abbreviation
asplit=advancedSplit

def similar(obj1,obj2,capital=True):
    '''Check the similarity of two strings.
        Set capital to False to ignore capital.'''
    def grade(o1,o2):
        ## Let o1>=o2
        if o1==o2:
            return 1
        if o1=='' or o2=='':
            return 0
        len_o1=len(o1)
        len_o2=len(o2)
        score=len_o2/len_o1
        if score==1:
            result=sum((i==j)+(i!=j)*(i.lower()==j.lower())*0.9 for i,j in zip(o1,o2))/len_o1
            return eval(format(result,'.4f'))
        if len_o2<=15 and score>0.6:
            ps=list(reversed(find(o2).power_set()+[o2]))
            maxLen=0
            for i,sub in enumerate(ps):
                subLen=len(sub)
                if sub in o1 and maxLen<subLen:
                    maxLen=subLen
                try:
                    if i<2**len(o2)-2 and maxLen>len(ps[i+1]):
                        break
                except IndexError:
                    break
            else:
                return 0
            score=maxLen/len_o1
        if o2.lower() in o1.lower():
            if o2 in o1:
                if have(o1).start(o2):
                    score*=1.5
                else:
                    pass
            else:
                score*=0.9
        else:
            d1,d2=find(o1).count(),find(o2).count()
            sd=set(d2.keys()).difference(set(d1.keys()))
            if len(sd)==len(d2):  ##完全不一样
                return 0
            for key in d1:
                if key in d2:
##                    score*=(d2[key]/d1[key])**((d1[key]>=d2[key])*2-1)
                    if d1[key]>d2[key]:
                        score*=d2[key]/d1[key]
                    else:
                        score*=d1[key]/d2[key]
            score*=1-sum([d2.get(item) for item in sd ])/len_o2
##            不乘0.8的话similar('12345678','23')跟similar('12345678','24')都是0.25
            score*=0.8
        return eval(format(score,'.4f'))

    if type(obj1)!=str or type(obj2)!=str:
        raise DataTypeError
    if not capital:
        obj1=obj1.lower()
        obj2=obj2.lower()
    if len(obj1)>=len(obj2):
        return grade(obj1,obj2)
    else:
        return grade(obj2,obj1)

def predir():
    '''Go back to the previous folder.'''
    path=os.getcwd()
    os.chdir(path[:find(path).last('\\')])

class have:
    def __init__(self,obj):
        self.support=[str,list,dict,frozenset,set,tuple]
        self.obj=obj
        self.type=type(obj)
        self.empty=self.obj.__new__(self.type)
        self.empty.__init__()
        if self.type not in self.support:
             raise DataTypeError

    def which(self,*args):
        '''Check which elements of args are contained in the obj.'''
        contain=[ arg for arg in args if arg in self.obj ]
        if contain:
            if len(contain)==1:
                return contain[0]
            return contain
        return self.empty

    def all(self,*args):
        '''Check whether obj contains any element of the args.'''
        if args==():
            return True
        for arg in args:
            if arg not in self.obj:
                return False
        return True

    def any(self,*args):
        '''Check whether obj contains all the elements of args.'''
        if args==():
            return True
        for arg in args:
            if arg in self.obj:
                return True
        return False

    def sub(self,element):
        '''Check whether the element is in the subset of obj.'''
        if self.type==str:
            raise DataTypeError
        for sub in self.obj:
            if element in sub:
                return True
        return False

    def start(self,*args):
        '''Check whether the string starts with any occurrence in args.'''
        if self.type!=str:
            raise DataTypeError
        for arg in args:
            if len(self.obj)>=len(arg):
                 if self.obj[:len(arg)]==arg:
                     return True
            else:
                return False
        return False

    begin=start

    def end(self,*args):
        '''Check whether the string ends with any occurrence in args.'''
        if self.type!=str:
            raise DataTypeError
        for arg in args:
            if len(self.obj)>=len(arg):
                 if self.obj[-len(arg):]==arg:
                     return True
            else:
                return False
        return False

    def multiple(self,obj2):
        '''Check whether self.obj is the multiple of obj2'''
        if self.type not in [str,list,tuple]:
            raise DataTypeError
        if self.type!=type(obj2):
            raise Exception('Only data of the same type can be compared!')
        length1=len(l1)
        length2=len(l2)
        if length1%length2!=0:
            return False
        for i in range(0,length1,length2):
            if l1[i:i+length2]!=l2:
                return False
        return True

class find:
    def __init__(self,obj):
        self.support=[str,list,dict,tuple,set]
        self.type=type(obj)
        if self.type not in self.support:
            print('Unsupported data type automatically converts to str.')
            self.obj=repr(obj)
            self.type=str
        else:
            self.obj=obj
        self.empty=self.obj.__new__(self.type)
            
    def after(self,occurrence):
        '''Return the obj after the occurrence.'''
        if self.type==str:
            return self.obj[self.obj.index(occurrence)+len(occurrence):]
        elif self.type in [list,tuple]:
            return self.obj[self.obj.index(occurrence)+1:]
        raise DataTypeError

    def all(self,occurrence):
        '''Find all the occuring positions in an obj.'''
        if self.type==str:
            return [ idx for idx in range(len(self.obj)) if occurrence==self.obj[idx:idx+len(occurrence)]]
        if self.type in [list,tuple]:
            return [ idx for idx in range(len(self.obj)) if occurrence==self.obj[idx]]
        raise DataTypeError

    def any(self,*args):
        '''Find any element of args in obj.'''
        return [arg for arg in args if arg in self.obj]

    def second(self,occurrence):
        '''Find the second occuring positions in an obj.'''
        count=0
        if self.type==str:
            for idx in range(len(self.obj)):
                if occurrence==self.obj[idx:idx+len(occurrence)]:
                    count+=1
                    if count==2:
                        return idx
        elif self.type in [list,tuple]:
            for idx in range(len(self.obj)):
                if occurrence==self.obj[idx]:
                    count+=1
                    if count==2:
                        return idx
        raise DataTypeError

    def between(self,obj1=None,obj2=None):
        '''Return the obj between obj1 and obj2 (not included).
            First occurrence only.'''
        if self.type not in [str,list,tuple]:
            raise DataTypeError
        try:
            if obj1:
                index1=self.obj.index(obj1)
            else:
                index1=0
            if obj2:
                index2=self.obj[index1:].index(obj2)+index1
            else:
                index2=None
            return self.obj[index1+len(obj1):index2]
        except ValueError:
            return self.empty

    def count(self):
        '''Count the occurrences of each element and return a dict.
            Please use collections.Counter'''
        obj=self.obj
        if self.type==str:
            obj=list(obj)
        elif self.type not in [list,tuple]:
            raise DataTypeError
        d={}
        for item in obj:
            d[item]=d.get(item,0)+1
        return d

    def consecutive(self):
        '''Count the longest consecutive occurrences.'''
        if self.type==dict:
            raise DataTypeError
        maxStreak=streak=1
        for i,ch in enumerate(self.obj):
            if i>0:
                if ch==self.obj[i-1]:
                    streak+=1
                else:
                    if streak>=maxStreak:
                        maxStreak=streak
                    streak=1
        return maxStreak

    def distance(self,obj1=None,obj2=None):
        '''Find the distance between obj1 and obj2.'''
        return len(self.between(obj1,obj2))

    def key(self,value):
        '''Find all the keys that have the value.'''
        if self.type!=dict:
            raise DataTypeError
        return tuple(k for k in self.obj if self.obj[k]==value)

    def last(self,occurrence):
        '''Find the last occuring position in an obj.'''
        if occurrence not in self.obj:
            return -1
        index=self.obj.index(occurrence)
        if self.type==str:
            for idx in range(len(self.obj)-1,index,-1):
                if self.obj[idx:idx+len(occurrence)]==occurrence:
                    index=idx
                    break
        elif self.type in [list,tuple]:
            for idx in range(len(self.obj)-1,index,-1):
                if self.obj[idx:]==occurrence:
                    index=idx
                    break
        return index

    def power_set(self):
        '''Find all the subs of obj except the empty sub and itself.
           This fuction returns a list because set is not ordered.'''
        length=len(self.obj)
        return [self.obj[j:j+i] for i in range(1,length) for j in range(length+1-i)]

def startwith(string,occurrence):
    '''Check whether the string starts with occurrence.'''
    if len(string)>=len(occurrence):
        return string[:len(occurrence)]==occurrence
    return False

def endwith(string,occurrence):
    '''Check whether the string ends with occurrence.'''
    if len(string)>=len(occurrence):
        return string[-len(occurrence):]==occurrence
    return False

flatten = lambda x:[y for l in x for y in flatten(l)] if isinstance(x, list) else [x]

def rmdup(obj):
    '''Return a list without duplicates.'''
    new=[]
    for i in obj:
        if i not in new:
            new.append(i)
    typ=type(obj)
    if typ==list:
        return new
    elif typ==tuple:
        return tuple(new)

def without(obj,*args):
    '''Return an obj without elements of args.'''
    typ=type(obj)
    if typ==list:
        return [ i for i in obj if i not in args]
    if typ==tuple:
        return ( i for i in obj if i not in args)
    if typ==str:
        for arg in args:
            obj=obj.replace(arg,'')
        return obj
    if typ==dict:
        return { k:obj[k] for k in obj if k not in args}
    if typ in [set,frozenset]:
        return obj.difference(args)
    raise DataTypeError

def delta_days(day1,day2):
    '''Please enter an 8-digit number like 20170101'''
    year=lambda x:x//10000
    month=lambda x:(x%10000)//100
    day=lambda x:x%100
    start=datetime.datetime(year(day1),month(day1),day(day1))
    end=datetime.datetime(year(day2),month(day2),day(day2))
    delta=(end-start).days+1
    print(abs(delta))

def substitute(obj,*args):
    '''Support data type: str, tuple, list, set.
        Usage: substitute([1,2,3,4],1,2,2,3) // Returns [3,3,3,4]
        Abbreviation:sub'''
    num=len(args)
    if num==0:
        return
    if num%2:
        raise Exception('Please type in the correct number of subsitution words!')
    typ=type(obj)
    if typ==str:
        new=obj
        for i in range(0,num,2):
            subed=args[i]
            if type(subed)!=str:
                subed=str(subed)
            subs=args[i+1]
            if type(subs)!=str:
                subs=str(subs)
            new=new.replace(subed,subs)
    else:
        if typ==tuple:
            new=()
        elif typ==list:
            new=[]
        elif typ==set:
            new=set()
        else:
            raise DataTypeError
        for item in obj:
            for i in range(0,num,2):
                if item==args[i]:
                    item=args[i+1]
            if typ==tuple:
                new+=(item,)
            elif typ==list:
                new+=[item]
            elif typ==set:
                new.add(item)
    return new

##abbreviation
sub=substitute

def createList(sort=False,reverse=False,string=False): # create same elements
    print('By using this function you can create a list without typing punctuations.')
    lst=[]
    string=input('Please type STRING items seperated with space below like \'a b c\'. If you don\'t want strings please press the \'Enter\' button:\n>>> ')
    sl=string.split() # sl means string list
    for item in sl:
        lst.append(item)
    number=input('Please type NUMBERS seperated with space below like \'1 1.5 10\' or a range like \'1,10,2\'. If you don\'t want numbers please press the \'Enter\' button:\n>>> ')
    while True:
        sn=number.split()  # sn means split number list
        for item in sn:
            l=item.split(',')
            if len(l)>3:
                number=input('You typed in '+str(len(l)-3)+' more \',\' !Please type again!\n>>> ')
                lst=[]
                break
            elif len(l)==3: #quickly built a list that contains numbers from m to n
                if int(l[0])>int(l[1]):
                    for i in range(int(l[0]),int(l[1]),-abs(int(l[2]))):
                        lst.append(i)
                else:
                    for i in range(int(l[0]),int(l[1])+1,int(l[2])):
                        lst.append(i)
            elif len(l)==2:
                if int(l[0])>int(l[1]):
                    for i in range(int(l[0]),int(l[1]),-1):
                        lst.append(i)
                else:
                    for i in range(int(l[0]),int(l[1])+1):
                        lst.append(i)
            elif not item.isnumeric() and item.find('-')==0:
                lst.append(eval(item))
            elif not item.isnumeric() and item.find(',')==-1:
                print('The input should be NUMBERS!\n')
                createList()
                return
            else:
                lst.append(eval(item))
        break
    listOrTupleOrSetOrDict=input('Please type your list, tuple, set or dict here. If you want no input just press the \'Enter\' button:\n>>> ')
    if listOrTupleOrSetOrDict!='':
        while type(eval(listOrTupleOrSet)) not in [list,tuple,set,dict]:
            listOrTupleOrSetOrDict=input('Your input in not a list, tuple, set or dict! Please type again!\n>>> ')
        lst.append(listOrTupleOrSetOrDict)
    if sort:
        lst.sort()
    if reverse:
        lst.reverse()
    if string:
        s=''
        for item in lst:
            s+=str(item)+' '
        print('\''+s[:-1]+'\'')
    else:
        print(lst)

##abbreviation
cl=createList

def formatted():
    '''请叫我套路生成器'''
    fmt=input('Please input your format sentence with variables replaced by {}.\n>>> ')
    while fmt.find('{}')==-1:
        fmt=input('Please type in at least 1 pair of {}!\n>>> ')
    else:
        fmtlst=fmt.split('{}')
        printlst=[]
        while True:
            printstr=''
            var=input('Please input your variables seperated with only 1 space or comma below. No input will stop this function.\n>>> ')
            varlst=advancedSplit(var)
            if var=='':
                break
            if len(varlst)==1:
                varlst*=fmt.count('{}')
            elif len(varlst)!=fmt.count('{}'):
                print('Please type in the correct number of variables!')
                continue
            for i in range(len(varlst)):
                printstr+=fmtlst[i]+varlst[i]
            if len(fmtlst)==len(varlst)+1:
                printstr+=fmtlst[-1]
            printlst.append(printstr)
        seperation=input('How do you want to seperate them? Input your words below to seperate them. No input will be regarded as new line.\n>>> ')
        print('\nThe format sentence you want is:\n\n')
        for item in printlst:
            if seperation!='' and item!=printlst[-1]:
                print(item,end=seperation)
            else:
                print(item)

#abbreviation
fmt=formatted
