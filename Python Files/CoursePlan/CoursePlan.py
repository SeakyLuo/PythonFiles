from tkinter import *
from tkinter import messagebox
import ez
import atexit
## 1. Undetermined cource  2. schedule conflict 3. multiple schedule

TBA = 'T.B.A.'
aweekdays = ['m', 't', 'w', 'r', 'f']
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

def evaluateTime(time):
    '''Time format 12:30'''
    colon = time.find(':')
    h = eval(time[:colon])
    if h<8:
        h += 12
    m = time[colon+1:]
    if m[0] == '0':
        m = eval(m[1])
    else:
        m = eval(m)
    return h*60+m

def evalInfo(info):
    '''Help reduce the problem between Windows and Mac.'''
    if type(info) == str:
        return eval(info)
    return info

def overlap(time1, time2):
    t1 = [evaluateTime(t) for t in time1.split('-')]
    t2 = [evaluateTime(t) for t in time2.split('-')]
    if any(t1[0] <= t <= t1[1] for t in t2) or any(t2[0] <= t <= t2[1] for t in t1):
        return True
    return False

def length(t1, t2):
    return abs(evaluateTime(t2)-evaluateTime(t1))

def weekIndex(datetime):
    weekindex = 0
    while datetime[weekindex].isalpha():
        if datetime[weekindex] not in aweekdays: raise SyntaxError
        weekindex += 1
    return weekindex

class coursePlan(Frame):
    def __init__(self,  master):
        Frame.__init__(self,  master)
        self['bg'] = 'MintCream'
        self.buttonColor = 'lavender'
        self.labelWidth = 18
        self.buttonWidth = 6
        Label(self, text = 'Time', relief = FLAT, bg = '#00ffff', \
                  width = self.buttonWidth, height = 1).grid(row = 0, column = 0, sticky = NSEW)
        self.time = ['{}:{}0'.format((i//2+7)%12+1, [0, 3][i%2]) for i in range(24)]
        for i, date in enumerate(weekdays):
            Label(self, text = date, relief = FLAT, bg = '#00{}ff'.format(hex(250-i*25)[2:]), \
                  width = self.labelWidth, height = 1).grid(row = 0, column = i+1, sticky = NSEW)
        for i, time in enumerate(self.time):
            Label(self, text = time, relief = FLAT, bg = '#00{}ff'.format(hex(250-i*5)[2:]), \
                  width = self.buttonWidth, height = 1).grid(row = i+1, column = 0, sticky = NSEW)
        self.nameLabel = Label(self, text = 'Course:')
        self.nameBox = Entry(self)
        self.timeLabel = Label(self, text = 'Time:')
        self.timeBox = Entry(self)
        self.exampleText = 'Example: tr12-1:15'
        self.locLabel = Label(self, text = 'Location:')
        self.locBox = Entry(self)
        self.instructorLabel = Label(self, text = 'Instructor:')
        self.instructorBox = Entry(self)
        self.boxList = [self.nameBox, self.timeBox, self.locBox, self.instructorBox]
        for i, (box, label) in enumerate(zip(self.boxList, [self.nameLabel, self.timeLabel, self.locLabel, self.instructorLabel])):
            label.configure(bg = 'MistyRose', \
                            bd = 0, \
                            height = 1, \
                            width = self.labelWidth//2, \
                            relief = FLAT)
            label.grid(row = i, column = 6, sticky = NSEW)
            box.configure(bg = 'MistyRose', \
                           bd = 0, \
                           width = 3*self.labelWidth//2, \
                           relief = FLAT)
            box.grid(row = i, column = 7, columnspan = 3, sticky = NSEW)
            box.bind('<KeyRelease>',  self.switchBox)
            if i:
                box.bind('<FocusIn>',  self.focusIn)
                box.bind('<FocusOut>',  self.focusOut)
        self.setup()
        self.addButton = Button(self, text = 'Add', command = self.add)
        self.clearButton = Button(self, text = 'Clear', command = self.clear)
        self.readButton = Button(self, text = 'Read', command = self.read)
        self.saveButton = Button(self, text = 'Save', command = self.save)
        buttonList = [self.addButton, self.clearButton, self.readButton, self.saveButton]
        for i, button in enumerate(buttonList):
            self.configureButton(button)
            button.grid(row = i, column = 10, sticky = NSEW, columnspan = 2)
        clbggclr = 'Aquamarine' ## Course List bg color ## Aquamarine DeepSkyBlue Thistle SeaGreen1
        Label(self, text = 'Course List', relief = FLAT, bg = clbggclr, \
              bd = 0, width = 2*self.labelWidth, height = 1).grid(row = len(self.boxList), column = 6, columnspan = 4, sticky = NSEW)
        sortButton = Button(self, text = 'Sort', command = self.sort)
        self.configureButton(sortButton, clbggclr)
        sortButton.grid(row = len(self.boxList), column = 10)       
        dropAllButton = Button(self, text = 'DropAll', command = self.dropAll)
        self.configureButton(dropAllButton, clbggclr)
        dropAllButton.grid(row = len(self.boxList), column = 11)
        self.read()
        atexit.register(self.asksave)

    def setup(self):
        self.courseInfo = []
        self.courseLabels = []
        self.courseWidgets = []
        self.nameBox.focus()
        self.focusOut('<FocusOut>')
        self.modifyButtons = []
        self.exception = False

    def putLabel(self, name, datetime, loc, instructor, original = 0):
        datetime = datetime.lower()
        datetime = datetime.replace(' ', '')
        try:
            weekindex = weekIndex(datetime)
            if weekindex == 0: raise SyntaxError
            time = datetime[weekindex:].strip()
            if time.isnumeric():
                time = '{}:00-{}:50'.format(time, time)
            elif time.count('-') == 0 and time.count == 1:
                ## 4:00 -> 4:00-4:50
                time = time+'-'+time[:-2]+'50'
            elif time.count('-') == 1 and time.count(':')<2:
                ## 2-3:15 -> 2:00-3:15
                dash = time.find('-')
                start = time[:dash]
                if start.count(':') == 0:
                    start += ':00'
                end = time[dash:] ## 不用dash+1
                if end.count(':') == 0:
                    end += ':00'
                time = start+end
            elif time.count('-') != 1 or time.count(':')>2:
                raise SyntaxError
            ## 时间冲突有没有更好的解决办法
            for info in self.courseInfo:
                if original  ==  info: continue
                t2 = info[1]
                weekindex2 = weekIndex(t2)
                if any(weekday in datetime[:weekindex] and overlap(time, t2[weekindex2:]) for weekday in t2[:weekindex2]):
                    raise ValueError
        except SyntaxError:
            messagebox.showerror('Error', 'Invalid Time Format!\n'+self.exampleText)
            self.exception = True
            return
        except ValueError:
            messagebox.showerror('Error', 'Schedule conflict!')
            self.exception = True
            return
        dash = time.find('-')
        start = time[:dash]
        end = time[dash+1:]
        grids = length(start, end)//30+1
        datetime = datetime[:weekindex]+time
        courseButton = Button(self, text = name+[' --- '+loc, ''][loc == TBA], bg = 'Moccasin', \
                          bd = 0, width = 2*self.labelWidth, height = 1)
        courseButton['command'] = lambda :self.showCourseInfo(courseButton)
        index = -1
        if original:
            index = self.courseInfo.index(original)
            self.courseWidgets[index][0].grid_forget()
            courseButton.grid(row = index+len(self.boxList)+1, column = 6, columnspan = 3, sticky = NSEW)
            self.courseInfo[index] = (name, datetime, loc, instructor)
            for label in self.courseLabels[index]:
                label.grid_forget()
            self.courseLabels[index] = []
        else:
            rowNum = len(self.courseWidgets)+len(self.boxList)+1
            courseButton.grid(row = rowNum, column = 6, columnspan = 3, sticky = NSEW)
            copyButton = Button(self, text = 'Copy')
            copyButton['command'] = lambda :self.copy(copyButton)
            modifyButton = Button(self, text = 'Modify')
            modifyButton['command'] = lambda :self.modify(modifyButton)
            self.modifyButtons.append(modifyButton)
            dropButton = Button(self, text = 'Drop')
            dropButton['command'] = lambda :self.drop(dropButton)
            butts = [copyButton, modifyButton, dropButton]
            for i, button in enumerate(butts):
                self.configureButton(button)
                button.grid(row = rowNum, column = 9+i, sticky = NSEW)
            copyButton['bg'] = 'Moccasin'  ## PeachPuff
            self.courseWidgets.append((courseButton, copyButton, modifyButton, dropButton))
            self.courseInfo.append((name, datetime, loc, instructor))
            self.courseLabels.append([])

        for weekday in datetime[:weekindex]:
            label = Label(self, text = name+'\n'+loc, bg = 'RosyBrown1', \
                        bd = 0, width = self.labelWidth, height = grids)
            self.courseLabels[index].append(label)
            label.grid(row = self.time.index(start)+1, column = aweekdays.index(weekday)+1, rowspan = grids, sticky = NSEW)

    def add(self, original = 0):
        if len(self.courseInfo) == 20:
            messagebox.showerror('Error', 'You have reached the limit of courses!')
            return
        info = name, datetime, loc, instructor = (box.get() for box in self.boxList)
        if datetime in ('', self.exampleText) or info in self.courseInfo:
            return
        if name == '':
            messagebox.showerror('Error', 'Please input course name!')
            return
        self.putLabel(name, datetime, loc, instructor, original)
        if self.exception:
            self.exception = False
        else:
            self.clear()

    def read(self):
        self.setup()
        self.clear()
        info = []
        try:
            self.readInfo = ez.fread('schedule.txt')
        except FileNotFoundError:
            ez.fwrite('schedule.txt', info)
        if self.readInfo:
            for name, datetime, loc, instructor in self.readInfo:
                self.putLabel(name, datetime, loc, instructor)

    def asksave(self):
        root = Tk()
        root.withdraw()
        if self.courseInfo != self.readInfo:
            if self.readInfo:
                if messagebox.askyesno('Reminder', 'You have modified your schedule.\nDo you want to save it?'):
                    self.save()
            elif messagebox.askyesno('Reminder', 'Do you want to save your new schedule?'):
                self.save()

    def save(self):
        ez.fwrite('schedule.txt', self.courseInfo)
        self.readInfo = self.courseInfo
        messagebox.showinfo("Success",  "You have successfully saved your schedule!")

    def clear(self):
        for box in self.boxList:
            box.delete(0, END)
        self.focusOut('<FocusOut>')
        self.nameBox.focus()
        
    def copy(self, button):
        index = evalInfo(button.grid_info()['row'])-len(self.boxList)-1
        info = self.courseInfo[index]
        self.clear()
        self.focusIn(1)
        for i, box in enumerate(self.boxList):
            box.insert(0, info[i])

    def modify(self, button):
        self.clear()
        if button['text'] == 'Cancel':
            button['text'] = 'Modify'
        elif button['text'] == 'Modify':
            ## 如果先按了一个modify再按了另一个modify
            for mb in self.modifyButtons:
                if mb['text'] == 'Cancel':
                    self.modify(mb)
                    break
            index = evalInfo(button.grid_info()['row'])-len(self.boxList)-1
            info = self.courseInfo[index]
            self.focusIn(1)
            for i, box in enumerate(self.boxList):
                box.insert(0, info[i])
            self.addButton['command'] = lambda :self.modifyMode(button, info)
            button['text'] = 'Cancel'

    def modifyMode(self, button, info):
        self.add(info)
        self.addButton['command'] = self.add
        button['text'] = 'Modify'

    def drop(self, button):
        index = evalInfo(button.grid_info()['row'])-len(self.boxList)-1
        for label in self.courseLabels[index]:
            label.grid_forget()
        self.courseLabels.pop(index)
        self.courseInfo.pop(index)
        for widget in self.courseWidgets.pop(index):
            widget.grid_forget()
        for i, widgets in enumerate(self.courseWidgets[index:]):
            rowNum = i+index+len(self.boxList)+1
            for j, wid in enumerate(widgets):
                wid.grid_forget()
                wid.grid(row = rowNum, column = 6+j+(j != 0)*2, columnspan = 1+(j == 0)*2, sticky = NSEW)
                
    def dropAll(self):
        for lst in self.courseLabels:
            for label in lst:
                label.grid_forget()
        for widget in self.courseWidgets:
            for item in widget:
                item.grid_forget()
        self.setup()

    def showCourseInfo(self, button):
        index = evalInfo(button.grid_info()['row'])-len(self.boxList)-1
        info = self.courseInfo[index]
        info = f'Name: {info[0]}\nTime: {info[1]}\nLocation: {info[2]}\nInstructor: {info[3]}'
        messagebox.showinfo('Course Info', info)

    def sort(self):
        def key(x):
            name = ''
            number = ''
            level = ''
            i = 0
            ## by name
            while True:
                if x[0][i].isnumeric():
                    name = x[0][:i].strip().lower()
                    for ch in x[0][i:]:
                        if ch.isnumeric():
                            number += ch
                        elif ch.isalpha():
                            level += ch
                    number = eval(number)
                    level = level.lower()
                    break
                i += 1
            ## by time
            time = x[1][weekIndex(x[1]):]
            time = eval(time[:time.find(':')])
            if time<8: time += 12
            return (name, number, level, aweekdays.index(x[1][0]), time, x[2], x[3])
        copy = sorted(self.courseInfo.copy(), key = key)
        self.dropAll()
        for name, datetime, loc, instructor in copy:
            self.putLabel(name, datetime, loc, instructor)

    def configureButton(self, button, bg = '', height = 0, width = 0, bd = 0, relief = FLAT):
        button.configure(bg = bg or self.buttonColor, \
                         height = height, \
                         width = width or self.buttonWidth, \
                         bd = bd, \
                         relief = relief)

    def switchBox(self, event):
        key = event.keysym
        widget = event.widget
        index = self.boxList.index(widget)
        if key == 'Up':
            self.boxList[index-1].focus()
        elif key == 'Down':
            self.boxList[(index+1)%len(self.boxList)].focus()

    def focusIn(self, event):
        if event == 1:
            for wid in self.boxList[1:]:
                wid.delete(0, END)
                wid['fg'] = 'black'
        else:
            wid = event.widget
            if wid == self.timeBox and wid.get() == self.exampleText or\
               wid in [self.locBox, self.instructorBox] and wid.get() == TBA:
                wid.delete(0, END)
                wid['fg'] = 'black'

    def focusOut(self, event):
        if self.timeBox.get() == '':
            self.timeBox.insert(0, self.exampleText)
            self.timeBox['fg'] = 'grey39'
        if self.locBox.get() == '':
            self.locBox.insert(0, TBA)
            self.locBox['fg'] = 'grey39'
        if self.instructorBox.get() == '':
            self.instructorBox.insert(0, TBA)
            self.instructorBox['fg'] = 'grey39'

root = Tk()
cp = coursePlan(root)
cp.pack()
root.title('Schedule')
root.mainloop()

ez.py2pyw(__file__)
