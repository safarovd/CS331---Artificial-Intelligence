class State():
    prev_state = None
    def __init__(self, chickens, wolves, boat):
        self.left_chickens = chickens
        self.left_wolves = wolves
        self.right_chickens = 0
        self.right_wolves = 0
        self.left_boat = boat
        self.right_boat = 0 if boat else 1
        self.prev_state = None
    # setter functions for moving animals and boat
    def move_chicken_right(self, amount):
        self.left_chickens -= amount
        self.right_chickens += amount
    
    def move_chicken_left(self, amount):
        self.left_chickens += amount
        self.right_chickens -= amount

    def move_wolf_right(self, amount):
        self.left_wolves -= amount
        self.right_wolves += amount
    
    def move_wolf_left(self, amount):
        self.left_wolves += amount
        self.right_wolves -= amount
    
    def move_boat(self):
        temp = self.left_boat
        self.left_boat = self.right_boat
        self.right_boat = temp
    
    def save_parent_state(self, parent):
        self.prev_state = parent
    # getter functions for getting states in tuples and 2d lists
    def return_state_as_tuple(self):
        return (self.right_chickens,self.right_wolves,self.right_boat,self.left_chickens,self.left_wolves,self.left_boat)

    def return_state_as_lists(self):
        return [[self.right_chickens,self.right_wolves,self.right_boat],[self.left_chickens,self.left_wolves,self.left_boat]]