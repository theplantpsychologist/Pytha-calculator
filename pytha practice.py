from tkinter import *
import random
root = Tk()
#canvas2 = Canvas(master,width=600,height = 600)
#canvas2.pack()
lines = []
clickcount = 0

def key(event):
    #print ("pressed", repr(event.char))
    pass
def linestart(event):
    #frame.focus_set()
    global cursor, vertexx, vertexy
    vertexx = event.x
    vertexy = event.y
    cursor = canvas2.create_oval(event.x+2, event.y+2,event.x -1, event.y-1,fill="red",outline="red")

def lineend(event):
    canvas2.delete(cursor)
    recent = canvas2.create_line(vertexx,vertexy,event.x,event.y,fill="red",width=2)
    lines.append(recent)

def click(event):
    global clickcount
    start = True
    #clickcount =+ 1
    if clickcount//2 != clickcount/2:
        lineend(event)
        clickcount+=1
        start = False
    if clickcount//2 == clickcount/2 and start:
        linestart(event)
        clickcount+=1

def undo():
    canvas2.delete(lines[-1])
    lines.pop()


    
canvas2 = Canvas(root, width=600, height=600)
canvas2.bind("<Key>", key)
canvas2.bind("<Button-1>", click)
#canvas2.bind("<Button-2>", lineend)

canvas2.pack()

def draw_grid(x,y,grid):
    for k in range(-10,x+20):
        canvas2.create_line(grid*k+100, 600, grid*k+100, 0, width = 0.5, fill="light grey")
    for k in range(-10,y+20):
        canvas2.create_line(0, 500-grid*k, 600, 500-grid*k, width = 0.5, fill = "light gray")
def draw_axis(x,y,grid):
    canvas2.create_line(100,500, 100 + grid*x, 500, width = 2)
    canvas2.create_line(100,500, 100, 500-grid*y, width = 2)

def draw_circles(x,y,grid,flap1,flap2):
    canvas2.create_oval(100+grid*x+grid*flap1, 500+grid*flap1, 100+grid*x-grid*flap1,500-grid*flap1, outline="cyan", width=1.5)
    canvas2.create_oval(100-grid*flap2, 500-grid*y-grid*flap2,100+grid*flap2,500-grid*y+grid*flap2, outline="cyan", width=1.5)    

def draw_boxes(x,y,grid,flap1,flap2):
    canvas2.create_rectangle(100+grid*x+grid*flap1, 500+grid*flap1, 100+grid*x-grid*flap1,500-grid*flap1, outline="cyan", width=1.5)
    canvas2.create_rectangle(100-grid*flap2, 500-grid*y-grid*flap2,100+grid*flap2,500-grid*y+grid*flap2, outline="cyan", width=1.5)   
    
def regenerate():
    global lines,clickcount,grid,x,y,flap1,flap2
    clickcount = 0
    lines =[]
    canvas2.delete("all")
    canvas2.create_rectangle(0,00,600,600,fill="white",outline="white")

    x = random.randint(5,15)
    y = random.randint(5,15)
    stretch = (x**2 + y**2) **0.5
    print("x axis:"+str(x),"  y axis:"+str(y))
    flap1 = random.randint(3,int(stretch)-3)
    flap2 = int(stretch)-flap1
    print("left circle:"+str(flap2),"  right circle:"+str(flap1))
    grid = 400/max(x+flap1,y+flap2)
    if grid < 400/17:
        grid = 400/17
    draw_grid(x,y,grid)
    draw_circles(x,y,grid,flap1,flap2)
    draw_boxes(x,y,grid,flap1,flap2)
    draw_axis(x,y,grid)
    if y == flap1 + flap2 or x == flap1 + flap2:
        regenerate()

def draw_setup():
    global lines,clickcount,grid,x,y,flap1,flap2
    clickcount = 0
    lines =[]
    canvas2.delete("all")
    canvas2.create_rectangle(0,00,600,600,fill="white",outline="white")

    Setup = eval(setup.get())
    x = Setup[0]
    y = Setup[1]
    flap1 = Setup[2]
    flap2 = Setup[3]
    print("x axis:"+str(x),"  y axis:"+str(y))
    print("left circle:"+str(flap2),"  right circle:"+str(flap1))
    grid = 400/max(x+flap1,y+flap2)
    #if grid < 400/17:
     #   grid = 400/17
    draw_grid(x,y,grid)
    draw_circles(x,y,grid,flap1,flap2)
    draw_boxes(x,y,grid,flap1,flap2)
    draw_axis(x,y,grid)
    if y == flap1 + flap2 or x == flap1 + flap2:
        regenerate()

def print_setup():
    global x, y, flap1, flap2
    print([x,y,flap1,flap2])

enter = Button(canvas2,text="random setup",command=regenerate)
enter.place(x=400,y=90)

enter = Button(canvas2,text="undo",command=undo)
enter.place(x=400,y=530)

#canvas2.create_text(300,30,text="Enter custom setup: [x,y,flapx,flapy]")
setup = Entry(root,bd=2,width=15)
setup.place(x=400,y=30)

enter = Button(canvas2,text="enter setup [x,y,flapx,flapy]",command=draw_setup)
enter.place(x=400,y=60)

enter = Button(canvas2,text="print current setup",command=print_setup)
enter.place(x=400,y=120)


def tkx(coordinate):
    return coordinate*grid + 100
def tky(coordinate):
    return 500-coordinate*grid


#nicecombos = []
#combos = []
#solutions = 0
def overlap():
    global bx,by,ax,ay, nicecombos, combos, solution, area
    bx = x-flap1
    by = y-flap2
    ax = flap2
    ay = flap1
    canvas2.create_rectangle(tkx(bx),tky(by),tkx(ax),tky(ay),outline="pink",width=2)
    area = abs((ax-bx)*(ay-by))/2
    def factor(area):
        global factor1, factor2, solution, combos, nicecombos
        combos = []
        nicecombos = []
        for x in range(1,int(area)):
            y = area/x
            niceness = abs(x-y)
            if x==int(x) and y==int(y):
                nicecombos.append([niceness,x])
            else:
                combos.append([niceness,x])
        if combos == []:
            x = 0.25
            while combos == []:
                y = area/x
                niceness = abs(x-y)
                combos.append([niceness,x])
                x += 0.25
            
        if nicecombos!=[]:
            factor1 = min(nicecombos)[1]
            solution = nicecombos.index(min(nicecombos))
        else:
            factor1 = min(combos)[1]
            solution = combos.index(min(combos))
        factor2 = area/factor1
        #print(factor1,factor2, combos)
    factor(area)

def rotate():
    global a2x,a2y
    a2x=bx+ay-by
    a2y=by+ax-bx
    canvas2.create_rectangle(tkx(bx),tky(by),tkx(a2x),tky(a2y),outline="purple",width=2)

def cd1():
    global cx,cy,dx,dy,a2x,a2y
    cx = a2x+factor1
    cy= by-factor1
    dx = bx-factor2
    dy = a2y + factor2
    if dy>y:
        gap = dy-y
        dy -= gap
        dx += gap
        cy -= gap
        cx += gap
        a2y -= gap
        a2x += gap
        #print('SHIFTED DOWN')
    if cy<0:
        gap = 0-cy
        dy += gap
        dx -= gap
        cy += gap
        cx -= gap
        a2y+= gap
        a2x-= gap
        #print('SHIFTED UP')
    while a2y >=dy:
        a2y -=1
        a2x +=1
    while a2x >= cx:
        a2y+=1
        a2x-=1
    

def parallelogram():
    canvas2.create_line(tkx(a2x),tky(a2y),tkx(cx),tky(cy),fill="green",width=3)
    canvas2.create_line(tkx(a2x),tky(a2y),tkx(dx),tky(dy),fill="green",width=3)
    global b2x,b2y
    b2x = dx + cx-a2x
    b2y = dy + cy-a2y
    canvas2.create_line(tkx(b2x),tky(b2y),tkx(dx),tky(dy),fill="green",width=3)
    canvas2.create_line(tkx(b2x),tky(b2y),tkx(cx),tky(cy),fill="green",width=3)


def arms():
    canvas2.create_line(tkx(bx),tky(by),tkx(bx-5),tky(by-5),fill="green",width=3)
    canvas2.create_line(tkx(ax),tky(ay),tkx(a2x),tky(a2y),fill="green",width=3)
    canvas2.create_line(tkx(ax),tky(ay),tkx(ax+5),tky(ay+5),fill="green",width=3)  
def b():
    canvas2.create_line(tkx(b2x),tky(b2y),tkx(bx),tky(by),fill="green",width=3)
def ridge():
    canvas2.create_line(tkx(0),tky(y),tkx(dx),tky(dy),fill="green",width=3)
    canvas2.create_line(tkx(x),tky(0),tkx(cx),tky(cy),fill="green",width=3)


#canvas2.mainloop()
def show_solution1():
    if y-flap2 >= flap1:
        print("no pytha necessary")
        pass
    overlap()
    if bx==ax:
        print("no pytha necessary")
        pass
    rotate()
    cd1()
    parallelogram()
    b()
    arms()
    ridge()

def next_solution():
    global solution,factor1,factor2
    if nicecombos!=[]:
        if len(nicecombos) == 1:
            print("only found one solution does not go off grid. This does not mean yours is wrong if you found one.")
        elif solution < len(nicecombos):
            factor1 = nicecombos[solution][1]
            factor2 = area/factor1
            solution += 1
        elif solution >= len(nicecombos):
            solution = 0
            factor1 = nicecombos[solution][1]
            factor2 = area/factor1
    else:
        if len(combos)==1:
            print("you got unlucky lmao")
        elif solution < len(combos):
            factor1 = combos[solution][1]
            factor2 = area/factor1
            solution += 1
        else:
            solution =0
            factor1 = combos[solution][1]
            factor2 = area/factor1
    canvas2.delete("all")
    canvas2.create_rectangle(0,00,600,600,fill="white",outline="white")

    draw_grid(x,y,grid)
    draw_circles(x,y,grid,flap1,flap2)
    draw_boxes(x,y,grid,flap1,flap2)
    draw_axis(x,y,grid)

    rotate()
    cd1()
    parallelogram()
    b()
    arms()
    ridge()
    
def hide_solution():
    canvas2.delete('all')
    canvas2.create_rectangle(0,00,600,600,fill="white",outline="white")
    draw_grid(x,y,grid)
    draw_circles(x,y,grid,flap1,flap2)
    draw_boxes(x,y,grid,flap1,flap2)
    draw_axis(x,y,grid)

enter = Button(canvas2,text="SHOW SOLUTION",command=show_solution1)
enter.place(x=400,y=180)
enter = Button(canvas2,text="next solution",command=next_solution)
enter.place(x=400,y=210)
enter = Button(canvas2,text="hide solution",command=hide_solution)
enter.place(x=400,y=240)


