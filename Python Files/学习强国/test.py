import time

for i in range(10):
    print('Loading' + i * '.', end='\r')
    time.sleep(1)