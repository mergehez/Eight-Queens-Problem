import sys
import tkinter as tk
import tkinter.messagebox as msgbox


## GameBoard class from http://stackoverflow.com/a/4959995/2999554
class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=32, color1="white", color2="blue"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


# image for queen
imagedata = '''
    iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAtAAAALQB65csewAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFWSURBVEiJ1ZUxTgJREIa/QU02aEOk4AgmFDS2hlgbTkCzFTEcwcaEPQUVva0JB9iESk9AC0dQTFAZC2fNY308V9Yt/JNJ9s375/9n3r7NiqpSJWq/IYtIU0SalRiIyC2wBJb2XAyq+mMADWAFqMUKaBSpLTrBARA568hyhXAGjIEboB6YInEmSAK8ummNTZvUKRwGCicObxLgDR1eWrPzzXDqG1FELoHYScWW88HVaAB0bYo1MPB0FAFzp6ss5kDk4Q9MKwW67sYUeAP6gbPPR5Lj9k1j+pVzNkdW9A7ElmtbN7sM1kDbuLHVKjDyGfScwg1wDcwC4lnMjLtxcj2fQauAWNFofTMwk8UfiC9CX/ID5bGl8f8NxP3hiMgxn7epDO5V9TlbHOY2X4Ar4GhP8VfgbiuTu0Udyt+iTugWXezZ+U6Nyg3yL/kcOClp8KSqj16DKvABRL2gKnTXZ/kAAAAASUVORK5CYII=
'''





## Queens class from http://svn.python.org/projects/python/trunk/Demo/scripts/queens.py

N = 8   # Number of Columns, for chess board
M = 1   # Number of Solutions
class Queens:

    def __init__(self, n=N, m=M):
        self.n = n
        self.m = m
        self.reset()
    def setM(self,m=M):
        self.m = m
    def getM(self):
        return self.m
    def reset(self):
        n = self.n
        m = self.m
        self.y = [None] * n                     # Where is the queen in column x
        self.row = [0] * n                      # Is row[y] safe?
        self.up = [0] * (2*n-1)                 # Is upward diagonal[x-y] safe?
        self.down = [0] * (2*n-1)               # Is downward diagonal[x+y] safe?
        self.nfound = 0                         # Instrumentation

        # All Solutions (3d array of zeros) [sol][row][col]
        self.sols = [[[0 for k in range(n)] for j in range(n)] for i in range(m+1)]
    def add(self, c, r, x):
        self.sols[c][r][x] = 1

    def solve(self, x=0):               # Recursive solver
        for y in range(self.n):
            if self.safe(x, y):
                self.place(x, y)
                if x+1 == self.n:
                    if self.nfound == self.m:
                        return
                    self.display()
                else:
                    self.solve(x+1)
                self.remove(x, y)

    def safe(self, x, y):
        return not self.row[y] and not self.up[x-y] and not self.down[x+y]

    def place(self, x, y):
        self.y[x] = y
        self.row[y] = 1
        self.up[x-y] = 1
        self.down[x+y] = 1

    def remove(self, x, y):
        self.y[x] = None
        self.row[y] = 0
        self.up[x-y] = 0
        self.down[x+y] = 0

    silent = 0

    def display(self):
        rw=0
        print("------------------start----------------")
        for y in range(self.n-1, -1, -1):
            col = ''
            cl=y
            for x in range(self.n):
                if self.y[x] == y:
                    col += ' Q '
                    rw = int(x)
                else:
                    col += ' . '
            #print (col)
            self.add(self.nfound,rw,cl)
            print ("[sol][row][col]", self.nfound,rw,cl)
        print("------------------end----------------")
        rw=0
        cl=0
        self.nfound = self.nfound + 1

q = Queens(8,M)
root = tk.Tk()
board = GameBoard(root)
solnum=0;
def refresh():              # displaying chess border with a solution
    M = q.getM()
    global labeltext
    global solnum
    for i in range(q.n):                            # i is row
        for j in range(q.n):                        # j is column
            if q.sols[solnum][i][j] == 1:
                print ("[sol][row][col]", solnum,i,q.sols[solnum][i][j])
                board.addpiece("player"+str(i) , player1 , i, j)    # adding a queen to the board
    print("---------------"+str(solnum+1)+"-------------------")
    labeltext = str(solnum+1) + ". Solution"        # changing label text
    solnum = (solnum + 1)%(M);
    label.configure(text=labeltext)
    root.mainloop()

def getM(): # asking number of solutions
    global M
    global q
    a = "";
    try:
        a = int(input("How many solution do you want? "))
        if a<0:
            print("Must be a positive integer!!")
            getM()
        else:
            if a>92:    # For a 64-cell board, max number of solutions is 92
                print("Must be less than 92!!")
                getM()
            else:
                q = Queens(8,a)
                q.solve()       # inserting all solution to the solution array(q.sols)
                refresh()       
    except ValueError:
        print("Not an integer value!!")
        getM()
        
if __name__ == "__main__":
    label = tk.Label(root, text="", width=25)
    label.pack(pady=5)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    player1 = tk.PhotoImage(data=imagedata)
    btn = tk.Button(root,text='Refresh',width=25,command=refresh) 
    btn.pack(pady=10)
    n = N
    getM()
