import turtle
import numpy as np
from time import sleep, time

# Screen class for screen setup
class Screen():
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
        self.border = Turtle()
        self.border.color("black")
        self.border.pensize(3)
        self.border.hideturtle()
        self.border.jump(-330, -330)
        self.border.square(660)

    
    def init_writer(self):
        self.writer = Turtle()
        self.writer.color("black")
        self.writer.hideturtle()
    
    def update_info(self, population):
        info_str = "Generation: {}  Best Fitness: {}".format(
            population.gen,
            population.fitness)
        self.writer.clear()
        self.writer.jump(-200, 250)
        self.writer.write(info_str)

# Base Turtle class
class Turtle(turtle.Turtle):
    def square(self, length):
        for _ in range(4):
            self.forward(length)
            self.left(90) 

    def jump(self, x, y):
        self.penup()
        self.goto(x, y)
        self.pendown()

# Candy graphic representation
class Candy(Turtle):
    def __init__(self, x:int = 0, y:int = 200):
        super().__init__()
        self.shape("square")
        self.shapesize(2,2)
        self.color("red")
        self.jump(x,y)
        self.limit = 20

# Obstacle graphic representation
class Obstacle(Turtle):
    def __init__(self, x:int,y:int):
        super().__init__()
        self.shape("circle")
        self.shapesize(2,2)
        self.color('black')
        self.jump(x,y)
        self.limit = 20

# Dot class groups functions essential to every dot
class Dot(Turtle):
    def __init__(self, steps: int = 50000):
        super(Dot, self).__init__()
        # graphics settings
        self.shape("circle")
        self.shapesize(0.2,0.2)
        self.color("black")
        # position setttings
        self.jump(0,-100)
        self.penup()
        self.setheading(90)
        # behavior settings
        self.speed(0)
        self.steering = np.random.randint(low=-90, high=90, size=steps)
        self.dead = False
        self.fitness = 0

    def move(self):
        self.forward(10)
        self.right(self.steering[self.fitness])
        self.fitness += 1

    def out_of_bounds(self):
        if self.xcor() < -330:
            return True
        if self.xcor() > 330:
            return True
        if self.ycor() < -330:
            return True
        if self.ycor() > 330:
            return True
        return False

# Population class groups dots in one place and updates them when needed
class Population(object):
    def __init__(self, size: int = 1000, lr : int = 20):
        super(Population, self).__init__()
        self.dots = [Dot() for _ in range(size)]
        self.size = size
        self.gen = 0
        self.fitness = float("inf")
        self.lr = lr / 100

    def update_gen(self, parent_dot: Dot):
        self.gen += 1
        # hide dots from pop.dots
        [d.hideturtle() for d in self.dots]
        # clear self.dots
        self.dots = []
        # init new list of dots
        self.fitness = parent_dot.fitness
        self.dots = [Dot() for _ in range(self.size)]
        # randomly shift steering for each dot
        for dot in self.dots:
            dot.steering = parent_dot.steering + np.random.randint(
                low=int(-10*(1-self.lr)**self.gen),
                high=int(10*(1-self.lr)**self.gen),
                size=parent_dot.steering.shape[0]
                )

distance = lambda dot, obj: np.sqrt([(dot.xcor()-obj.xcor())**2 + (dot.ycor()-obj.ycor())**2])

def main():
    screen = Screen()
    population = Population()
    initial_population = len(population.dots)
    candy = Candy()
    obstacles = [Obstacle(180,-70), Obstacle(-180,-70), Obstacle(0,70)]
    generation_finished = False
    deleted = 0

    while True:
        t0 = time()

        to_delete = set()
        for ix, dot in enumerate(population.dots):
            # move every dot and check if still in boudaries
            dot.move()
            if dot.out_of_bounds():
                dot.hideturtle()
                to_delete.add(ix)
                continue
            # check distance to the candy
            # if small enough break loop and re-init population
            if distance(dot, candy) < candy.limit:
                generation_finished = True
                break
                
            # check distance with every obstacles
            # if small enough dot is hidden and added to the delete list
            for obs in obstacles:
                if distance(dot, obs) < obs.limit:
                    dot.hideturtle()
                    to_delete.add(ix)
                    continue
        
        if generation_finished:
            print('Updating generation')
            population.update_gen(dot)
            generation_finished = False
            deleted = 0
        else:
            # delete all dots out of bounds or hit by obstacle
            prev_size = len(population.dots)
            
            population.dots = [dot for ix,dot in enumerate(population.dots) if ix not in to_delete]
            
            size = len(population.dots)
            deleted_now = prev_size - size
            deleted += deleted_now
            print("Deleted ", deleted, " dots")
        
        screen.update_info(population)
        screen.screen.update()
        if deleted == initial_population:
            del screen, population, initial_population
            del candy, obstacles, generation_finished
            del deleted
            main()
        t1 = time()

        exe_time = t1 - t0
        if 1/60 - exe_time > 0:
            sleep(1/60 - exe_time)


if __name__ == "__main__":
    main()