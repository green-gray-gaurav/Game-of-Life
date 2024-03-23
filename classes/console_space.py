
class ConsoleSpace():
    import msvcrt , os , sys , copy

    def __init__(self ,  width:int = 100 ,  height:int=30) -> None:
        #here we are creating the internal buffer of console space
        self.grid = [[0 for _ in range(width)] for __ in range(height) ]

        #this dict stores console object instances
        self.console_objects = {}

        self.space_dull_pixel = ' '
        self.space_lit_pixel = '.'
        pass
    def get_dim(self):
        return len(self.grid[0]) , len(self.grid)

        #this function used to add the console objects in console space
    def add_console_object(self ,console_obj):
        self.console_objects[console_obj.instance_name] = console_obj
        pass

    def start_gameloop(self):
        #here we start gameloop
        loop = True
        while loop:
            #----uesr input to get the keys----
            char = ConsoleSpace.msvcrt.getch()

            request_queue = []
            #updating the console objects -- and merging on grid
            for tag , console_obj  in self.console_objects.items():
                
                console_obj.event(char)
                console_obj.update()
                self.__merge_mask(console_obj)

                request_queue += console_obj.request_queue


            #displying the modified console space
            for yi in self.grid:
                for xi in yi:
                    if(xi==0):
                        print(self.space_dull_pixel , end="")
                    else:
                        print(xi , end="")
                print()

            #handling the console object requests
            while(len(request_queue) > 0):
                rq = request_queue.pop(0)
                rtype , data = rq
                if(rtype == "add"):
                    self.add_console_object(data[0])
                if(rtype == "getgrid"):
                    self.grid
                    data[0](ConsoleSpace.copy.deepcopy(self.grid))
                if(rtype == "terminate"):
                    loop = False



            #clearing the console space buffer
            
            for yi in range(len(self.grid)):
                for xi in range(len(self.grid[0])):
                    self.grid[yi][xi] = self.space_dull_pixel

    
    # to merge the console object on console space
    def __merge_mask(self , console_obj):
        sx , sy = console_obj.get_size()
        for i in range(sx):
            for j in range(sy):
                try :
                    self.grid[j + console_obj.y ][i + console_obj.x] = console_obj.mask[j][i]
                except:pass
    
    

        
        pass
            
# here is the definition of console object
class ConsoleObject():
    def __init__(self , label:str ,pos) -> None:
        self.instance_name = label
        self.mask = None
        self.x  , self .y = pos

        self.request_queue = []
        
        pass
    #to create the pattern for console object
    def set_mask(self , mask:list):
        self.mask = mask
        return self
    #set its position in conosole space
    def set_pos(self , pos:list):
        self.x , self.y = pos

    def get_size(self):
        return len(self.mask[0]) ,  len(self.mask)
    def get_pos(self):
        return self.x , self.y
    
    #these function can we over-ridden like we did in main.py file
    def event(self , e):pass
    def update(self):pass

    # to send reuest to console space
    def send_request(self , rtype ,request_data):
        self.request_queue.append([rtype , request_data])
        pass
    def get_request_queue(self):
        rq  = self.request_queue.copy()
        self.request_queue = []
        return rq


    
    
    

    
