import math
import random
import ez
from decimal import Decimal
from functools import reduce

def product(*numbers):
    return reduce(lambda x,y:x*y,numbers)

def accurateCalculation(formula='',sn=False):
    '''Function calls not supported.
        Set sn to True to use scientific notation.
        Abbreviation: ac'''
    def get_result():
        ni='' ## new i
        try:
            nf=formula.replace('^','**').lower() ## new formula
        except AttributeError:
            raise Exception('Input formula should be a string.')
        num=''
        try:
            for i,ch in enumerate(nf):
                if ch.isnumeric() or \
                   (ch=='-' and (i==0 or nf[i-1]=='e')) or \
                   (ch=='+' and (i==0 or nf[i-1]=='e')) or \
                   (ch=='e' and (nf[i+1].isnumeric() or nf[i+1] in ['+','-'])) or \
                   (ch=='.' and nf[i+1].isnumeric()):
                    num+=ch
                elif ch==' ':
                    pass
                else:
                    if num:
                        ni+='Decimal("{}")'.format(num)
                        num=''
                    ni+=ch
            if num:
                ni+='Decimal("{}")'.format(num)
        except:
            raise Exception('Invalid expression: '+num)
        result=eval(repr(eval(ni))[9:-2])
        return result

    if formula:
        result=get_result()
        if sn:
            result=scin(result,0)
        return result
    while True:
        formula=input('Input the formula below. Empty input will exit.\n>>> ')
        if formula=='':
            return
        if ez.startwith(formula,'sn='):
            sn=eval(formula[3:])
            continue
        result=get_result()
        if sn:
            result=scin(result,0)
        print(result)

##abbreviation
ac=accurateCalculation

def intToList(integer):
    return [ integer//10**i%10 for i in range(len(str(integer))) ]

def scientificNotation(num,pr=True):
    '''Abbreviation: scin'''
    result='%e'%num
    if pr:
        print(result)
    else:
        return result

##abbreviation
scin=scientificNotation

def nmb(n,m): ## nmb does not mean nimabi
## This function gives an algorithm which returns all the method
## that you can put n identical balls into m identical boxes
    def recursive(n,m,lst,method=''):
        if m>1:
            startIdx=0
            if method!='':
                startIdx=int(method[-2])
            for i in range(startIdx,n//m+1):
                recursive(n-i,m-1,lst,method+str(i)+'-')
            method=''
        elif m==1:
            lst.append(method+str(n))

    methodlst=[]
    recursive(n,m,methodlst)
    print(methodlst,len(methodlst),sep='\n')

def congruenceEquation(a,b,m):
    ''' Find the least positive integer x that satisfies ax≡b(mod m).
        Abbreviation: cE.'''
    if b<0:
        b%=m
    for i in range(m):
        if (a*i)%m==b:
            return i

##abbreviation
cE=congruenceEquation

def chineseRemainderTheorem():
    '''Find solutions to the system of congruences by typing the a,b,m of ax≡b(mod m).
        If a is 1, only b and m are needed.
        Abbrevation: crt.'''
    number=()
    divisor_dict={}
    print('Type the a,b,m of ax≡b(mod m). If a is 1, only b and m are needed.')
    while True:
        s=input('Please seperate a,b,m or b,m by space. Order matters. Press Enter to stop.\n>>> ')
        if s and s.find(' ')==-1:
            print('No space detected! Please type again! Correct form: >>> 7 3 15')
            continue
        elif s=='':
            break
        dr=s.split()
        ## x≡dr[0](mod dr[1]) or
        ## dr[0]*x≡dr[1](mod dr[2])
        try:
            dr[0]=int(dr[0])
            dr[1]=int(dr[1])
            if len(dr)==3:
                dr[2]=int(dr[2])
                dr[0]=congruenceEquation(dr[0],dr[1],dr[2])
                dr[1],dr[2]=dr[2],dr[1]
        except:
            print('Invalid input! Please try again!')
            continue
        if dr[1]<=0:
            print('Positive divisor only! Please try again!')
            continue
        elif dr[1] in divisor_dict and divisor_dict[dr[0]]!=dr[1]:
            print('Inconsistent remainder! Please try again!')
            continue
        elif dr[0]<0 or dr[0]>dr[1]:
            print('Remainder automatically adjusted.')
            dr[0]=dr[0]%dr[1]
        divisor_dict[dr[1]]=[dr[0]]
        if number==():
            number=(dr[1],dr[0])
        else:
            divisor,remainder=number
            dr[0]=(dr[0]-remainder)%dr[1]
            for i in range(dr[1]):
                if (divisor*i)%dr[1]==dr[0]:
                    number=(lcm(divisor,dr[1]),remainder+i*divisor)
                    break
            else:
                yn=input('Such number doesn\'t exist! Did you just make a typo?\nInput "y" for yes to delete the previous input, "r" to restart. Other input will be regarded as no.\n>>> ').lower()
                if yn=='y':
                    del divisor_dict[dr[1]]
                    continue
                elif yn=='r':
                    divisor_dict={}
                    continue
                else:
                    ## do something?
                    return

    if number==():
        return
    n0,n1=number
    formula='x'
    if n0!=1:
        formula=str(n0)+'x'
    natural_num='positive integer'
    if n1 and n0!=n1:
        formula+='+'+str(n1)
        n0=n1
        natural_num='natural number'
    print('The least satisfying postive integer is {}.'.format(n0))
    print('All the satifying numbers are in the form: {}, where x is any {}.'.format(formula,natural_num))

##abbreviation
crt=chineseRemainderTheorem

def pH(concentration):
    '''Support pH, pOH and any pK values'''
    return -math.log(concentration,10)

def titration(volume,molarity1,molarity2,pk,product_basic=0):
    '''Support weak acid or weak base only'''
    n1=volume*molarity1
    mol=n1/(volume+n1/molarity2)
    h=(mol*10**(pk-14))**0.5
    if product_basic:
        h=10**(-14)/h
    return pH(h)

def burn_equation(formula):
    '''Please enter a formula like C8H16O2'''
    d={}
    length=len(formula)
    parentheses=False
    d_={}

    def judge(i,ch,dictionary):
        if ch.isalpha():
            if i+1==length:
                dictionary[ch]=dictionary.get(ch,0)+1
            elif formula[i+1].isnumeric():
                num=''
                while i+1<length and formula[i+1].isnumeric():
                    num+=formula[i+1]
                    i+=1
                dictionary[ch]=dictionary.get(ch,0)+eval(num)
            else:
                dictionary[ch]=dictionary.get(ch,0)+1

    for i,ch in enumerate(formula):
        if ch=='(':
            parentheses=True
        elif ch==')':
            if i+1<length and formula[i+1].isnumeric():
                multiple=eval(formula[i+1])
            for element in d_:
                d[element]=d.get(element,0)+d_[element]*multiple
            parentheses=False
        if parentheses:
            judge(i,ch,d_)
        else:
            judge(i,ch,d)

    new_d={}
    new_d[formula]=1
    new_d['CO2']=max([d.get('C',0),d.get('c',0)])
    new_d['H2O']=max([d.get('H',0),d.get('h',0)])//2
    new_d['O']=2*new_d['CO2']+new_d['H2O']-max([d.get('O',0),d.get('o',0)])
    multiple=[1,2][new_d['O']%2]
    for compound in new_d:
        new_d[compound]*=multiple
    new_d['O2']=new_d['O']//[2,1][new_d['O']%2]

    for compound in new_d:
        if new_d[compound]==1:
            new_d[compound]='+'+compound
        elif new_d[compound]==0:
            new_d[compound]=''
        else:
            new_d[compound]='+{}{}'.format(new_d[compound],compound)
    reactant='{}{}→'.format(new_d[formula],new_d['O2'])[1:]
    product='{}{}'.format(new_d['CO2'],new_d['H2O'])[1:]
    print(reactant+product)

def truth_table(formula,output='a'):
    '''Please enter the formula in terms of a string.
       Use "=>" or "->" for "imply", "+" for "exclusive or".
       Please use () for precendence in case of miscalculations.
       Default output table will be of Ts and Fs.
       Change the value of output to "full" to output a complete table,
       to "num" to output a table of 1s and 0s.'''
    TF=[True, False]
    connective=['and','or','not']

    new_formula=''
    var_lst=[]  ## for p,q,r
    compound_dict={} ## for (p and q):"method['p'] and method['q']"
    col_lst=[]  ## for display
    parentheses_stack=[]  ## put parentheses' indice
    corresponding_stack=[] ## put parentheses' indice of new_formula
    variable=''
    compound=''
    is_compound=False

    formula.strip()
    if formula[-1].isalpha():
        formula+=' '
    for i,ch in enumerate(formula):
        if ch.isalpha():
            variable+=ch
        else:
            if ch=='(':
                parentheses_stack.append(i)
                corresponding_stack.append(len(new_formula)+1)
            elif ch==')':
                try:
                    start_pos=parentheses_stack.pop()+1
                except:
                    print('The numbers of left and right parentheses do not match!')
                    return
                compound=formula[start_pos:i].strip()
                if compound not in compound_dict:
                    is_compound=True
            elif (ch=='=' or ch=='-') and formula[i+1]=='>':
                previous_variable=''
                if len(corresponding_stack)==0:
                    if new_formula.find('(')==-1:
                        new_formula='not {} or'.format(new_formula)
                    else:
                        idx=-1
                        while True:
                            previous_variable=new_formula[idx]+previous_variable
                            if new_formula[idx]=='(':
                                break
                            idx-=1
                        new_formula=new_formula[:idx]+'not {} or'.format(previous_variable.strip())
                else:
                    idx=-1
                    while True:
                        previous_variable=new_formula[idx]+previous_variable
                        idx-=1
                        if idx+1==corresponding_stack[-1]-len(new_formula):
                            break
                    new_formula=new_formula[:idx+1]+'not {} or'.format(previous_variable.strip())
                continue
            elif ch=='>':
                continue
            elif ch=='+': ##(p and not q) or (not p and q)
                continue
            if variable:
                if variable not in connective:
                    if variable not in var_lst:
                        var_lst.append(variable)
                    new_formula+='method[\'{}\']'.format(variable)
                else:
                    new_formula+=variable
                variable=''
            if is_compound:
                compound_dict[compound]=new_formula[corresponding_stack.pop():]
                is_compound=False
            new_formula+=ch

    var_num=len(var_lst)
    col_lst=var_lst+list(compound_dict.keys())+[formula]
    var_len={}
    first_line=''
    for col in col_lst:
        length=[6,len(col)+1][len(col)>5]
        var_len[col]=length
        first_line+=('{:'+str(length)+'}').format(col)
    print(first_line)

    printout=''
    file_content=','.join(col_lst)+'\n'
    table=[]

    ##assign values
    def recursive(method={}):
        length=len(method)
        if length<var_num:
            for tf in TF:
                method[var_lst[length]]=tf
                if length==var_num-1:   ## after appending if length==var_num
                    table.append(repr(method))
                recursive()
                del method[var_lst[length]]

    recursive()

    for method in table:
        method=eval(method)
        row=[]
        for col in col_lst:
            if col in compound_dict:
                row.append((eval(compound_dict[col]),var_len[col]))
            elif col==formula:
                row.append((eval(new_formula),var_len[col]))
            else:
                row.append((eval('method[\'{}\']'.format(col)),var_len[col]))
        for tf,length in row:
            printout+=('{:'+str(length)+'}').format(repr(tf))
            file_content+='{},'.format(tf)
        printout+='\n'
        file_content=file_content[:-1]+'\n'
    printout=printout[:-1]
    file_content=file_content[:-1]
    print(printout)

    try:
        infile=open('C:\\Users\\Seaky\\Desktop\\truth table.csv','w')
    except:
        print('傻逼关进程啊！')
        return
    if output=='num':
        file_content=sub(file_content,'True','1','False','0')
    elif output!='full':
##        file_content=sub(file_content,'and','∧','or','∨','not','￢')
        file_content=sub(file_content,'True','T','False','F')
    infile.write(file_content)
    infile.close()

integer=lambda x:[x,int(x)][x==int(x)]

def get24(a,b=-1,c=-1,d=-1):
    if 1000<=a<10000 and b==c==d==-1:
        a,b,c,d=map(int,str(a))
    elif not 0<a<10 or not 0<b<10 or not 0<c<10 or not 0<d<10:
        print('Numbers should be greater than 0 and less than 10.')
        return
    operators=['+','-','*','/']
    jiajian=['+','-']
    chengchu=['*','/']
    for p in permutations(str(a),str(b),str(c),str(d)):
        for o1 in operators:
            for o2 in operators:
                for o3 in operators:
                    calculations=['{}{}{}{}{}{}{}'.format(p[0],o1,p[1],o2,p[2],o3,p[3]),\
                                  '({}{}{}){}{}{}{}'.format(p[0],o1,p[1],o2,p[2],o3,p[3]),\
                                  '{}{}{}{}({}{}{})'.format(p[0],o1,p[1],o2,p[2],o3,p[3]),\
                                  '({}{}{}{}{}){}{}'.format(p[0],o1,p[1],o2,p[2],o3,p[3]),\
                                  '({}{}{}){}({}{}{})'.format(p[0],o1,p[1],o2,p[2],o3,p[3]),\
                                   '(({}{}{}){}{}){}{}'.format(p[0],o1,p[1],o2,p[2],o3,p[3])]
                    for c in calculations:
                        try:
                            if eval(c)==24:
                                print(c)
                                break
                        except ZeroDivisionError:
                            pass

def permutation(n,m):
    '''factorial(n)/factorial(n-m)
        n!/(n-m)!'''
    return factorial(n)//factorial(n-m)

##abbreviation
a=permutation

def permutations(*args):
    '''Please use builtin func: itertools.permuations'''
    methods=[]
    length=len(args)
    def recursive(p=()):
        if len(p)==length and p not in methods:
            methods.append(p)
            return
        lst=list(args)
        for i in p:
            lst.remove(i)
        for arg in lst:
            recursive(p+(arg,))

    recursive()
    return methods

def combination(n,m):
    ''' n choose m
        factorial(n)/(factorial(m)*factorial(n-m))
        n!/(m!*(n-m)!)'''
    if m>n:
        return 0
    if m>n//2:
        return combination(n,n-m)
    num=1
    for i in range(n-m+1,n+1):
        num*=i
    num//=factorial(m)
    return num

##abbreviation
c=combination

def npickm(n,m):
    '''n cannot have duplicates.
        Please use builtin func: itertools.combinations, itertools.combinations_with_replacement'''
    methods=[]
    def recursive(method=set()):
        for item in n:
            if item not in method:
                recursive(method.union({item}))
            if len(method)==m:
                if method not in methods:
                    methods.append(method)
                return

    recursive()
    return methods

def fraction(n,m):
    '''Reduce n/m'''
    output='{}/{}'.format(n,m)
    negative=''
    if n*m<0:
        negative='-'
        n=abs(n)
        m=abs(m)
    if type(n)==float or type(m)==float:
        while int(n)!=n or int(m)!=m:
            n*=10
            m*=10
        n=int(n)
        m=int(m)
    new_n=n
    new_m=m
    if n%m==0:
        new_n=n//m
        new_m=1
        output+='={}{}/1'.format(negative,new_n)
    elif m%n==0:
        new_n=1
        new_m=m//n
        output+='={}1/{}'.format(negative,new_m)
    else:
        for i in range(2,int(min(n,m)**0.5)+1):
            while new_n%i==0 and new_m%i==0:
                new_n//=i
                new_m//=i
        if new_n!=n:
            output+='={}{}/{}'.format(negative,new_n,new_m)
    quotient=ac(repr(n/m))
    if quotient==int(quotient):
        quotient=int(quotient)
        output+='='
    elif set(findPrimeFactors(new_m,False)).issubset({2,5}):
        output+='='
    else:
        output+='≈'
    output+=negative+repr(quotient)
    print(output)

##abbreviation
frac=fraction

def factorial(n):
    '''Return n!'''
    product=1
    for i in range(1,n+1):
        product*=i
    return product

##abbreviation
fact=factorial

def factorialSkip(n):
    if n in [0,1] :
        return 1
    return n*factorialSkip(n-2)

def isPrime(n):
    if type(n)==int and n>=2:
        for i in range(2,int(n**0.5)+1):
            if n%i==0:
                return False
        return True
    return False

def findPrimeFactors(num,ifPrint=True,return_dict=False):
    '''Automatically Regarded as a non-negative number'''
    num=abs(num)
    if isPrime(num) or num in [0,1]:
        return [num]
    i=num
    d={}
    for k in range(2,num//2+1):
        while i%k==0:
            d[k]=d.get(k,0)+1
            i/=k
    s=''
    if d!={}:
        for key in d:
            if d[key]==1:
                s+=str(key)+'*'
            else:
                s+='('+str(key)+'^'+str(d[key])+')*'
    if ifPrint:
        print(str(num)+'='+s[:-1])
    if return_dict:
        return d
    else:
        return list(d.keys())

##abbreviation
fpf=findPrimeFactors

def findAllFactors(num):
    return [ i for i in range(1,int(num**0.5)+1) if num%i==0 ]

def findCofactors(num1,num2):
    '''Automatically Regarded as non-negative numbers.'''
    if num1==0:
        return findAllFactors(num2)
    elif num2==0:
        return findAllFactors(num1)
    return [ i for i in range(1,min([abs(num1),abs(num2)])//2+1) if num1%i==num2%i==0]

##abbreviation
fc=findCofactors

def gcd(n1,n2):
    '''Greatest common divisor'''
    if abs(n1-n2)==1:
        return 1
    return findCofactors(n1,n2)[-1]

def lcm(n1,n2):
    '''Least common multiple'''
    if any([n1,n2])==0:
        return 0
    if n1%n2==0:
        return n1
    elif n2%n1==0:
        return n2
    elif gcd(n1,n2)==1:
        return n1*n2
    n1_dict=findPrimeFactors(n1,ifPrint=0,return_dict=1)
    n2_dict=findPrimeFactors(n2,ifPrint=0,return_dict=1)
    for factor in n2_dict:
        n1_dict[factor]=max(n2_dict[factor],n1_dict.get(factor,0))
    num=1
    for factor in n1_dict:
        num*=factor**n1_dict[factor]
    return num

formLst=['w','l','s','b']

def matrixProducer(row=0,column=0,formula="",matrixOrDeterminant='m'):
    ## latex form
    if row==0 or column==0 or formula=="":
        inputRC=""
        while True:
            if matrixOrDeterminant=='m':
                inputRC=input('Input the rows and columns here and seperate them with space or comma.\n>>> ')
            elif matrixOrDeterminant=='d':
                inputRC=input('Input the size of the determinant and seperate them with space or comma.\n>>> ')
            RC=advancedSplit(inputRC)
            if len(RC)==0:
                return
            elif len(RC)==1:
                inputRC=' '.join(2*RC)
            elif len(RC)>2:
                inputRC=input('Your input must be 2 numbers! Please type again!\n>>> ')
                continue
            for item in RC:
                if not item.isnumeric():
                    inputRC=input('Your input must be numbers! Please type again!\n>>> ')
                    continue
            break
        row=int(RC[0])
        column=int(RC[1])
        inputEnt=input('Input the entries of matrix row by row seperated with space or comma.\nPlease type here: ')
        Ent=advancedSplit(inputEnt)
    else:
        Ent=advancedSplit(formula)
    difference=len(Ent)-row*column
    if difference!=0:
        if difference==1:
            print('\nYou typed in 1 more entry! We will get restarted!\n')
        elif difference>1:
            print('\nYou typed in {} more entries! We will get restarted!\n'.format(difference))
        elif difference==-1:
            print('\nYou need to type in 1 more entry! We will get restarted!\n')
        elif difference<-1:
            print('\nYou need to type in {} more entries! We will get restarted!\n'.format(-difference))
        matrixProducer()
        return
    else:
        output=''
        for i in range(row):
            for j in range(column):
##                entry=Ent[i*column+j]
##                if -1<entry.find('f')<entry.find('(')<entry.find(',')<entry.find(')'):
##                    output+=['','-'][entry[0]=='-']+fl(entry[entry.find('(')+1:entry.find(',')],entry[entry.find(',')+1:entry.find(')')])[2:-2]
##                else:
##                    output+=Ent[i*column+j]
##                output+='&'
                output+=Ent[i*column+j]+'&'
            output=output[:-1]+'\\\\'
        if matrixOrDeterminant=='m':
            output='$$\\begin{bmatrix}'+output[:-2]+'\\end{bmatrix}$$'
        elif matrixOrDeterminant=='d':
            output='$$\\begin{vmatrix}'+output[:-2]+'\\end{vmatrix}$$'
        return output

def matrixLaTeX(row=0,column=0,matrix="",printOrReturn='p'):
    output=matrixProducer(row,column,matrix)
    if printOrReturn=='p':
        print('By using this function you will get a matrix in LaTeX form.')
        print('The matrix you want in LaTeX is:\n\n'+output+'\n')
    else:
        return output

##abbreviation
ml=matrixLaTeX

def matrixWolframAlpha(row=0,column=0,matrix='',leftBracket='[',rightBracket=']',printOrReturn='p'):   ##no brackets
##        inputBracket=input('By using this function you will get a matrix in WolframAlpha form.\nFirst of all, which bracket do you want to use, \'(\', \'[\'(default) or\'{\'?\n>>> ')
##        if inputBracket!='(' and ')' and '[' and ']' and '{' and '}' and '':
##            print('Please type in the correct bracket!\n')
##            matrixWolframAlpha()
##        leftBracket='['
##        rightBracket=']'
##        if inputBracket=='(' or inputBracket==')':
##            leftBracket='('
##            rightBracket=')'
##        elif inputBracket=='{' or inputBracket=='}':
##            leftBracket='{'
##            rightBracket='}'
    output=matrixProducer(row,column,matrix)
    output=matrixConvert(form='w',matrix=output)
    if printOrReturn=='p':
        print('By using this function you will get a matrix in WolframAlpha form.')
        print('The matrix you want in WolframAlpha Form is:\n\n'+output+'\n')
    else:
        return output

##abbreviation
mw=matrixWolframAlpha

def mf(r=0,c=0,rg=None,f='',var='',pr='p'):
    if r==0 or c==0:
        inputRC=input('This function provides a shortcut for users to create an m*n matrix.\nPlease type m and n seperated with space or comma\n>>> ')
        RC=advancedSplit(inputRC)
        if len(RC)==0:
            return
        elif len(RC)==1:
            RC*=2
        elif len(RC)>2:
            print('\nPlease type in 2 numbers!\n')
            mf()
            return
        for item in RC:
            if not item.isnumeric():
                print('\nPlease type in numbers!\n')
                return
        r=int(RC[0]) #r means rows
        c=int(RC[1]) #c means columns
    else:
        if type(r)!=int:
            print ('The number of rows must be an integer!\n')
            mf()
            return
        if type(c)!=int:
            print ('The number of columns must be an integer!\n')
            mf()
            return
    if rg and type(rg) not in [tuple,list]:
        print ('Please type in a tuple or a list as range!\n')
        mf()
        return
    if rg and var:
        print ('You can only choose either a matrix with range or a variable matrix!\n')
        mf()
        return
    inputForm=f
    if f==None:
        inputForm=input('Please type in the form that you want. \'l\' represents LaTeX form, \'w\' represents WolframAlpha form(default), \'b\' represents beautified matrix form and \'s\' represents string form.\n>>> ')
    while True:
        if inputForm=='':
            inputForm='l'
        elif inputForm not in formLst:
            inputForm=input('Your form is not supported! Please type again!\n>>> ')
            continue
        break
    output=''
    var=''
    if r*c<=26 and rg==None and input('Do you want to make the matrix a multi-variables matrix?Type \'y\' representing \'yes\'. Other input will be regarded as \'no\'.\n>>> ').lower() in ['y','yes']:
        output=matrixProducer(r,c,','.join( chr(97+i) for i in range(r*c)))
        output=matrixConvert(form=inputForm,matrix=output)
    else:
        var=input('Do you want to make it a one-variable matrix? Type in the variable or press "Enter" to skip.\n>>> ')
        if var=='':
            newLst=[]
            if rg==None:
                newLst=[]
                inputRange=input('Please type in a range like 0(will produce a matrix that only contains 0) or 1 10 or 10,2,-2:\n>>> ')
                while True:
                    lst=advancedSplit(inputRange)
                    for item in lst:
                        if type(eval(item))!=int:
                            inputRange=input('Your input must be integers! Please type again!\n>>> ')
                            continue
                    newLst=lst
                    break
            else:
                newLst=rg
            startNum=0
            endNum=0
            step=1
            numlst=[]
            if len(newLst)==1:
                numlst=newLst*r*c
            elif len(newLst)==2:
                startNum=newLst[0]
                endNum=newLst[1]
                if startNum>endNum:
                    step=-1
                numlst=[repr(i) for i in range(startNum,endNum+1,step)]
            elif len(newLst)==3:
                startNum=newLst[0]
                endNum=newLst[1]
                if startNum>endNum:
                    step=-abs(newLst[2])
                else:
                    step=newLst[2]
                numlst=[repr(i) for i in range(startNum,endNum+1,step)]
            else:
                print('The numbers you want do not match the number of entries in the matrix!.Please type in the correct number of numbers!\n')
                mf()
                return
            if len(numlst)!=r*c:
                print('Please type in the correct numbers!\n')
                mf()
                return
            output=matrixProducer(row,column,','.join(numlst))
        else:
            output=matrixProducer(row,column,','.join(var+'_'+str(i)+str(j) for i in range(1,r+1) for j in range(1,c+1)))
    output=matrixConvert(form=inputForm,matrix=output)
    if pr=="p":
        print('\nThe matrix you want is:\n\n'+output+'\n')
    else:
        return output

def formJudge(m):
    if type(m)!=str:
        return False
    if m.find('$$\\begin{bmatrix}')==0 and len(m)-m.find('\end{bmatrix}$$')==15 and (m.find('&') and m.find('\\'))!=-1:
        return 'l'
    elif m.find('$$\\begin{vmatrix}')==0 and len(m)-m.find('\end{vmatrix}$$')==15 and (m.find('&') and m.find('\\'))!=-1:
        return 'dl'
    elif m.find(' ')>0:
        for i in m.split():
            if not i.isalnum():
                return False
        return 's'
    elif type(eval(m))==list:
        for item in eval(m):
            if type(item)!=list:
                return False
        return 'w'
    elif m.find(' ')==-1:
        if m.isalnum():
            return 's'
        return False
    elif m.count('|')%2==0 and m.count('\n')==m.count('|')/2-1:
        return 'b'
    else:
        return False

def matrixConvert(form='',matrix=''):
    if matrix=='':
        inputMat=input('By using this function, you can change your matrix form.\nPlease type your matrix here:').strip()
    else:
        inputMat=matrix
    if formJudge(inputMat)==False:
        print('Your matrix is not supported! Please type again!\n')
        matrixConvert()
    while True:
        if form:
            inputForm=form
        else:
            inputForm=input('Please type in the form that you want. \'l\' represents LaTeX form,\'w\' represents WolframAlpha form, \'b\' represents beautified matrix form and \'s\' represents string matrix form.\n>>> ').lower()
        if inputForm.lower() not in formLst:
            inputForm=input('Your matrix form is not supported! Please type again!\n>>> ')
        else:
            break
    if formJudge(inputMat)==form:
        return inputMat
    newMat=''
    if formJudge(inputMat)=='w':
        if inputForm=='l':
            inputMat=ez.substitute(inputMat,'[[','$$\\begin{bmatrix}',']]','\\end{bmatrix}$$','],[','\\\\')
            for ch in inputMat:
                if ch==',':
                    ch='&'
                newMat+=ch
        elif inputForm=='w':
            newMat+=matrix
        elif inputForm=='b':
            inputMat=ez.substitute(inputMat,'[[','|',']]','|','],[','|\n|',',',' ')
            newMat=formatBMat(inputMat)
        else:
            inputMat=ez.substitute(inputMat,'[[','',']]','','],[',' ')
            for ch in inputMat:
                if ch==',':
                    ch=' '
                newMat+=ch
    elif formJudge(inputMat)=='l' or 'dl':
        if formJudge(inputMat)=='dl':
            inputMat=inputMat.replace('vmatrix','bmatrix')
        if inputForm=='w':
            inputMat=inputMat.replace('$$\\begin{bmatrix}','[[')
            inputMat=inputMat.replace('\\end{bmatrix}$$',']]')
            for i,ch in enumerate(inputMat):
                if ch=='&':
                    ch=','
                elif ch=='\\' and inputMat[i+1]=='\\':
                    ch='],['
                elif ch=='\\' and inputMat[i-1]=='\\':
                    ch=''
                newMat+=ch
        elif inputForm=='l':
            newMat+=matrix
        elif inputForm=='b':
            inputMat=ez.substitute(inputMat,'$$\\begin{bmatrix}','|','\\end{bmatrix}$$','|','\\\\','|\n|','&',' ')
            newMat=formatBMat(inputMat)
        else:
            inputMat=inputMat[18:-15]
            for ch in inputMat:
                if not ch.isalnum():
                    ch=' '
                newMat+=ch
            newMat=newMat.replace('  ',' ')
    elif formJudge(inputMat)=='b':
        if inputForm=='w':
            inputMat=inputMat[1:]+'[['
            inputMat=inputMat[:-1]+']]'
            for i,ch in enumerate(inputMat):
                if ch=='|' and inputMat[i+1]=='\n':
                    ch=']'
                elif ch=='\n':
                    ch=','
                elif ch=='|' and inputMat[i-1]=='\n':
                    ch='['
                elif ch==' ':
                    ch=','
                newMat+=ch
        elif inputForm=='b':
            newMat+=matrix
        if inputForm=='l':
            inputMat=inputMat[1:]+'$$\\begin{bmatrix}'
            inputMat=inputMat[:-1]+'\\end{bmatrix}$$'
            for ch in inputMat:
                if ch==' ':
                    ch='&'
                elif ch=='|':
                    ch='\\'
                elif ch=='\n':
                    ch=''
                newMat+=ch
        else:
            inputMat=inputMat[1:-1]
            for ch in inputMat:
                if not ch.isalnum():
                    ch=' '
                newMat+=ch
            newMat=newMat.replace('  ',' ')
    if form=='' or matrix=='Noe':
        print('\n'+newMat)
    else:
        return newMat

##abbreviation
mc=matrixConvert

def matrixRandom(row=0,column=0,randRange=None,form='',printOrReturn='y'):
    if randRange and type(rg) not in [tuple,list]:
        print ('Please type in a tuple or a list as range!\n')
        matrixRandom()
        return
    elif randRange==None:
        newLst=[]
        inputRange=input('Please type in the range of matrix entries like 1 9 or 10,2,-2\n>>> ')
        while True:
            lst=advancedSplit(inputRange)
            for item in lst:
                if type(eval(item))!=int:
                    inputRange=input('Your input must be integers! Please type again!\n>>> ')
                    continue
            newLst=lst
            break
        startNum=0
        endNum=0
        step=1
        numlst=[]
        if len(newLst)==2:
            startNum=newLst[0]
            endNum=newLst[1]
            if startNum>endNum:
                startNum,endNum=endNum,startNum
        elif len(newLst)==3:
            if startNum>endNum:
                startNum,endNum=endNum,startNum
            startNum=newLst[0]
            endNum=newLst[1]
            step=abs(newLst[2])
        else:
            print("Please type in 2 or 3 numbers!")
            matrixRandom()
            return
        numlst=[repr(random.randrange(startNum,endNum+1,step)) for i in range(row*column)]
    inputForm=form
    if form=='':
        inputForm=input('Please type in the form that you want. \'l\' represents LaTeX form, \'w\' represents WolframAlpha form(default), \'b\' represents beautified matrix form and \'s\' represents string form.\n>>> ')
    while True:
        if inputForm=='':
            inputForm='l'
        elif inputForm not in formLst:
            inputForm=input('Your form is not supported! Please type again!\n>>> ')
            continue
        break
    output=matrixProducer(row,column,','.join(numlst))
    output=matrixConvert(form=inputForm,matrix=output)
    if printOrReturn=='p':
        print('By using this function you will get a random matrix in LaTeX form.')
        print('The randam matrix you want is:\n\n'+output+'\n')
    else:
        return output

##abbreviation
mr=matrixRandom

def formatBMat(matrix):
    rowmatrix=matrix.replace('|',' ')
    itemlist=rowmatrix.split
    L=[]
    longest=len(itemlist[0])
    newMat=''
    for item in itemlist:
        if len(item)>longest:
            longest=len(item)
    for item in itemlist:
        L.append(('{:'+str(longest)+'}').format(item))
    r=matrix.count('\n')+1
    c=int(len(itemlist)/r)
    for i in range(r):
        newMat+='|'
        for j in range(c):
            newMat+=L[i*c+j]
            if j!=c-1:
                newMat+=' '
        newMat+='|\n'
    return newMat[:-1]

## fold line version
##def formatBMat(m):
##    rm=m.replace('|',' ')
##    l=rm.split()
##    L=[]
##    longest=len(l[0])
##    newMat=''
##    for item in l:
##        if len(item)>longest:
##            longest=len(item)
##    for item in l:
##        L.append(('{:'+str(longest)+'}').format(item))
##    r=m.count('\n')+1
##    c=int(len(l)/r)
##    for i in range(r):
##        if i==0:
##            newMat+='┌'
##        elif i==r-1:
##            newMat+='└'
##        else:
##            newMat+=' |'
##        for j in range(c):
##            newMat+=L[i*r+j]
##            if j!=c-1:
##                newMat+=' '
##        if i==0:
##            newMat+='┐\n'
##        elif i==r-1:
##            newMat+='┘'
##        else:
##            newMat+='|\n'
##    return newMat

def matrixMultiplication():
    rightMat=input('Please type in your right matrix in any form except string form.\n>>>')
    rightPower=1
    mp=[]
    if rightMat.count('^')==1:
        mp=rightMat.split('^')
        rightPower=eval(mp[1])
    elif rightMat.count('**')==1:
        mp=rightMat.split('**')
        rightPower=eval(mp[1])
    else:
        mp=[rightMat]
    if type(rightPower)!=int:
        print('The exponent must be integers! Please type again!\n')
        matrixMultiplication()
        return
    rightMat=mp[0]
    if formJudge(rightMat)==False:
        print('Your right matrix form is not supported! Please type again!\n')
        matrixMultiplication()
        return
    elif formJudge(rightMat)=='s':
        print('String form is not supported currently, please type again!\n')
        matrixMultiplication()
        return
    rightMat=eval(matrixConvert('w',rightMat))
    ml=len(rightMat)
    nl=len(rightMat[0])
    if rightPower!=1:
        if ml==nl:
            for power in range(rightPower):
                lst=[]
                for i in range(ml):
                    l=[]
                    for j in range(ml):
                        item=0
                        for k in range(ml):
                            item+=rightMat[i][k]*rightMat[k][j]
                        l.append(item)
                    lst.append(l)
                rightMat=lst
        else:
            print('This matrix can\'t be powered! Please type again!\n')
            matrixMultiplication()
            return
    while True:
        leftMat=input('Please type in your left matrix in any form besides string form, no input will stop this function.\n>>> ')
        leftPower=1
        if leftMat=='':
            break
        elif leftMat.count('^')==1:
            leftPower=int(leftMat.split('^')[1])
            leftMat=leftMat.split('^')[0]
        elif leftMat.count('**')==1:
            leftPower=int(leftMat.split('**')[1])
            leftMat=leftMat.split('**')[0]
        elif leftPower!=1:
            print('This matrix can\'t be powered! Please type again!\n')
            continue
        if formJudge(leftMat)==False:
            print('Your left matrix form is not supported! Please type again!\n')
            continue
        leftMat=eval(matrixConvert(form='w',matrix=leftMat))
        mr=len(leftMat)
        nr=len(leftMat[0])
        if nl!=mr:
            print('We can\'t do multiplication with these 2 matrices! Please type again!\n')
            continue
        for power in range(leftPower):
            lst=[]
            for i in range(ml):
                l=[]
                for j in range(nr):
                    item=0
                    for k in range(nl):
                        item+=leftMat[i][k]*rightMat[k][j]
                    l.append(item)
                lst.append(l)
            rightMat=lst
    if input('Do you want to beautify this matrix? Type \'y\' representing \'yes\', other input will be regarded as \'no\'.\n>>> ').lower()==( 'y' or 'yes' ):
        print(matrixConvert(form='b',matrix=str(rightMat).replace(' ','')))
    else:
        print('The result matrix is:\n{}'.format(str(rightMat).replace(' ','')))

##abbreviation
mtp=matrixMultiplication

def determinantLaTeX(size=0,determinant='',printOrReturn='p'):
    output=matrixProducer(size,size,determinant,'d')
    if printOrReturn=='p':
        print('By using this function you will get a determinant in LaTeX form.')
        print('The matrix you want in LaTeX is:\n\n'+output+'\n')
        print('And it has the VALUE:   '+str(determinantCalculation(finalDeterminant)))
    else:
        return output

##abbreviation
dl=determinantLaTeX

def determinantCalculation(inputDet=''):
    if inputDet=='':
        det=input('Please input your determinant in LaTeX form or in WolframAlpha form: ')
    else:
        det=inputDet
    if formJudge(det) not in ['dl','w']:
        print('Please type in the correct form!\n')
        determinantCalculation()
        return
    else:
        det=eval(matrixConvert('w',det))
        def compute(determinant):
            if len(determinant)==1:
                determinantValue=determinant[0][0]
            else:
                determinantValue=0
                for i in range(len(determinant)):
                    n=[[row[j] for j in range(len(determinant)) if j != i] for row in determinant[1:]]
                    if i%2==0:
                        determinantValue+=determinant[0][i]*compute(n)
                    else:
                        determinantValue-=determinant[0][i]*compute(n)
            return determinantValue
        detValue=compute(det)
    if inputDet==None:
        print('The value of your determinant is {}.'.format(detValue))
    else:
        return detValue

##abbreviation
dc=determinantCalculation

def boldedRLaTeX(n=0):
    if n:
        return ('$$\mathbb{R}^'+str(n)+'$$')
    else:
        n=input('How many dimensions would you like?\n>>> ')
        if n:
            print('$$\mathbb{R}^'+n+'$$')
        else:
            print('$$\mathbb{R}$$')

##abbreviation
br=boldedRLaTeX

def fractionLaTeX(numerator=None,denominator=None):
    if numerator==None or denominator==None:
        if numerator==None:
            numerator=input('Please type in numerator here: ')
        if denominator==None:
            denominator=input('Please type in denominator here: ')
        print('$$\\frac{'+numerator+'}{'+denominator+'}$$')
    else:
        return ('$$\\frac{'+str(numerator)+'}{'+str(denominator)+'}$$')

##abbreviation
fl=fractionLaTeX

def vectorLaTeX(entry=None,vector=True,overRightArrow=False):
    if entry==None:
        entry=input('Please input your entry here: ')
    if vector==True and overRightArrow==False:
        print('$$vec{'+entry+'}$$')
    elif overRightArrow==True:
        print('$$overrightarrow{'+entry+'}$$')

##abbreviation
vl=vectorLaTeX

def advancedSplit(s):
    lst=[]
    d={'\'':0,'\"':0,'(':0,')':0,'[':0,']':0,'{':0,'}':0}
    item=''
    for i in range(len(s)):
        ch=s[i]
        if ch in d:
            d[ch]+=1
        if ch in [' ',','] and s[i-1] not in [' ',','] and d['\'']%2==0 and d['\"']%2==0 and d['(']==d[')'] and d['[']==d[']'] and d['{']==d['}']:
           lst.append(item)
           item=''
           ch=''
        item+=ch
        if i==len(s)-1:
            lst.append(item)
    return lst

def pi(precision=None):
    if precision:
        return sum([ 4*(-1)**i/(2*i+1) for i in range(precision)])
    return 3.141592653589793

##def e(precision=None):
##    if precision:
##        return (1+1/n)**n
##    return 2.718281828459045

