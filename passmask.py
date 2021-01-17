import sys,termios
import atexit 

def initproc():

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    print(old_settings)
    new_set = old_settings[:]
    new_set[0] = new_set[0] & ~(termios.BRKINT  | termios.ICRNL  | termios.IXON | termios.ISTRIP | termios.INPCK)
    #new_set[1] = new_set[1] & ~(termios.OPOST)
    new_set[3] = new_set[3] & ~(termios.ICANON | termios.ECHO | termios.IEXTEN | termios.ISIG)
    new_set[6][termios.VMIN] = 1
    new_set[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_set)
    return old_settings,fd  


def getch():   
    try:
        ch = sys.stdin.read(1)
       
    except BaseException as error:
        print('An exception occurred')
    return ch


old, fd =  initproc()

@atexit.register
def atend():
    termios.tcsetattr(fd, termios.TCSANOW, old) 
    #sys.stdout.flush()

def precheck(message,symbol):
    if(message == ''):
        print('Enter proper prompt. Exiting..')
        sys.exit()
    if(len(symbol)> 1):
        print('Only 1 character is allowed as a mask symbol. Exiting..')
        sys.exit() 
    if(symbol == ''):
        print('Enter proper symbol for mask. Exiting..')  
        sys.exit()

# atexit.register(atend)
def masked(message = 'Enter password : ', symbol = '*'):

    precheck(message,symbol)
    sys.stdout.write(message)
    sys.stdout.flush()
    key = ''
    while True:
        val  = ord(getch())
        if val == 13:
            #print("inside")
            sys.stdout.write('\n')
            termios.tcsetattr(fd, termios.TCSAFLUSH, old) 
            sys.stdout.flush()  
            break
        elif val == 8 or val ==127:
            if len(key) > 0:
                sys.stdout.write('\b \b') 
                key = key[:-1]
                sys.stdout.flush()
        elif val in (3,22,15):
            break        
        else:

            sys.stdout.write(symbol)
            sys.stdout.flush()
            key +=  chr(val)

    return key 

