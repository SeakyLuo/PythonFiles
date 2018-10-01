from tkinter import *
from random import *
import sys

root=Tk()

class GreedySnake(Frame):
    def __init__(self,master,x=1600,y=900,size=50,nFood=1):
        Frame.__init__(self,master)
        self.height=y
        self.width=x
        self.pixel=size
        self.master=master
        self.canvas=Canvas(self,height=y,width=x,relief=SUNKEN,borderwidth=3)
        self.canvas.pack()
        self.canvas.bind_all('<KeyRelease>',self.turn)
        self.directions=['Up','Down','Left','Right']
        self.moveDistance={'Up':(0,-size),'Down':(0,size),'Left':(-size,0),'Right':(size,0)}
        self.setup()
        for i in range(nFood):
            self.foodAppear()
        self.automove()

    def setup(self):
        self.dead=False
        self.headX,self.headY=self.width//2,self.height//2
        self.direction=choice(self.directions)
        bodyX,bodyY=self.moveDistance[self.direction]
        self.body=[(self.headX,self.headY),(self.headX-bodyX,self.headY-bodyY),(self.headX-2*bodyX,self.headY-2*bodyY)]
        for i,j in self.body:
            self.canvas.create_rectangle(i,j,i+self.pixel,j+self.pixel,fill='red',tags='snake')
        self.fooddict={}
        self.foodtag=0

    def turn(self,event):
        if event.keysym in self.directions:
            self.direction=event.keysym

    def automove(self):
        if self.dead:
            return
        x,y=self.moveDistance[self.direction]
        self.headX+=x
        self.headY+=y
        if (self.headX,self.headY) in self.fooddict:
            tag=self.fooddict[(self.headX,self.headY)]
            self.canvas.delete(tag)
            del self.fooddict[(self.headX,self.headY)]
            self.foodAppear()
        elif (self.headX,self.headY) in self.body[1:] or self.headX in [-self.pixel,self.width+self.pixel] or self.headY in [-self.pixel,self.height+self.pixel]:
            self.dead=True
            self.canvas.create_text(self.width//2,self.height//2,text='You Are Lost!',fill='black',font=('Helvetica',self.pixel*2,'bold italic'))
            restart=Button(text='Restart',font=('Helvetica',20,'bold italic'),relief=GROOVE,bg='yellow',command=self.restart)
            self.canvas.create_window(self.width//2-self.pixel,self.height//2+2*self.pixel,window=restart)
            Quit=Button(text='Quit',font=('Helvetica',20,'bold italic'),relief=GROOVE,bg='green',command=self.master.destroy)
            self.canvas.create_window(self.width//2+self.pixel,self.height//2+2*self.pixel,window=Quit)
        else:
            self.body.pop()
        self.body.insert(0,(self.headX,self.headY))
        self.canvas.delete('snake')
        for i,j in self.body:
            self.canvas.create_rectangle(i,j,i+self.pixel,j+self.pixel,fill='red',tags='snake')
        self.after(250,self.automove)

    def foodAppear(self):
        foodX,foodY=randrange(0,self.width,self.pixel),randrange(0,self.height,self.pixel)
        while (foodX,foodY) in self.body+list(self.fooddict.keys()):
            foodX,foodY=randrange(0,self.width,self.pixel),randrange(0,self.height,self.pixel)
        self.canvas.create_rectangle(foodX,foodY,foodX+self.pixel,foodY+self.pixel,fill='yellow',tags='food'+str(self.foodtag))
        self.fooddict[(foodX,foodY)]='food'+str(self.foodtag)
        self.foodtag+=1

    def restart(self):
        self.canvas.delete(ALL)
        self.setup()
        self.automove()

game=GreedySnake(root)
game.pack()
game.master.title("Greedy Snake")

root.mainloop()
