from random import *
from tkinter import *
from tkinter import messagebox

root=Tk()
class World(Frame):
    def __init__(self,parent,x=600,y=800,size=25):
        Frame.__init__(self,parent)
        self.canvas=Canvas(self,height=y,width=x,relief=SUNKEN,borderwidth=3)
        self.width,self.height=x,y
        self.pixel_size=size
        self.canvas.pack()
        self.birdX,self.birdY=200,400
        self.canvas.create_rectangle(self.birdX,self.birdY,self.birdX+self.pixel_size,self.birdY+self.pixel_size,fill='red',tags='bird')
        self.isFalling=True
        self.time=0
        self.interval=6*size
        self.points=0
        self.canvas.create_text(self.width//2,self.height//10,text=str(self.points),fill='black',font=('Helvetica',self.pixel_size*2,'bold italic'),tags='points')
        self.columns=[]
        self.column_size=2*self.pixel_size
        self.isAlive=True
        self.canvas.bind_all('<KeyRelease>',self.rise)
        self.generate_columns()
        self.move_columns()
        self.fall()

    def rise(self,event):
        if not self.isAlive:
            return
        if event.keysym=='Up':
            self.isFalling=False
            self.time=0
            self.up()
            self.isFalling=True

    def up(self):
        if self.time<15:
            self.time+=1
            self.birdY-=15-self.time
            self.canvas.delete('bird')
            self.canvas.create_rectangle(self.birdX,self.birdY,self.birdX+self.pixel_size,self.birdY+self.pixel_size,tags='bird',fill='red')
            self.judge()
            self.after(25,self.up)            
               
    def fall(self):
        if self.isFalling:
            self.birdY+=7.5          
            self.canvas.delete('bird')
            self.canvas.create_rectangle(self.birdX,self.birdY,self.birdX+self.pixel_size,self.birdY+self.pixel_size,tags='bird',fill='red')
            self.judge()
            if not self.isAlive and self.birdY+self.pixel_size>=self.height:
                return
            self.after(25,self.fall)

    def generate_columns(self):
        colX,colY=self.width,randrange(self.interval,self.height-self.interval,self.pixel_size)
        self.canvas.create_rectangle(colX,0,colX+self.column_size,colY,tags='col',fill='green')  #upper tube
        self.canvas.create_rectangle(colX,colY+self.interval,colX+self.column_size,self.height,tags='col',fill='green')   #lower tube
        self.columns.append((colX,colY))

    def move_columns(self):
        if not self.isAlive:
            return
        self.canvas.delete('col')
        for i in range(len(self.columns)):
            x,y=self.columns.pop(0)
            if x+2*self.pixel_size<0:                
                continue
            elif x<200+3*self.pixel_size and len(self.columns)==0:
                self.generate_columns()
            elif x+2*self.pixel_size==self.birdX:
                self.canvas.delete('points')
                self.points+=1
                self.canvas.create_text(self.width//2,self.height//10,text=str(self.points),fill='black',font=('Helvetica',self.pixel_size*2,'bold italic'),tags='points')
            x-=5
            self.columns.append((x,y))
            self.canvas.create_rectangle(x,0,x+self.column_size,y,tags='col',fill='green')  #upper tube
            self.canvas.create_rectangle(x,y+self.interval,x+self.column_size,self.height,tags='col',fill='green')   #lower tube
        self.canvas.after(40,self.move_columns)

    def judge(self):
        x,y=self.columns[-1]
        if self.birdY+self.pixel_size>self.height or \
        (x+self.column_size>self.birdX+self.pixel_size>x and self.birdY+self.pixel_size>y+self.interval) or \
        (x<self.birdX<x+self.column_size and self.birdY+self.pixel_size>y+self.interval) or\
        (x+self.column_size>self.birdX+self.pixel_size>x and self.birdY<y) or\
        (x<self.birdX<x+self.column_size and self.birdY<y):
            messagebox.showinfo('You Are Lost!',f'You got {self.points} points.')
            self.isAlive=False            

game=World(root)
game.pack()
game.master.title("Flappy Bird")
root.mainloop()
