import turtle


class Screen:
    """Screen object for turtle library setup
    """

    def __init__(self):
        self.init_screen()
        self.init_border()
        self.init_writer()

    def init_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=660, height=660, startx=630, starty=0)
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

    def update_info(self, population, deleted):
        info_str = "Generation: {}  Best Fitness: {} Dead dots: {}".format(
            population.gen, population.fitness, deleted
        )
        self.writer.clear()
        self.writer.jump(-200, 250)
        self.writer.write(info_str)


class Turtle(turtle.Turtle):
    """Base Class for moving objects on the screen
    
    Arguments:
        turtle {[type]} -- [description]
    """

    def square(self, length):
        for _ in range(4):
            self.forward(length)
            self.left(90)

    def jump(self, x, y):
        self.penup()
        self.goto(x, y)
        self.pendown()


class Candy(Turtle):
    """Represents the goal of the program
    
    Arguments:
        Turtle {turtle} -- detectable object on the screen
    """

    def __init__(self, x: int = 0, y: int = 200):
        """Instantiates the object
        
        Keyword Arguments:
            x {int} -- x axis position (default: {0})
            y {int} -- y axis position(default: {200})
        """
        super().__init__()
        self.shape("square")
        self.shapesize(2, 2)
        self.color("red")
        self.jump(x, y)
        self.limit = 20


class Obstacle(Turtle):
    def __init__(self, x: int, y: int):
        """Creates an obstacle object
        
        Arguments:
            Turtle {Turtle} -- Graphic agent
            x {int} -- x axis position
            y {int} -- y axis position
        """
        super().__init__()
        self.shape("circle")
        self.shapesize(5, 5)
        self.color("black")
        self.jump(x, y)
        self.limit = 50
