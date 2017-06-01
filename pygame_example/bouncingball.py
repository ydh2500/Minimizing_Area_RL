from tkinter import *

class Box:
    def __init__(self, size):
        self.size = size
        
    def in_horizontal_contact(self, x):
        return x <= 0 or x >= self.size
        
    def in_vertical_contact(self, y):
        return y <= 0 or y >= self.size

    def in_square_contact_x(self, x, y, gap):
        return gap*(-1) <= ((self.size // 2)-x) <= gap and abs((self.size // 2)-y) == gap
    def in_square_contact_y(self, x, y, gap):
        return gap*(-1) <= ((self.size // 2)-y) <= gap and abs((self.size // 2)-x) == gap
class MovingBall:
    def __init__(self, x, y, xv, yv, color, size, box):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.color = color
        self.size = size
        self.box = box
        
    def move(self, time_unit, gap):
        self.x = self.x + self.xv * time_unit
        self.y = self.y + self.yv * time_unit
        if self.box.in_horizontal_contact(self.x):
            self.xv = - self.xv
        elif self.box.in_vertical_contact(self.y):
            self.yv = - self.yv
        elif self.box.in_square_contact_x(self.x, self.y, gap) :
            self.yv *= -1
        elif self.box.in_square_contact_y(self.x, self.y, gap):
            self.xv *= -1

            
class AnimationWriter:
    def __init__(self, root, ball, ball2, box):
        self.size = box.size
        self.canvas = Canvas(root, width=self.size, height=self.size)
        self.canvas.grid()
        self.ball = ball
        self.ball2 = ball2
            
    def animate(self):
        gap = self.ball.size
        e = self.size // 2
        self.canvas.delete(ALL)
        self.ball.move(1, gap)
        x = self.ball.x
        y = self.ball.y
        s = self.ball.size * 2
        c = self.ball.color
        e = self.size // 2
        self.canvas.create_oval(x, y, x+s , y+s, outline=c, fill=c)
        self.ball2.move(1, gap)
        x2 = self.ball2.x
        y2 = self.ball2.y
        s2 = self.ball2.size * 2
        c2 = self.ball2.color
        self.canvas.create_oval(x2, y2, x2+s2 , y2+s2, outline=c2, fill=c2)
        if (x-x2)**2 + (y-y2)**2 < (gap*2)**2:
            self.ball.xv *= -1
            self.ball.yv *= -1
            self.ball2.xv *= -1
            self.ball2.yv *= -1
        self.canvas.create_rectangle(e+gap, e+gap, e-gap, e-gap, outline="blue", fill="blue")
        self.canvas.after(10, self.animate)
        
class BounceController:
    def __init__(self):
        box_size = 400
        ball_size = 10
        ball_color_red = 'red'
        ball_color_green = 'green'
        x_velocity, y_velocity = 5, 2
        self.root = Tk()
        self.root.title("Bouncing Ball")
        self.root.geometry(str(box_size+10)+"x"+str(box_size+10))
        self.box = Box(box_size)
        self.ball = MovingBall(box_size//5, box_size//5, x_velocity, y_velocity, ball_color_red, ball_size, self.box)
        self.ball2 = MovingBall(box_size//3, box_size//3, x_velocity, y_velocity, ball_color_green, ball_size, self.box)

    def play(self):    
        AnimationWriter(self.root, self.ball, self.ball2, self.box).animate()
        self.root.mainloop()

    
A= BounceController()
A.play()


