import turtle
import numpy as np
from time import sleep, time
from base import Screen, Turtle, Candy, Obstacle

# Dot class groups functions essential to every dot
class Dot(Turtle):
    def __init__(self, steps: int = 50000):
        super(Dot, self).__init__()
        # graphics settings
        self.shape("circle")
        self.shapesize(0.2, 0.2)
        self.color("black")
        # position setttings
        self.jump(0, -100)
        self.penup()
        self.setheading(90)
        # behavior settings
        self.speed(0)
        self.steering = np.random.randint(low=-90, high=90, size=steps)
        self.dead = False
        self.fitness = 0

    def move(self) -> None:
        self.forward(10)
        self.right(self.steering[self.fitness])
        self.fitness += 1

    def out_of_bounds(self) -> bool:
        if self.xcor() < -330:
            return True
        if self.xcor() > 330:
            return True
        if self.ycor() < -330:
            return True
        if self.ycor() > 330:
            return True
        return False


class Population(object):
    def __init__(self, size: int = 1000, lr: int = 20):
        """Groups the dots and update the generation
    
        Arguments:
            size {int} -- number of dots to spawn
            lr {int} -- percentage by which to decrease the freedom of change in steering
        """
        super(Population, self).__init__()
        self.dots = [Dot() for _ in range(size)]
        self.size = size
        self.gen = 0
        self.fitness = float("inf")
        self.lr = lr / 100

    def update_gen(self, parent_dot: Dot) -> None:
        """Erases all current dots and spanws new ones based on winner dot
        
        Arguments:
            parent_dot {Dot} -- Base dot from which to copy the steering
        """
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
                low=int(-50 * (1 - self.lr) ** self.gen),
                high=int(50 * (1 - self.lr) ** self.gen),
                size=parent_dot.steering.shape[0],
            )


distance = lambda dot, obj: np.sqrt(
    [(dot.xcor() - obj.xcor()) ** 2 + (dot.ycor() - obj.ycor()) ** 2]
)


def game_loop():
    screen = Screen()
    population = Population()
    initial_population = len(population.dots)
    candy = Candy()
    obstacles = [
        Obstacle(*np.random.randint(low=-320, high=320, size=2)) for _ in range(3)
    ]
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
            population.update_gen(dot)
            generation_finished = False
            deleted = 0
        else:
            # delete all dots out of bounds or hit by obstacle
            prev_size = len(population.dots)

            population.dots = [
                dot for ix, dot in enumerate(population.dots) if ix not in to_delete
            ]

            size = len(population.dots)
            deleted_now = prev_size - size
            deleted += deleted_now

        screen.update_info(population, deleted)
        screen.screen.update()

        t1 = time()

        exe_time = t1 - t0
        if 1 / 60 - exe_time > 0:
            sleep(1 / 60 - exe_time)

        if deleted == initial_population:
            return None


if __name__ == "__main__":
    while True:
        game_loop()
