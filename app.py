import tkinter as tk
import random

# Constants
WIDTH = 600
HEIGHT = 400
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_SIZE = 15
BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = WIDTH // BRICK_COLUMNS
BRICK_HEIGHT = 20

class Breakout:
    def __init__(self, root):
        self.root = root
        self.root.title("Breakout - Tkinter Edition")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.running = True

        self.paddle = self.canvas.create_rectangle(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT, fill="white")
        self.canvas.move(self.paddle, (WIDTH - PADDLE_WIDTH) / 2, HEIGHT - 40)

        self.ball = self.canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill="red")
        self.canvas.move(self.ball, WIDTH / 2, HEIGHT / 2)

        self.ball_dx = random.choice([-3, 3])
        self.ball_dy = -3

        self.bricks = []
        self.create_bricks()

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        self.update()

    def create_bricks(self):
        colors = ["red", "orange", "yellow", "green", "blue"]
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLUMNS):
                x1 = col * BRICK_WIDTH
                y1 = row * BRICK_HEIGHT
                x2 = x1 + BRICK_WIDTH - 2
                y2 = y1 + BRICK_HEIGHT - 2
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[row % len(colors)], width=1)
                self.bricks.append(brick)

    def move_left(self, event):
        self.canvas.move(self.paddle, -20, 0)

    def move_right(self, event):
        self.canvas.move(self.paddle, 20, 0)

    def update(self):
        if not self.running:
            return

        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(self.paddle)

        # Bounce off walls
        if ball_coords[0] <= 0 or ball_coords[2] >= WIDTH:
            self.ball_dx = -self.ball_dx
        if ball_coords[1] <= 0:
            self.ball_dy = -self.ball_dy

        # Ball hits paddle
        if self.intersect(ball_coords, paddle_coords):
            self.ball_dy = -abs(self.ball_dy)

        # Ball falls below paddle
        if ball_coords[3] >= HEIGHT:
            self.game_over("Game Over")

        # Ball hits bricks
        for brick in self.bricks:
            if self.intersect(ball_coords, self.canvas.coords(brick)):
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.ball_dy = -self.ball_dy
                break

        # Win condition
        if not self.bricks:
            self.game_over("You Win!")

        self.root.after(16, self.update)  # ~60 FPS

    def intersect(self, a, b):
        return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])

    def game_over(self, message):
        self.running = False
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text=message, fill="white", font=("Arial", 24))

if __name__ == "__main__":
    root = tk.Tk()
    game = Breakout(root)
    root.mainloop()
