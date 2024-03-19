import tkinter as tk
import random


class SnakeGame(tk.Tk):
    def __init__(self, width=400, height=400, block_size=20, speed=250):
        super().__init__()
        self.width = width
        self.height = height
        self.block_size = block_size
        self.speed = speed
        self.score = 0
        self.snake = [(width // 2, height // 2)]
        self.direction = "Right"
        self.food = self.create_food()
        self.running = False
        # self.game_over_text = None
        self.title("Snake")

        self.canvas = tk.Canvas(self, width=width, height=height, bg="black")
        self.canvas.pack()
        self.game_over_text = self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text="Press space to start",
            fill="white",
            font=("Helvetica", 24),
        )
        self.bind("<KeyPress>", self.change_direction)
        self.bind(
            "<space>", self.start_or_restart_game
        )  # Obsługa naciśnięcia klawisza spacji

        self.update_snake()

    def create_food(self):
        x = (
            random.randint(0, (self.width - self.block_size) // self.block_size)
            * self.block_size
        )
        y = (
            random.randint(0, (self.height - self.block_size) // self.block_size)
            * self.block_size
        )
        return x, y

    def update_snake(self):
        self.canvas.delete("snake", "food", "score")

        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x,
                y,
                x + self.block_size,
                y + self.block_size,
                fill="green",
                tags="snake",
            )

        self.canvas.create_rectangle(
            self.food[0],
            self.food[1],
            self.food[0] + self.block_size,
            self.food[1] + self.block_size,
            fill="red",
            tags="food",
        )

        self.canvas.create_text(
            self.width - 50, 10, text=f"Score: {self.score}", fill="white", tags="score"
        )

    def move_snake(self):
        head = self.snake[0]
        x, y = head

        if self.direction == "Left":
            x -= self.block_size
        elif self.direction == "Right":
            x += self.block_size
        elif self.direction == "Up":
            y -= self.block_size
        elif self.direction == "Down":
            y += self.block_size

        self.snake.insert(0, (x, y))

        if self.snake[0] == self.food:
            self.score += 1
            self.food = self.create_food()
        else:
            self.snake.pop()

        self.update_snake()

        if self.check_collision():
            self.game_over()
        elif self.running:
            self.after(self.speed, self.move_snake)

    def check_collision(self):
        head = self.snake[0]
        x, y = head

        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True

        if head in self.snake[1:]:
            return True

        return False

    def game_over(self):
        self.game_over_text = self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text="Game Over\nPress space to restart",
            fill="white",
            font=("Helvetica", 24),
        )
        self.running = False  # Ustawienie flagi running na False, gdy gra się kończy

    def start_or_restart_game(self, event):
        if not self.running:  # Rozpoczęcie gry tylko jeśli nie jest już uruchomiona
            self.canvas.delete(self.game_over_text)
            self.running = True
            self.snake = [
                (self.width // 2, self.height // 2)
            ]  # Resetowanie pozycji węża
            self.direction = "Right"  # Resetowanie kierunku węża
            self.score = 0  # Resetowanie wyniku
            self.food = self.create_food()  # Generowanie nowego jedzenia
            self.move_snake()  # Rozpoczęcie ruchu węża
            if self.game_over_text:  # Usunięcie tekstu "Game Over" po restarcie
                self.canvas.delete(self.game_over_text)

    def change_direction(self, event):
        new_direction = event.keysym

        if new_direction in ["Up", "Down", "Left", "Right"]:
            if (
                (new_direction == "Up" and self.direction != "Down")
                or (new_direction == "Down" and self.direction != "Up")
                or (new_direction == "Left" and self.direction != "Right")
                or (new_direction == "Right" and self.direction != "Left")
            ):
                self.direction = new_direction


if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()
