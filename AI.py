import turtle
from random import choice, choices, randint
from time import sleep, time

class MyScreen():
    def __init__(self):
        self.init_screen()
        self.init_border()
        self.init_writer()

    def init_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(
            width=660,
            height=660,
            startx=630,
            starty=0
        )
        self.screen.tracer(0)
        self.screen.bgcolor("white")
        self.screen.title("Get Candy")


    def init_border(self):
        self.border = MyTurtle()
        self.border.color("black")
        self.border.pensize(3)
        self.border.hideturtle()
        self.border.jump(-330, -330)
        self.border.square(660)

    
    def init_writer(self):
        self.writer = MyTurtle()
        self.writer.color("black")
        self.writer.hideturtle()
    
    def update_info(self):
        info_str = "Generation: {}  Best Fitness: {}".format(
            my_population.gen_number,
            min(my_population.winner_fitness, default="Infinite")
        )
        self.writer.clear()
        self.writer.jump(-200, 250)
        self.writer.write(info_str)

class MyTurtle(turtle.Turtle):
    def square(self, length):
        for _ in range(4):
            self.forward(length)
            self.left(90) 

    def jump(self, x, y):
        self.penup()
        self.goto(x, y)
        self.pendown()

class Candy(MyTurtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(2,2)
        self.color("red")
        self.jump(0,200)
        self.limit = 20

class Population(MyTurtle):
    myDots = []
    parents = []
    generation = "alive"
    found_list = []
    winner = None
    winner_fitness = []
    parent_fitness = {}
    new_brain_moves = []
    gen_number = 0
    def verif(self):
        for dot in self.myDots:
            if dot.found == True: 
                self.found_list.append(dot)
                if dot in self.myDots:
                    self.myDots.remove(dot)
        if len(self.myDots)==0:
            self.generation = "over"
        else:
            self.generation = "alive" 

    def chose_winner(self):
        for dot in self.found_list:
            self.parents.append(dot)
            dot.hideturtle()
        for dot in self.parents:
            self.parent_fitness[dot] = dot.fitness
        self.winner = min(self.parent_fitness, default=0,key=self.parent_fitness.get)
        self.winner_fitness.append(self.winner.fitness)
        self.found_list = []
        self.parent_fitness = {}
        self.parents = []

    def clone(self):
        self.new_brain_moves  = []
        for move in self.winner.brain.moves:
            my_move = [0,0]
            my_move[0] = move[0] + randint(-1,1)
            my_move[1] = move[1] + randint(-1,1)
            self.new_brain_moves.append(my_move)
    
    def update(self):
        self.verif()
        if self.generation == "over":
            self.chose_winner()
            self.gen_number +=1
            for i in range(100):
                self.clone()
                Dot().brain.moves = self.new_brain_moves
                
class Dot(MyTurtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(0.2,0.2)
        self.color("black")
        self.jump(0,-200)
        self.penup()
        self.brain = Behavior(4000)
        self.going = [0,0]
        self.count = 0
        self.dead = False
        self.found = False
        self.fitness = 0
        my_population.myDots.append(self)

    def move(self):
        self.going = self.brain.moves[self.count]
        self.forward(self.going[0])
        self.right(self.going[1])
        self.fitness += self.going[0]
        self.count +=1

    def bounds(self):
        if self.xcor() < -330:
            self.dead = True
        if self.xcor() > 330:
            self.dead = True
        if self.ycor() < -330:
            self.dead = True
        if self.ycor() > 330:
            self.dead = True

    def destroy(self):
        my_population.myDots.remove(self)
        self.hideturtle()

    def find(self):
        if self.xcor() < my_candy.xcor() + my_candy.limit and self.xcor() > my_candy.xcor() - my_candy.limit and self.ycor() < my_candy.ycor() + my_candy.limit and self.ycor() > my_candy.ycor() - my_candy.limit:
            self.found = True
            self.color("green")

    def verif(self):
        self.bounds()
        self.find()
        if self.dead == True:
            self.destroy()

    def update(self):
        self.verif()
        if self.found != True:
            self.move()
               
class Behavior():
    frwrd_freedom = 15
    turn_freedom = 45
    def __init__(self, decisions):
        self.moves = []
        self.decisions = decisions
        self.randomize()

    def randomize(self):
        for i in range(self.decisions):
            self.moves.append([randint(10, self.frwrd_freedom), randint(-self.turn_freedom, Behavior.turn_freedom)])



my_screen = MyScreen()
my_population = Population()
my_population.hideturtle()
my_candy = Candy()
for i in range(100):
    Dot()

while True:
    t0 = time()

    for dot in my_population.myDots:
        dot.update()

    my_population.update()

    my_screen.update_info()
    my_screen.screen.update()
    t1 = time()

    exe_time = t1 - t0
    if 1/60 - exe_time > 0:
        sleep(1/60 - exe_time)