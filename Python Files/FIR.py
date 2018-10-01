from tkinter import *
from random import choice

HEX=lambda x:hex(x)[-1].upper()
def play(player='0',opp='*',mode='PVE'):
    root=Tk()
    fir=FIR(root,player,opp,mode)
    root.wm_title("五子棋")
    root.mainloop()

class FIR:
    def __init__(self,master,player='0',opp='*',mode='PVE'):
        self.master=master
        self.player=player
        self.opp=opp
        self.empty="_"
        self.mode=mode
        for i in range(16):
            Label(self.master,width=2,text=HEX(i)).grid(row=0,column=i)
            Label(self.master,width=2,text=HEX(i)).grid(row=i,column=0)
        self.restartButton=Button(self.master,text='Restart',command=self.restart)
        self.restartButton.grid(row=1,column=16)
        self.undo=Button(self.master,text='Undo',command=self.undo)
        self.undo.grid(row=1,column=17)
        self.modeLabel=Label(self.master,text='Mode')
        self.modeLabel.grid(row=2,column=16)
        self.modeButton=Button(self.master,text=self.mode,command=self.switchMode)
        self.modeButton.grid(row=2,column=17)
        self.setup()
        print('游戏开始啦~你是{}，电脑是{}'.format(self.player,self.opp))

    def setup(self):
        self.gameover=False
        self.playerLabel=Label(self.master,text=['玩家1','你'][self.mode=='PVE'])
        self.playerLabel.grid(row=3,column=16)
        self.playerBox=Entry(self.master,width=3)
        self.playerBox.grid(row=3,column=17)
        self.playerBox.insert(0,self.player)
        self.oppLabel=Label(self.master,text=['玩家2','电脑'][self.mode=='PVE'])
        self.oppLabel.grid(row=4,column=16)
        self.oppBox=Entry(self.master,width=3)
        self.oppBox.grid(row=4,column=17)
        self.oppBox.insert(0,self.opp)

        self.objs={(i,j):self.empty for i in range(1,16) for j in range(1,16)}
        self.grid=self.objs.copy()
        for i in range(1,16):
            for j in range(1,16):
                obj=Button(self.master,width=2)
                obj.configure(command=lambda button=obj:self.put(button))
                obj.grid(row=i,column=j)
                self.objs[(i,j)]=obj
        self.moves=[]
        if choice([0,1]):
            if self.mode=='PVE':
                print('这次是电脑先哦')
                self.respond()
            elif self.mode=='PVP':
                print('这次是玩家'+self.opp+'先哦')
        else:
            print('这次是'+['玩家'+self.player,'你'][self.mode=='PVE']+'先下哦')

    def restart(self):
        player=self.playerBox.get()
        opp=self.oppBox.get()
        if player==opp:
            print('双方棋子不可以一样哦')
            return
        elif len(player)>1 or len(opp)>1:
            print('棋子只能用单个字符表示呢')
            return
        else:
            self.player=player
            self.opp=opp
        print('\n'+'='*5+'分割线'+'='*5+'\n')
        print('重新开始咯~')
        for loc in self.moves:
            self.objs[loc].grid_forget()
        self.setup()

    def switchMode(self):
        self.mode=['PVE','PVP'][self.mode=='PVE']
        self.modeButton.grid_forget()
        self.modeButton=Button(self.master,text=self.mode,command=self.switchMode)
        self.modeButton.grid(row=2,column=17)
        self.playerLabel.grid_forget()
        self.playerLabel=Label(self.master,text=['玩家1','你'][self.mode=='PVE'])
        self.playerLabel.grid(row=3,column=16)
        self.oppLabel.grid_forget()
        self.oppLabel=Label(self.master,text=['玩家2','电脑'][self.mode=='PVE'])
        self.oppLabel.grid(row=4,column=16)

    def undo(self):
        if self.gameover:
            print('游戏结束啦，不能悔棋啦')
            return
        for i in range(2):
            try:
                r,c=self.moves.pop()
            except IndexError:
                print('没有棋可以悔啦')
                return
            ## 显示哪一颗棋子被拿走
            self.grid[(r,c)]=self.empty
            self.objs[(r,c)].grid_forget()
            b=Button(self.master,width=2)
            b.configure(command=lambda button=b: self.put(button))
            b.grid(row=r,column=c)
        print('羞羞，怎么可以悔棋呐')

    def put(self,button):
        info=button.grid_info()
        r=info['row']
        c=info['column']
        button.grid_forget()
        Label(self.master,text=self.player).grid(row=r,column=c)
        self.moves.append((r,c))
        self.grid[(r,c)]=self.player
        if self.mode=='PVE':
            print('你把棋放在了({}, {})'.format(HEX(r),HEX(c)))
            self.respond()
        else:
            print('玩家{}把棋放在了({}, {})'.format(self.player,HEX(r),HEX(c)))
            if self.check(self.player)[0]==5:
                self.end("游戏结束啦，{}获得胜利~".format(self.player))
            else:
                self.player,self.opp=self.opp,self.player

    def respond(self):
        if self.moves:
            print('轮到电脑啦↓')
            num_player,defense=self.check(self.player)
            if num_player==5:
                self.end("哼哼赢了我这个笨笨的AI也没什么好高兴的~")
                return
            num_opp,offense=self.check(self.opp)
            ## 提升AI智商 从去掉choice做起
            ## 不知道try-except要不要用
            ## 好像会放在放过的上面= =
            try:
                if num_opp>=num_player and num_opp>1:
                    r,c=choice(offense)
                elif num_opp<num_player:
                    r,c=choice(defense)
                else:
                    r,c=choice(self.taolu())
            except IndexError:
                r,c=choice(self.taolu())
        else:
            ## 如果电脑先 中间随便放一个
            r=choice([7,8,9])
            c=choice([7,8,9])
            num_opp=1
        self.grid[(r,c)]=self.opp
        self.objs[(r,c)].grid_forget()
        Label(self.master,text=self.opp).grid(row=r,column=c)
        self.moves.append((r,c))
        print('电脑把棋放在了({}, {})'.format(HEX(r),HEX(c)))
        if self.check(self.opp)==(5,[]):
            self.end("辣鸡，居然输给人家这么笨的AI")
            return
        elif len(self.moves)==256:
            self.end("棋盘满啦，游戏平局.")
            return
        print('轮到你啦↓')

    def check(self,side):
        maximum=1
        isEmpty=lambda x,y:self.grid.get((x,y))==self.empty
        isSide=lambda x,y:self.grid.get((x,y))==side
        isOpp=lambda x,y:self.grid.get((x,y)) not in [self.empty,side]
        move={ 1:[], 2:[], 2.5:[], 3:[], 4:[]}
        directions=[(1,0),(0,1),(1,1),(1,-1)]
        for r,c in self.moves:
            if self.grid[(r,c)]!=side:
                continue
            for x,y in directions:
                line=''.join(self.grid.get((r+k*x,c+k*y),'') for k in range(1,5))
                if line=='':
                    continue
                count=1
                if line==side*4:
                    ## 如果不止5个相连请你圆润地离开
                    for k in range(5):
                        Label(self.master,text=side,bg='yellow').grid(row=r+k*x,column=c+k*y)
                    return 5,[]
                elif line.count(side)==3:
                    idx=line.find(self.empty)+1
                    if idx:
                        count=4
                        move[count].append((r+idx*x,c+idx*y))
                    elif line[:3]==side*3 and isEmpty(r-x,c-y):
                        count=4
                        move[count].append((r-x,c-y))
                elif line[:3].count(side)==2 and maximum<4:
                    idx=line[:3].find(self.empty)+1
                    if idx:
                        count=3
                        if isOpp(r-x,c-y) and isEmpty(r+4*x,c+4*y):
                            ## (*0_00_, *00_0_, *000__) 变 (*0_000, *00_00, *000_0)
                            count=2+idx/10
                            ## 感觉有点蠢 加个int()
                            move[int(count)]=move.get(count,[])+[(r+4*x,c+4*y)]
                        elif isEmpty(r-x,c-y) and isOpp(r+4*x,c+4*y):
                            ## (_0_00*, _00_0*, _000_*) 变 (00_00*, 000_0*, 0000_*)
                            count=2.4-idx/10
                            move[int(count)]=move.get(count,[])+[(r-x,c-y)]
                        move[count]=move.get(count,[])+[(r+idx*x,c+idx*y)]
                    elif line[:2]==side*2 and isEmpty(r-x,c-y) and isEmpty(r-2*x,c-2*y):
                        ## __000* 变 _0000*
                        count=2.3
                        move[count]=move.get(count,[])+[(r-x,c-y)]
                elif line[:2]==side+self.empty and isEmpty(r-x,c-y) and maximum<3:
                    if isEmpty(r+3*x,c+3*y) or isEmpty(r-2*x,c-2*y):
                        count=2
                        k=1
                        ## *__00__* || *_00__*
                        while isEmpty(r+(k+3)*x,c+(k+3)*y) and not isEmpty(r-(k+2)*x,c-(k+2)*y):
                            if isSide(r-(k+2)*x,c-(k+2)*y) or isOpp(r+(k+3)*x,c+(k+3)*y):
                                move[count].append((r-x,c-y))
                            if isSide(r+(k+3)*x,c+(k+3)*y) or isOpp(r-(k+2)*x,c-(k+2)*y):
                                move[count].append((r+2*x,c+2*y))
                            k+=1
                    if len(line)<3:
                        continue
                    if line[2]==self.empty:
                        for i,j in directions:
                            if (i,j)==(x,y):
                                continue
                            for k in range(2):
                                ## 破T型
                                for m in range(3):
                                    for d in [k+2,-(k+1)]:
                                        if isOpp(r+(d+(-1)**(d<0))*x,c+(d+(-1)**(d<0))*y):
                                            continue
                                        row=[ self.grid.get((r+d*x+n*i,c+d*y+n*j),'') for n in range(m-3,m+2)]
                                        if isOpp(r+d*x+(m-4)*i,c+d*y+(m-4)*j) or isOpp(r+d*x+(m+2)*i,c+d*y+(m+2)*j):
                                            continue
                                        if row.count(side)==2 and row.count(self.empty)==3 and not row[0]==row[-1]==side:
                                            count=2.5
                                            move[count].append((r+d*x,c+d*y))
                elif line[0]==self.empty and maximum<3:
                    # _0_0_ or _0__0_
                    length=len(line)
                    idx=line.find(side)
                    if length<3 or idx==-1 or not isEmpty(r-x,c-y) or not isEmpty(r+(idx+2)*x,c+(idx+2)*y):
                        continue
                    if idx in [1,2]:
                        count=2
                        move[count]+=[ (r+k*x,c+k*y) for k in range(1,1+idx)]
                    ## 破(_0_0_, _0__0_, _0___0_)的T型
                    for k in set((1,idx)):
                        for i,j in directions:
                            if (i,j)==(x,y):
                                continue
                            for m in range(2):
                                column=[self.grid.get((r+k*x+n*i,c+k*y+n*j),'') for n in range(m-2,m+2)]
                                if isOpp(r+k*x+(m-3)*i,c+k*y+(m-3)*j) or isOpp(r+k*x+(m+2)*i,c+k*y+(m+2)*j):
                                    continue
                                if column.count(side)==column.count(self.empty)==2:
                                    count=2.5
                                    move[count].append((r+k*x,c+k*y))
                ## 可以考虑一下 _0_0_0_的算法
                if count>maximum:
                    maximum=count
        return maximum,move[maximum]

    def taolu(self):
        x,y=self.moves[-1]
        k=1
        while True:
            loop=[ (x+i,y+j) for i in range(-k,k+1) for j in range(-k,k+1) if self.grid.get((x+i,y+j))==self.empty ]
            if loop:
                return loop
            k+=1

    def end(self,msg):
        overmsg='游戏已经结束啦，按Restart可以重新开始游戏，按Quit会退出游戏哦'
        if self.gameover:
            print(overmsg)
        else:
            print(msg)
            for i in range(1,16):
                for j in range(1,16):
                    if (i,j) in self.moves:
                        continue
                    Button(self.master,width=2,command=lambda :print(overmsg)).grid(row=i,column=j)
            self.gameover=True

play(player='0',opp='*',mode='PVE')
