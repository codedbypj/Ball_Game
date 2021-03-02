import pygame
import os

pygame.init()
pygame.mixer.init()
pygame.font.init()

#fonts
WINNER_FONT = pygame.font.SysFont('consolas', 70)

#constants
FPS = 60
WIDTH, HEIGHT = 900, 500
LINE_WIDTH = 10
BALL_WIDTH, BALL_HEIGHT = 30, 30
PLAYER_VELOCITY = 10

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball-Game")
BALL = pygame.transform.scale(pygame.image.load(os.path.join('Assets','ball.png')), (BALL_WIDTH, BALL_HEIGHT))
BOUNCE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "bubble_pop.mp3"))

#User Events
WALL_BOUNCE = pygame.USEREVENT + 1
RED_BOUNCE = pygame.USEREVENT + 2
BLUE_BOUNCE = pygame.USEREVENT + 3

def draw(ball, player1, player2):
    WIN.fill(BLACK)
    WIN.blit(BALL, (ball.x, ball.y))
    pygame.draw.rect(WIN, RED, player1)
    pygame.draw.rect(WIN, BLUE, player2)
    # top line
    pygame.draw.rect(WIN, GREEN, [0,0,WIDTH,LINE_WIDTH])
    # bottom line
    pygame.draw.rect(WIN, YELLOW, [0,HEIGHT-10,WIDTH,LINE_WIDTH])
    # left line
    pygame.draw.rect(WIN, WHITE, [0,0,LINE_WIDTH, HEIGHT])
    # right line
    pygame.draw.rect(WIN, WHITE, [WIDTH-10,0,LINE_WIDTH, HEIGHT+LINE_WIDTH])    
    pygame.display.update()

def draw_winner(draw_text):
    text = WINNER_FONT.render(draw_text, 1, WHITE)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)
    

def player1_movement(player1, ball, keys_pressed):
    if keys_pressed[pygame.K_w] and player1.y > LINE_WIDTH:
        player1.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_s] and player1.y + player1.height + 10 < LINE_WIDTH + HEIGHT :
        player1.y += PLAYER_VELOCITY

def player2_movement(player2, ball, keys_pressed):
    if keys_pressed[pygame.K_UP] and player2.y > LINE_WIDTH:
        player2.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_DOWN] and player2.y + player2.height + 10 < LINE_WIDTH + HEIGHT:
        player2.y += PLAYER_VELOCITY

def ball_movement(ball, ball_dir, ball_velocity):
    dx, dy = ball_dir[0], ball_dir[1]
    ball.move_ip(dx * ball_velocity, dy * ball_velocity)
    if ball.y + ball.height >= HEIGHT - LINE_WIDTH or ball.y <= LINE_WIDTH:
        pygame.event.post(pygame.event.Event(WALL_BOUNCE))
    if ball.x <= LINE_WIDTH:
        pygame.event.post(pygame.event.Event(RED_BOUNCE))
    if ball.x + ball.width >= WIDTH - LINE_WIDTH:
        pygame.event.post(pygame.event.Event(BLUE_BOUNCE))
def main():
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_WIDTH, BALL_HEIGHT)
    ball_velocity = 8
    ball_acceleration = 1
    count, next = 0, 10
    ball_dir = [1,1]
    player1 = pygame.Rect(LINE_WIDTH, LINE_WIDTH + 20, 10, 80)
    player2 = pygame.Rect(WIDTH - LINE_WIDTH - 10, LINE_WIDTH + 20, 10, 80)
    run = True
    clock = pygame.time.Clock()
    while run:
        game_over = "None"
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == WALL_BOUNCE:
                ball_dir[1] = 0 - ball_dir[1]
            if event.type == RED_BOUNCE:
                count += 1
                if player1.colliderect(ball):
                    ball_dir[0] = 0 - ball_dir[0]
                    BOUNCE_SOUND.play()
                else:
                    #pygame.time.delay(2000)
                    game_over = "BLUE WINS!!!"
            if event.type == BLUE_BOUNCE:
                if player2.colliderect(ball):
                    ball_dir[0] = 0 - ball_dir[0]
                    BOUNCE_SOUND.play()
                else:
                    #pygame.time.delay(2000)
                    game_over = "RED WINS!!!"
        if game_over is not "None":
            run = False
            draw_winner(game_over)
            break
        if count >= count + next :
            prev = count
            ball_velocity += ball_acceleration
            ball_acceleration += 1
        keys_pressed = pygame.key.get_pressed()
        player1_movement(player1, ball, keys_pressed)
        player2_movement(player2, ball, keys_pressed)
        ball_movement(ball, ball_dir, ball_velocity)
        draw(ball, player1, player2)
        #move_ball(ball)
    main()
def rot_image(ball_temp):
    pass

if __name__ == '__main__':
    WIN.fill(WHITE)
    pygame.time.delay(1000)
    ball_temp = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'ball.png')),(WIDTH,HEIGHT))
    WIN.blit(ball_temp,(0,0))
    pygame.display.flip()
    pygame.time.delay(2000)
    rot_image(ball_temp)
    main()
        