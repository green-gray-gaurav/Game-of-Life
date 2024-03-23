
#--------------some useful classes to create a maker initlilizer---------------------
from classes.console_space import ConsoleSpace , ConsoleObject
import time , copy

#-----------default active cell represntation in the grid of 2d space-----------------------
CELL = 'O'


#---------------inheriting the console object whcih is controllable in console space---------------
class Ink(ConsoleObject):
    def __init__(self, label: str, pos) -> None:
        super().__init__(label, pos)
        self.counter = 1
        self.grid = None

    def update(self):
        pass
    def event(self, e):
        #getting the user input for navigating the marker--creating a cell--begin the simulation
        x , y = self.get_pos()
        if(e == b'w'):
            self.set_pos((x, y-1))
        if(e == b'a'):
            self.set_pos((x-1 , y))
        if(e == b's'):
            self.set_pos((x , y+1))
        if(e == b'd'):
            self.set_pos((x+1 , y))
        if(e == b'c'):
            #------------adding a cell object in the console space------------------------
            self.send_request("add" , [cell(self.counter , self.get_pos()).set_mask([CELL])])
            self.counter+=1
        if(e == b'b'):
            #-------------storing a grid created and exiting the console space----------
            self.send_request("getgrid" , [self.__trigger])
            self.send_request("terminate" , [])
           
        
    def __trigger(self , obj):
        self.grid = obj

#------------------this one is cell objct on console space-----------------------
class cell(ConsoleObject):
    def __init__(self, label: str, pos) -> None:
        super().__init__(label, pos)
          




#---------------------------------for maker to write-------------------------
space = ConsoleSpace()

#---------------------setting the maker to make the initial generation
w , h = space.get_dim()
inker = Ink( "new", (int(w/2) , int(h/2))).set_mask(
    [['x']],
)
#---------------------for displaying the maker realtime
space.add_console_object(inker)


#-----------------------adding some user realted info
print("---------------------------GAME OF LIFE------------------------")
print("""The Game of Life, It is a zero-player game,
meaning that its evolution is determined by
its initial state, requiring no further input.
One interacts with the Game of Life by creating 
an initial configuration and observing how it evolves.
       """)

print("------------how to setup initial confuguration---------------")

print("1 . use w,a,s,d keys to navigate a maker x")
print("2 . use c key to plant a cell at maker x position")
print("3 . use b key to begin the game of life")



print("-------------------------------------------------------------")


#-------------------------here is the user input


user = input("enter y to initilize game of life: ")
if(user=='y'):
    space.start_gameloop()
else:
    print("exiting the game of life")
    exit(0)


#-------------------------for printing each generation of cells on console----------------------
def print_cell_grid(grid):
    for xi in grid:
        for yi in xi:
            if(yi==CELL):
                print(yi, end="")
            else:print(space.space_dull_pixel  , end="")
        print()

#a utilty function to check 8 neighbours of the a cell to determine it state for next generation
def is_live(grid , x , y):
    try: 
        if grid[y][x] == CELL: return 1
        else: return 0
    except: return 0

#--------------------------to make a single iteration of generation----------------------------
def simpulate_game_of_life(grid):

    grid_changed = copy.deepcopy(grid)
    for yi in range(len(grid)):
        for xi in range(len(grid[0])):
            live_count = 0
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if(i==0 and j==0 ):pass
                    else :live_count += is_live(grid  , xi+i , yi+j)
           
            if(live_count < 2 or live_count > 3): grid_changed[yi][xi] = 0
            if(live_count == 3): grid_changed[yi][xi] = CELL
    
    del grid
    return grid_changed
            

#----------------simulatin the genration of cells -------------------------
while True:
    print_cell_grid(inker.grid)
    inker.grid = simpulate_game_of_life(inker.grid)
    time.sleep(0.1)
    pass