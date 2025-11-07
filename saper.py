import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
CELL_SIZE = 40
MARGIN = 2
HEADER_HEIGHT = 60
FONT_SIZE = 20
MIN_FONT_SIZE = 16

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (120, 120, 120)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
DARK_RED = (128, 0, 0)
PURPLE = (128, 0, 128)
MAROON = (128, 0, 0)
TURQUOISE = (64, 224, 208)
DARK_GREEN = (0, 100, 0)
DARK_BLUE = (0, 0, 128)

COLORS = {
    '1': BLUE,
    '2': GREEN,
    '3': RED,
    '4': DARK_BLUE,
    '5': MAROON,
    '6': TURQUOISE,
    '7': BLACK,
    '8': DARK_GRAY
}

class Minesweeper:
    def __init__(self, width=10, height=10, mines=15):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = [[' ' for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flagged = [[False for _ in range(width)] for _ in range(height)]
        self.game_over = False
        self.win = False
        self.first_move = True
        self.mines_flagged = 0
        
        # Расчет размеров окна
        self.screen_width = width * (CELL_SIZE + MARGIN) + MARGIN
        self.screen_height = height * (CELL_SIZE + MARGIN) + MARGIN + HEADER_HEIGHT
        
        # Создание окна
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Сапер - убиваем время на паре")
        
        # Шрифты
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.min_font = pygame.font.Font(None, MIN_FONT_SIZE)
        
    def place_mines(self, first_x, first_y):
        safe_cells = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = first_x + dx, first_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    safe_cells.append((nx, ny))
        
        mines_placed = 0
        while mines_placed < self.mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in safe_cells and self.board[y][x] != 'X':
                self.board[y][x] = 'X'
                mines_placed += 1
        
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 'X':
                    count = self.count_adjacent_mines(x, y)
                    if count > 0:
                        self.board[y][x] = str(count)
    
    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.board[ny][nx] == 'X':
                        count += 1
        return count
    
    def reveal(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        
        if self.flagged[y][x] or self.revealed[y][x] or self.game_over or self.win:
            return
            
        if self.first_move:
            self.place_mines(x, y)
            self.first_move = False
            
        if self.board[y][x] == 'X':
            self.game_over = True
            return
            
        self.revealed[y][x] = True
        
        if self.board[y][x] == ' ':
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.width and 0 <= ny < self.height and 
                        not self.revealed[ny][nx] and not self.flagged[ny][nx]):
                        self.reveal(nx, ny)
        
        self.check_win()
    
    def toggle_flag(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height) or self.revealed[y][x] or self.game_over or self.win:
            return
        
        self.flagged[y][x] = not self.flagged[y][x]
        if self.flagged[y][x]:
            self.mines_flagged += 1
        else:
            self.mines_flagged -= 1
    
    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 'X' and not self.revealed[y][x]:
                    return False
        self.win = True
        return True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Рисуем заголовок с информацией
        mines_text = self.font.render(f"Мин: {self.mines - self.mines_flagged}", True, WHITE)
        status_text = self.font.render("Статус: ", True, WHITE)
        
        if self.game_over:
            status = self.font.render("ПОРАЖЕНИЕ!", True, RED)
        elif self.win:
            status = self.font.render("ПОБЕДА!", True, GREEN)
        else:
            status = self.font.render("Играем...", True, BLUE)
        
        self.screen.blit(mines_text, (10, 10))
        self.screen.blit(status_text, (self.screen_width // 2 - 50, 10))
        self.screen.blit(status, (self.screen_width // 2 + 20, 10))
        
        # Инструкция
        instruction = self.min_font.render("ЛКМ - открыть, ПКМ - флаг, R - перезапуск", True, GRAY)
        self.screen.blit(instruction, (10, HEADER_HEIGHT - 25))
        
        # Рисуем поле
        for row in range(self.height):
            for column in range(self.width):
                x = column * (CELL_SIZE + MARGIN) + MARGIN
                y = row * (CELL_SIZE + MARGIN) + MARGIN + HEADER_HEIGHT
                
                if self.revealed[row][column]:
                    # Открытая клетка
                    pygame.draw.rect(self.screen, WHITE, [x, y, CELL_SIZE, CELL_SIZE])
                    
                    if self.board[row][column] != ' ':
                        if self.board[row][column] == 'X':
                            # Мина
                            pygame.draw.circle(self.screen, RED, 
                                            [x + CELL_SIZE // 2, y + CELL_SIZE // 2], 
                                            CELL_SIZE // 3)
                        else:
                            # Число
                            number = self.board[row][column]
                            text = self.font.render(number, True, COLORS.get(number, BLACK))
                            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                            self.screen.blit(text, text_rect)
                
                else:
                    # Закрытая клетка
                    pygame.draw.rect(self.screen, DARK_GRAY, [x, y, CELL_SIZE, CELL_SIZE])
                    
                    if self.flagged[row][column]:
                        # Флаг
                        pygame.draw.polygon(self.screen, RED, [
                            (x + 10, y + 10),
                            (x + 30, y + 20),
                            (x + 10, y + 30)
                        ])
                        # Древко флага
                        pygame.draw.rect(self.screen, BLACK, [x + 8, y + 10, 4, 25])
        
        # Если игра окончена, показываем все мины
        if self.game_over:
            for row in range(self.height):
                for column in range(self.width):
                    if self.board[row][column] == 'X' and not self.flagged[row][column]:
                        x = column * (CELL_SIZE + MARGIN) + MARGIN
                        y = row * (CELL_SIZE + MARGIN) + MARGIN + HEADER_HEIGHT
                        pygame.draw.circle(self.screen, RED, 
                                        [x + CELL_SIZE // 2, y + CELL_SIZE // 2], 
                                        CELL_SIZE // 3)
    
    def get_cell_from_pos(self, pos):
        x, y = pos
        if y < HEADER_HEIGHT:
            return None, None
        
        column = (x - MARGIN) // (CELL_SIZE + MARGIN)
        row = (y - HEADER_HEIGHT - MARGIN) // (CELL_SIZE + MARGIN)
        
        if 0 <= row < self.height and 0 <= column < self.width:
            return column, row
        return None, None
    
    def restart(self):
        self.__init__(self.width, self.height, self.mines)

def main():
    game = Minesweeper(10, 10, 15)
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = game.get_cell_from_pos((x, y))
                
                if col is not None and row is not None:
                    if event.button == 1:  # ЛКМ
                        game.reveal(col, row)
                    elif event.button == 3:  # ПКМ
                        game.toggle_flag(col, row)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Перезапуск
                    game.restart()
                elif event.key == pygame.K_ESCAPE:  # Выход
                    pygame.quit()
                    sys.exit()
        
        game.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
