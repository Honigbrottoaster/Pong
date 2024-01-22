import pygame 
import sys

class Ball:
    def __init__(self, game):
        self.x_input = 1
        self.y_input = 1
        self.speed = 6
        self.rect = pygame.Rect(game.SCREEN_WIDTH / 2 - 15, game.SCREEN_HEIGHT / 2 - 15, 30, 30)

    def draw(self):
        pygame.draw.ellipse(game.screen, "red", self.rect)

    def move(self):
        if self.rect.y >= game.SCREEN_HEIGHT - 30 or self.rect.y <= 0:
            self.y_input *= -1
        
        if self.rect.x >= game.SCREEN_WIDTH - 30 or self.rect.x <= 0:
            self.x_input *= -1

        if self.rect.colliderect(game.player.rect):
            self.x_input *= -1
            game.score += 1

        if self.rect.colliderect(game.opponent.rect):
            self.x_input *= -1

        self.rect.x += self.x_input * self.speed
        self.rect.y += self.y_input * self.speed

class Opponent:
    def __init__(self, game):
        self.target_y = 0
        self.width = 20
        self.height = 100 
        self.speed = 6
        self.rect = pygame.Rect(game.SCREEN_WIDTH - 40, game.SCREEN_HEIGHT / 2 - self.height / 2, self.width, self.height)

    def draw(self):
        pygame.draw.rect(game.screen, "white", self.rect)

    def move(self, ball):
        self.target_y = ball.rect.y
        
        if self.target_y >= self.rect.y + self.height / 2 and self.rect.y < game.SCREEN_HEIGHT - self.height:
            self.rect.y += self.speed
        else:
            if self.rect.y > 0:
                self.rect.y -= self.speed

class Player:
    def __init__(self, game):
        self.width = 20
        self.height = 100 
        self.speed =7
        self.rect = pygame.Rect(20, game.SCREEN_HEIGHT / 2 - self.height / 2, self.width, self.height)
    
    def draw(self):
        pygame.draw.rect(game.screen, "white", self.rect)

    def move(self, direction):
        if direction == "UP" and self.rect.y >= 0:
            self.rect.y -= self.speed
        elif direction == "DOWN" and self.rect.y <= game.SCREEN_HEIGHT - self.height:
            self.rect.y += self.speed
        elif direction == "NONE":
            self.rect.y += 0

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 520
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pong")
        self.icon = pygame.image.load("img\icon.png").convert_alpha()
        pygame.display.set_icon(self.icon)
        self.score = 0

        #ball
        self.ball = Ball(self)

        #player
        self.player = Player(self)
        self.p_dir = "NONE"

        #opponent
        self.opponent = Opponent(self)

    def run(self):
        self.handleEvents()
        self.draw()
        self.update()

    def handleEvents(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.p_dir = "UP"
                elif event.key == pygame.K_DOWN:
                    self.p_dir = "DOWN"
            self.keys = pygame.key.get_pressed()
            if not any(self.keys):
                self.p_dir = "NONE"

    def draw(self):
        self.screen.fill((0, 0, 0))
    
        #ball
        self.ball.draw()

        #player
        self.player.draw()

        #opponent 
        self.opponent.draw()

        #score
        self.draw_score()

    def update(self):
        #ball
        self.ball.move()
        
        #player
        self.player.move(self.p_dir)

        #opponent
        self.opponent.move(self.ball)

        pygame.display.flip()
        self.clock.tick(80)

    def draw_score(self):
        font = pygame.font.Font(None, 50)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

if __name__ == "__main__":
    game = Game()
    while True:
        game.run()