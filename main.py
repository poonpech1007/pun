import pygame
import random

# Constants
WIDTH = 600
HEIGHT = 700
GRID_SIZE = 8
CELL_SIZE = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Items (using letters for simplicity, can replace with images)
ITEMS = ['A', 'B', 'C', 'D', 'E', 'F']

class Game:
    def __init__(self):
        self.grid = [[random.choice(ITEMS) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected = None
        self.score = 0

    def draw(self, screen):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE + 100, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 1)
                font = pygame.font.Font(None, 36)
                text = font.render(self.grid[i][j], True, BLACK)
                screen.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 120))
        
        # Draw score
        font = pygame.font.Font(None, 48)
        text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(text, (10, 10))

    def handle_click(self, pos):
        x, y = pos
        if y < 100:
            return
        j = x // CELL_SIZE
        i = (y - 100) // CELL_SIZE
        if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE:
            if self.selected is None:
                self.selected = (i, j)
            else:
                si, sj = self.selected
                if abs(si - i) + abs(sj - j) == 1:  # Adjacent cells
                    # Swap
                    self.grid[si][sj], self.grid[i][j] = self.grid[i][j], self.grid[si][sj]
                    if self.check_matches():
                        self.score += 10
                        self.remove_matches()
                        self.drop()
                        self.fill()
                    else:
                        # Swap back if no match
                        self.grid[si][sj], self.grid[i][j] = self.grid[i][j], self.grid[si][sj]
                self.selected = None

    def check_matches(self):
        matches = set()
        # Check rows
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 2):
                if self.grid[i][j] == self.grid[i][j+1] == self.grid[i][j+2] != None:
                    matches.add((i, j))
                    matches.add((i, j+1))
                    matches.add((i, j+2))
        # Check columns
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE - 2):
                if self.grid[i][j] == self.grid[i+1][j] == self.grid[i+2][j] != None:
                    matches.add((i, j))
                    matches.add((i+1, j))
                    matches.add((i+2, j))
        return matches

    def remove_matches(self):
        matches = self.check_matches()
        for i, j in matches:
            self.grid[i][j] = None

    def drop(self):
        for j in range(GRID_SIZE):
            col = [self.grid[i][j] for i in range(GRID_SIZE) if self.grid[i][j] is not None]
            col += [None] * (GRID_SIZE - len(col))
            for i in range(GRID_SIZE):
                self.grid[i][j] = col[GRID_SIZE - 1 - i]  # Reverse to drop from bottom

    def fill(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] is None:
                    self.grid[i][j] = random.choice(ITEMS)

# Main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pun Game - Match 3 Puzzle")
    game = Game()
    running = True
    while running:
        screen.fill(BLACK)
        game.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()