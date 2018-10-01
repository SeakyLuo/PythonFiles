def add(d):
    return sum(k*d[k] for k in d)

def recursion(total,*args):
    def fill(method,arguments):
        for i,arg in enumerate(arguments):
            while add(method)<=total:
                method[arg]+=1
            method[arg]-=1
            if add(method)==total and method not in methods:
                methods.append(method.copy())
##                print(method)
            while method[arg]:
                method[arg]-=1
                fill(method,arguments[i+1:])
    methods=[]
    fill({arg:0 for arg in args},sorted(args))
    return methods
##print(recursion(106,10,20,50,1,2,5))

#dynamic programming
def dynamic(total,*args):
    lst=[0 for i in range(total+1)]
    lst[0]=1
    for arg in args:
        for i in range(arg,total+1):
            lst[i]+=lst[i-arg]
    return lst[total]
##print(dynamic(106,10,20,50,1,2,5))
