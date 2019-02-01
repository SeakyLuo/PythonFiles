import ez
from ezs import ac, multiply, integer
import math

class stats:
    def __init__(self, *numbers, precision = 4, Print = True):
        '''Anaylyze numbers only.
        Usage: s = stat(1, 2, 3, 4, 5, 10, range(1, 21, 2), precision = 2, Print = False)
        Set precision to a specific number to round the results.
        If precision is negative, results will be as precise as possible.
        Set Print to False for not printing the result automatically.'''
        self.print = Print
        self.precision = precision
        self.data = ()
        for i in numbers:
            if type(i) == range:
                self.data += tuple(i)
            else:
                self.data += (integer(i), )
        try:
            self.calculate()
            self.round(self.precision)
        except TypeError:
            raise ez.DataTypeError
        self.getInfo()
        if Print:
            print(f'Your input data is:\n{self.data}')
            print(self.info)

    def __add__(self, other):
        '''Combine the two data.
            Precision will be set to the smaller value.
            Will not print the info if any Print is equal to False.
            '''
        return stats(*(self.data + other.data), \
                     precision = min(self.precision, other.precision), \
                     Print = self.print * other.print)

    def __str__(self):
        return self.info

    def __repr__(self):
        return repr(self.data)

    def calculate(self):
        '''Calculate various data.'''
        self.num = len(self.data)
        if self.num == 1 or self.data == (self.data[0], )*self.num:
            raise Exception('Are you serious???')
        self.sorted = sorted(self.data)
        self.count = ez.find(self.sorted).count()
        self.nodup = ez.rmdup(self.data)
        self.max = self.sorted[-1]
        self.min = self.sorted[0]
        self.mean = integer(sum(self.data)/self.num)
        self.median()
        self.mode = ez.find(self.count).key(max(self.count[k] for k in self.count))
        if set(self.mode) == set(self.data):
            self.mode = None
        self.var = sum((data - self.mean) ** 2 for data in self.data) / self.num
        self.sd = self.var ** 0.5
        self.ad = sum(abs(data - self.mean) for data in self.data) / self.num
        self.outlier()
        self.groups = {}

    def Max(self, nth = 1):
        '''Find the nth greatest number.'''
        return self.sorted[-nth]

    def Min(self, nth = 1):
        '''Find the nth least number.'''
        return self.sorted[nth - 1]

    def Mean(self, precision = 4):
        '''Find Arithmatic Mean, Geometric Mean, Harmonic Mean, Weighted Arithmatic Mean and Square Mean.'''
        self.precision = precision
        self.AM = sum(self.data) / self.num
        self.AM = integer(self.AM)
        self.GM = multiply(self.data) ** (1 / self.num)
        self.HM = self.num / sum(1 / n for n in self.data)
        self.wAM = sum(k * self.count[k] for k in self.count)/self.num
        self.SM = (sum(n ** 2 for n in self.data) / len(self.data)) ** 0.5
        if precision > 0:
            self.AM = round(self.AM, precision)
            self.GM = round(self.GM, precision)
            self.HM = round(self.HM, precision)
            self.wAM = round(self.wAM, precision)
            self.SM = round(self.SM, precision)
        print(f'''Arithmatic Mean: {self.AM}
                Geometric Mean: {self.GM}
                Harmonic Mean: {self.HM}
                Weighted Arithmatic Mean: {self.wAM}
                Square Mean: {self.SM}''')

    def Median(self, precision = 4):
        '''Find the median.'''
        self.precision = precision
        if self.num % 2:
            self.median = self.sorted[(self.num - 1) // 2]
        else:
            self.median = ac(repr((self.sorted[self.num // 2 - 1] + self.sorted[self.num // 2]) / 2))
            if precision:
                self.median = round(self.median, self.precision)

    def outlier(self):
        '''Outliers: less than Q1-1.5*interquartile or greater than Q3+1.5*interquartile.'''
        if self.num >= 4:
            mod = self.num % 4
            if mod:
                self.q1 = self.sorted[(self.num - mod) // 4]
                self.q3 = self.sorted[(self.num * 3 - 4 + mod) // 4]
            else:
                self.q1 = (self.sorted[self.num // 4 - 1] + self.sorted[self.num // 4]) / 2
                self.q3 = (self.sorted[self.num * 3 // 4 - 1] + self.sorted[self.num * 3 // 4]) / 2
            self.interquartile = self.q3 - self.q1
            outliers = ez.rmdup([i for i in self.sorted if i < self.q1 - 1.5 * self.interquartile or i > self.q3 + 1.5 * self.interquartile])
            self.outliers = outliers or None
            return self.outliers

    def add(self, *numbers):
        '''Add numbers to the data.'''
        if numbers:
            num = len(numbers)
            if num == 1:
                print('1 number is added.')
            else:
                print('{num} numbers are added.')
            self.data += numbers
            self.calculate()
        else:
            print('Nothing is added.')

    def round(self, precision = 4):
        '''Round numbers to a specific precision.
            If precision is negative, results will be as precise as possible.'''
        self.precision = precision
        self.mean = sum(self.data) / self.num
        self.median(precision)
        self.var = sum((data - self.mean) ** 2 for data in self.data) / self.num
        self.sd = self.var ** 0.5
        self.ad = sum(abs(data - self.mean) for data in self.data) / self.num
        if precision >= 0:
            self.mean = round(self.mean, precision)
            self.var = round(self.var, precision)
            self.sd = round(self.sd, precision)
            self.ad = round(self.ad, precision)

    def getInfo(self):
        '''Produce info to print.'''
        mode = str(list(self.mode))[1:-1] if self.mode else None
        outliers = str(self.outliers)[1:-1] if self.outlier else None
        self.info = f'''Count: {self.num}
Min: {self.min}
Max: {self.max}
Mean: {self.mean}
Median: {self.median}
Mode: {mode}
Variance: {self.var}
Standard Deviation: {self.sd}
Average Deviation: {self.ad}
Outliers: {outliers}'''

    def group(self, interval = 0):
        '''Group numbers with non-negative interval.
            If interval is 0, numbers will be grouped automatically.
            Otherwise it will be set to the given interval.'''
        self.groups = {}
        absmax = max(abs(i) for i in self.data)
        absmin = min(abs(i) for i in self.data)
        dmax = int(math.log(absmax, 10)) + 1
        dmin = 1
        if absmin:
            dmin = int(math.log(absmin, 10)) + 1
        dmdiff = dmax-dmin
        if interval == 0:
            diff = absmax - absmin
            ddiff = int(math.log(diff, 10)) + 1
            if dmdiff == 0:
                ## 不够好
                interval = 10 ** ddiff
                if ddiff < dmax:
                    self.groups = self.count
                    return self.groups
                if ddiff == dmax:
                    interval //= 10
            elif dmdiff == 1:
                interval = 10 ** dmin
            elif dmdiff == 2:
                interval = 10 ** dmin
                if ddiff == dmax:
                    interval *= 10
            elif dmdiff >= 3:
                ## 也许可以优化
                interval = 10
        if dmdiff < 3:
            mini = self.min // interval * interval
            maxi = (self.max // interval + 1) * interval
            while mini != maxi:
                for k in self.count:
                    upper = mini + interval
                    if mini <= k < upper:
                        key = f'[{mini}, {upper})'
                        self.groups[key] = self.groups.get(key, 0) + self.count[k]
                mini += interval
        else:
            nmin = nmax = 0
            try:
                ## n 表示 negative
                nmin = integer(-10**int(math.log(-min(k for k in self.count if k < 0), 10) + 1))
                nmax = integer(-10**int(math.log(-max(k for k in self.count if k < 0), 10) + 1))
            except ValueError:
                pass
            ## p 表示 positive
            pmin = 10 ** (dmin - 1)
            pmax = 10 ** dmax
            while nmin < nmax or pmin < pmax:
                for k in self.count:
                    nupper = nmin // interval
                    pupper = pmin * interval
                    key = ''
                    if nmin <= k<nupper:
                        key = f'[{nmin}, {nupper})'
                    elif -1 <= k<1:
                        key = '[-1, 1)'
                        if not nmax:
                            key = '[0, 1)'
                        elif not pmax:
                            key = '[-1, 0)'
                    elif pmin <= k<pupper:
                        key = f'[{pmin}, {pupper})'
                    if key:
                        self.groups[key] = self.groups.get(key, 0) + self.count[k]
                nmin //= interval
                pmin *= interval
            self.groups = { k:self.groups[k] for k in sorted(self.groups, key = lambda x: eval(ez.find(x).between('[', ', ')))}
        return self.groups

    def rm(self, *nums, number = 'out'):
        '''Remove nums from self.data.
            Set number to 'out' to remove outliers (Default).
            Set number to min to remove minimum values.
            Set number to max to remove maximum values.'''
        if number == 'out':
            if self.num > 4 and self.outliers:
                self.data = [i for i in self.data if i not in self.outliers]
            else:
                print('No outliers.')
                return
        else:
            if number == max:
                number = self.max
            elif number == min:
                number = self.min
            self.data = [i for i in self.data if i not in (number, *nums)]
        before = self.num
        self.calculate()
        difference = before-self.num
        if difference == 1:
            print('1 number is removed.')
        else:
            print(f'{difference} numbers are removed.')

    def plot(self, interval = 0, font = ("Helvetica", 16, 'normal'), color = "yellow", percent = False):
        '''Use cTurtle to plot a histogram.
            Default Font: Helvetica, 16, normal.
            Default binColor: yellow.
            Default Display: not in percentage'''
        import cTurtle
        self.group(interval)
        lower = eval(ez.find(list(self.groups.keys())[0]).between('[', ', '))
        interval = interval or eval(ez.find(list(self.groups.keys())[0]).between(', ', ')'))-lower
        upper = eval(ez.find(list(self.groups.keys())[-1]).between(', ', ')'))
        deltaBins = upper - lower
        xMin = lower - 0.1 * deltaBins
        xMax = upper + 0.1 * deltaBins
        yMin = -0.1
        yMax = 1.1
        ct = cTurtle.Turtle()
        ct.speed(0)
        ct.setWorldCoordinates(xMin, yMin, xMax, yMax)
        ct.hideturtle()
        ct.up()
        ct.pencolor("black")
        ct.fillcolor(color)

        maxValue  =  max(self.groups.values())
        while True:
            ct.goto(lower, -0.05)
            ct.write(lower, font = font)
            ct.goto(lower, 0)
            ct.down()
            value = self.groups.get(f'[{lower}, {lower + interval})', 0)
            if value:
                height = value / maxValue
                ct.begin_fill()
                ct.goto(lower, height)
                ct.goto(lower + interval, height)
                ct.goto(lower + interval, 0)
                ct.goto(lower, 0)
                ct.end_fill()
                ct.up()
                if percent:
                    value = str(round(integer(value / self.num * 100), 2)) + '%'
                else:
                    value = str(value)
                ct.goto(lower + 0.5 * interval, height)
                ct.write(value, align = 'center', font = (font[0], int(font[1] * 0.75) if len(value) > 2 * interval else font[1], font[2]))
                if lower + interval == upper:
                    ct.goto(upper, -0.05)
                    ct.write(upper, font = font)
                    break
            else:
                ct.goto(lower + interval, 0)
                ct.up()
            lower += interval

##s = stats(44, 32, 40, 42, 39, 33, 47, 45, 38, 42, 49, 45, 43, 43, 31, 38, 38, 42, 36, 37, 28, 48, 38, 45, 43, 46, 36, 50, 46, 48, 27, 46, 47, 44, 44, 48, 37, 48, 49, 47, 49, 40, 40, 41, 48, 42, 42, 41, 43, 27, 27, 40, 38, 40, 42, 45, 46, 46, 49, 37, 43, 36, 41, 36, 43, 46, 47, 46, 47, 22, 49, 49, 41, 44, 41, 43, 40, 45, 48)
##s = stats(50, 42, 57, 36, 0, 54, 56, 50, 36, 45, 42, 49, 45, 54, 44, 47, 62, 54, 57, 40, 36, 43, 52, 39, 29, 0, 56, 40, 49, 52, 38, 48, 48, 46, 39, 35, 59, 47, 51, 55, 49, 56, 43, 53, 49, 53, 59, 44, 53, 28, 56, 57, 55, 45, 40, 55, 38, 48, 43, 43, 36, 42, 40, 42, 42, 48, 41, 46, 41, 36, 47, 56, 39, 48, 59, 53, 58, 54, 44, 44, 64, 58, 53, 61, 45, 37, 52, 49, 46, 59, 30, 44, 50, 35, 55, 51, 44, 52, 0, 49, 39, 39, 47, 45, 50, 47, 59, 47, 23, 46, 34, 52, 33, 42, 36, 32, 51, 27, 44, 43, 52, 49, 55, 51, 43, 46, 45, 57, 53, 57, 52, 33, 56, 54, 57, 52, 33, 32, 23, 52, 44, 54, 59, 41, 54, 43, 39, 59, 21, 53, 40, 45, 52, 62, 50, 41, 49, 49, 57, 32, 46, 49, 48, 50, 53, 41, 52, 44, 46, 38, 47, 45, 36, 35, 46, 49, 42, 50, 33, 54, 51, 60, 58, 46, 44, 28, 34, 64, 51, 58, 39, 37, 51, 50, 37, 44, 36, 26, 56, 53, 33, 41, 44, 34, 34, 34, 54, 36, 41, 35, 48, 28, 34, 51, 41, 53, 35, 59, 46, 44, 52, 56, 51, 59, 47, 37, 49, 52, 52, 53, 34, 53, 41, 47, 52, 44, 0, 31, 39, 0, 51, 54, 49, 48, 44, 53, 0, 50, 50)
##s = stats(47, 39, 43, 38, 37, 43, 45, 40, 40, 42, 46, 47, 44, 45, 42, 36, 40, 40, 37, 45, 44, 41, 45, 36, 42, 38, 43, 47, 46, 27, 41, 45, 42, 43, 45, 40, 48, 45, 45, 46, 40, 38, 35, 48, 46, 47, 33, 37, 28, 35, 34, 44, 45, 42, 48, 46, 46, 40, 47, 42, 46, 45, 37, 48, 45, 39, 37, 40, 42, 42, 38, 47, 47, 35, 32, 46, 49)
