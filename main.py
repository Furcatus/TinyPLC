counter = 0

def init():
    print("Init")

def loop():
    global counter
    
    counter = counter + 1
    
    if (counter % 100) == 0:
        print(counter)