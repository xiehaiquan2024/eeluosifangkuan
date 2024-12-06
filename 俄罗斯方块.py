import pygame
import random

# 初始化 Pygame
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# 游戏设置
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# 方块形状定义
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        
    def new_piece(self):
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        x = GRID_WIDTH // 2 - len(shape[0]) // 2
        y = 0
        return {'shape': shape, 'x': x, 'y': y, 'color': color}
    
    def valid_move(self, piece, x, y):
        for i in range(len(piece['shape'])):
            for j in range(len(piece['shape'][0])):
                if piece['shape'][i][j]:
                    if (x + j < 0 or x + j >= GRID_WIDTH or
                        y + i >= GRID_HEIGHT or
                        (y + i >= 0 and self.grid[y + i][x + j])):
                        return False
        return True
    
    def merge_piece(self):
        for i in range(len(self.current_piece['shape'])):
            for j in range(len(self.current_piece['shape'][0])):
                if self.current_piece['shape'][i][j]:
                    self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = self.current_piece['color']
    
    def clear_lines(self):
        lines_cleared = 0
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        self.score += lines_cleared * 100
    
    def rotate_piece(self):
        shape = self.current_piece['shape']
        rotated = [[shape[j][i] for j in range(len(shape)-1, -1, -1)]
                  for i in range(len(shape[0]))]
        if self.valid_move({'shape': rotated,
                           'x': self.current_piece['x'],
                           'y': self.current_piece['y']},
                          self.current_piece['x'],
                          self.current_piece['y']):
            self.current_piece['shape'] = rotated
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # 绘制网格
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(self.screen,
                               WHITE,
                               [j * BLOCK_SIZE,
                                i * BLOCK_SIZE,
                                BLOCK_SIZE,
                                BLOCK_SIZE],
                               1)
                if self.grid[i][j]:
                    pygame.draw.rect(self.screen,
                                   self.grid[i][j],
                                   [j * BLOCK_SIZE,
                                    i * BLOCK_SIZE,
                                    BLOCK_SIZE,
                                    BLOCK_SIZE])
        
        # 绘制当前方块
        if self.current_piece:
            for i in range(len(self.current_piece['shape'])):
                for j in range(len(self.current_piece['shape'][0])):
                    if self.current_piece['shape'][i][j]:
                        pygame.draw.rect(self.screen,
                                       self.current_piece['color'],
                                       [(self.current_piece['x'] + j) * BLOCK_SIZE,
                                        (self.current_piece['y'] + i) * BLOCK_SIZE,
                                        BLOCK_SIZE,
                                        BLOCK_SIZE])
        
        # 绘制分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'分数: {self.score}', True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 10))
        
        pygame.display.flip()
    
    def run(self):
        fall_time = 0
        fall_speed = 500  # 下落速度（毫秒）
        
        while not self.game_over:
            fall_time += self.clock.get_rawtime()
            self.clock.tick()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece,
                                         self.current_piece['x'] - 1,
                                         self.current_piece['y']):
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece,
                                         self.current_piece['x'] + 1,
                                         self.current_piece['y']):
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece,
                                         self.current_piece['x'],
                                         self.current_piece['y'] + 1):
                            self.current_piece['y'] += 1
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
            
            if fall_time >= fall_speed:
                if self.valid_move(self.current_piece,
                                 self.current_piece['x'],
                                 self.current_piece['y'] + 1):
                    self.current_piece['y'] += 1
                else:
                    self.merge_piece()
                    self.clear_lines()
                    self.current_piece = self.new_piece()
                    if not self.valid_move(self.current_piece,
                                         self.current_piece['x'],
                                         self.current_piece['y']):
                        self.game_over = True
                fall_time = 0
            
            self.draw()
        
        # 游戏结束显示
        font = pygame.font.Font(None, 48)
        game_over_text = font.render('游戏结束!', True, WHITE)
        self.screen.blit(game_over_text,
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                         SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
    
    def create_block(self):
        """创建新的方块"""
        shapes = [
            [(0,0), (0,1), (1,0), (1,1)],  # 方块
            [(0,0), (0,1), (0,2), (0,3)],  # 长条
            [(0,0), (0,1), (0,2), (1,1)],  # T形
            [(0,0), (0,1), (1,1), (1,2)],  # Z形
            [(0,1), (0,2), (1,0), (1,1)],  # 反Z形
            [(0,0), (1,0), (1,1), (1,2)],  # L形
            [(0,2), (1,0), (1,1), (1,2)]   # 反L形
        ]
        
        # 随机选择一个形状
        self.current_shape = random.choice(shapes)
        # 设置方块的初始位置（通常在顶部中间）
        self.current_pos = [0, self.width // 2 - 1]
        
        # 检查新方块是否可以放置，如果不能则游戏结束
        if not self.is_valid_move(self.current_pos[0], self.current_pos[1]):
            return False
        return True
    
    def is_valid_move(self, row, col):
        """检查移动是否有效"""
        for block_row, block_col in self.current_shape:
            new_row = row + block_row
            new_col = col + block_col
            
            if new_row >= self.height or \
               new_col < 0 or \
               new_col >= self.width or \
               (new_row >= 0 and self.board[new_row][new_col]):
                return False
        return True

if __name__ == '__main__':
    game = Tetris()
    game.run()
    pygame.quit()
