import pygame
import secrets
import os

RED = (255, 26, 26)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (153, 204, 255)
BACKGROUND_COLOR = (30, 30, 30)

WIDTH = 800
HEIGHT = 550
SCREEN_SIZE = WIDTH, HEIGHT
FPS = 120

pygame.init()
clock = pygame.time.Clock()    
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption("Pong Game")
pygame.mouse.set_visible(0)

class Audio:
    def __init__(self):
        self.hit_sound = pygame.mixer.Sound("sounds/hit.wav")
        self.wall_sound = pygame.mixer.Sound("sounds/click.wav")
        self.out_sound = pygame.mixer.Sound("sounds/out.wav")
        pygame.mixer.music.load("sounds/music.wav")

    def play_music(self):
        pygame.mixer.music.play(-1)
    def stop_music(self):
        pygame.mixer.music.stop()

    def hit(self):
        pygame.mixer.Sound.play(self.hit_sound)
    def wall(self):
        pygame.mixer.Sound.play(self.wall_sound)
    def out(self):
        pygame.mixer.Sound.play(self.out_sound)

class Score:
    def __init__(self):
        self.score = 0
        self.high_score = 0

    def inc(self):
        self.score +=1
        self.high_score = max(self.score, self.high_score)

    def display(self, x, y):
        font = pygame.font.SysFont("monospace", 20, 1)
        textScore = font.render(f"Score: {str(self.score)}", 10, WHITE)
        textHighScore = font.render(f"High Score: {str(self.high_score)}", 1, WHITE)
    
        screen.blit(textScore, (x - 55, y))
        screen.blit(textHighScore, (x - 55, y+20))

    def reset(self):
        self.score=0
        
class Pad:
    def __init__(self, posx, posy, width, height, speed=1):
        self.posx, self.posy, self.width, self.height = posx, posy, width, height
        self.rect = pygame.Rect(posx, posy, width, height)
        self.speed = speed
        self.color = WHITE
    
    def getRect(self):
        return self.rect

    def display(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, dist):
        self.posy += dist*self.speed

        if self.posy <= 0:
            self.posy = 0
        if self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height
            
        self.rect = (self.posx, self.posy, self.width, self.height)

class Ball:
    def __init__(self, posx, posy, radius, speed):
        self.posx, self.posy, self.radius = posx, posy, radius
        self.speed, self.color = speed, WHITE
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
        self.xdir = -1
        self.ydir = 1

    def display(self):
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.xdir * self.speed
        self.posy += self.ydir * self.speed

        if self.posx-self.radius <= 0 or self.posx+self.radius >= WIDTH :
            self.reset()
            return "outOnX"
        if self.posy-self.radius <= 0 or self.posy+self.radius >= HEIGHT :
            self.ydir *= -1
            return "outOnY"
        return "updated"

    def reset(self):
        self.posx, self.posy = WIDTH/2, HEIGHT/2
        self.xdir, self.ydir = secrets.choice([-1, 1]), secrets.choice([-1, 1])

    def getRect(self):
        return self.ball

class Game:
    def __init__(self):
        self.audio_manager = Audio()

        self.player1 = Pad(10, HEIGHT/2-100, 10, 100, 5)
        self.player2 = Pad(WIDTH-20, HEIGHT/2-100, 10, 100, 5)
        self.ball = Ball(WIDTH/2, HEIGHT/2, 10, 2.5)
        self.score = Score()
    
    def updateFrame(self):
        screen.fill(BACKGROUND_COLOR)
        self.player1.display()
        self.player2.display()
        self.ball.display()
        self.score.display(WIDTH/2-20, 10)

    def run(self):
        p1y, p2y = 0, 0
        p1_up, p1_down = False, False 
        p2_up, p2_down = False, False
        
        self.audio_manager.play_music()

        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == "escape":
                        exit = True
                    if event.key == pygame.K_UP:
                        p2_up = True
                        p2y = -1
                    if event.key == pygame.K_DOWN:
                        p2_down = True
                        p2y = 1
                    if event.key == pygame.K_w:
                        p1_up = True
                        p1y = -1
                    if event.key == pygame.K_s:
                        p1_down = True
                        p1y = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        p2_up = False
                    if event.key == pygame.K_DOWN:
                        p2_down = False
                    if event.key == pygame.K_w:
                        p1_up = False
                    if event.key == pygame.K_s:
                        p1_down = False

            if pygame.Rect.colliderect(self.ball.getRect(), self.player1.getRect()) :
                    if self.ball.posx - self.ball.radius <= self.player1.posx + 5:
                        self.ball.posx +=15
                        print("Da")
                    self.ball.xdir = 1
                    self.score.inc()
                    self.audio_manager.hit()

            if pygame.Rect.colliderect(self.ball.getRect(), self.player2.getRect()) :
                    if self.ball.posx + self.ball.radius >= self.player2.posx + 5:
                        self.ball.posx -=15
                        print("Da")
                    self.ball.xdir = -1
                    self.score.inc()
                    self.audio_manager.hit()
            
            if p1_down == True or p1_up == True:
                self.player1.update(p1y)
            if p2_down or p2_up:
                self.player2.update(p2y)
            ball_state = self.ball.update()
            
            
            if ball_state == "outOnX":
                self.audio_manager.out()
                self.score.reset()
            if ball_state == "outOnY":
                self.audio_manager.wall()

            self.updateFrame()
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    g = Game()
    g.run()