import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1440, 780
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War")

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

BULLETS_VEL = 20
MAX_BULLETS = 3
GREEN = (124, 252, 0)
BLUE = (30, 144, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
VEL = 5

BLUE_HIT = pygame.USEREVENT + 1
GREEN_HIT = pygame.USEREVENT + 2


def blue_handle_movement(keys_press, blue):
    if keys_press[pygame.K_a] and blue.x - VEL > 0:  # Left
        blue.x -= VEL
    if keys_press[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x + 20:  # Right
        blue.x += VEL
    if keys_press[pygame.K_w] and blue.y - VEL > 0 - 5:  # Up
        blue.y -= VEL
    if keys_press[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT - 15:  # Down
        blue.y += VEL


def green_handle_movement(keys_press, green):
    if keys_press[pygame.K_LEFT] and green.x - VEL > BORDER.x + BORDER.width:  # Left
        green.x -= VEL
    if keys_press[pygame.K_RIGHT] and green.x + VEL + green.width < WIDTH + 20:  # Right
        green.x += VEL
    if keys_press[pygame.K_UP] and green.y - VEL > 0 - 5:  # Up
        green.y -= VEL
    if keys_press[pygame.K_DOWN] and green.y + VEL + green.height < HEIGHT - 15:  # Down
        green.y += VEL


def handle_bullets(blue_bullets, green_bullets, blue, green):
    for bullets in blue_bullets:
        bullets.x += BULLETS_VEL
        if green.colliderect(bullets):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            blue_bullets.remove(bullets)
        elif bullets.x > WIDTH:
            blue_bullets.remove(bullets)

    for bullets in green_bullets:
        bullets.x -= BULLETS_VEL
        if blue.colliderect(bullets):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            green_bullets.remove(bullets)
        elif bullets.x < 0:
            green_bullets.remove(bullets)


SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 80

Blue_SPACESHIP_IMAGE = pygame.image.load(os.path.join('playerShip1_blue.png'))
Blue_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    Blue_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

Green_SPACESHIP_IMAGE = pygame.image.load(os.path.join('playerShip1_green.png'))
Green_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    Green_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))


def draw_window(blue, green, blue_bullets, green_bullets, green_health, blue_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    green_health_text = HEALTH_FONT.render("Health: " + str(green_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, WHITE)
    WIN.blit(green_health_text, (WIDTH - green_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10, 10))

    WIN.blit(Green_SPACESHIP_IMAGE, (green.x, green.y))
    WIN.blit(Blue_SPACESHIP_IMAGE, (blue.x, blue.y))
    for bullets in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullets)
    for bullets in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullets)
    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    blue = pygame.Rect(190, 450, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    green = pygame.Rect(1200, 450, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    blue_bullets = []
    green_bullets = []

    green_health = 25
    blue_health = 25
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 - 2, 15, 10)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_SPACE and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x, green.y + green.height//2 - 2, 15, 10)
                    green_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == BLUE_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == GREEN_HIT:
                green_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if green_health <= 0:
            winner_text = "Blue Wins !"

        if blue_health <= 0:
            winner_text = "Green Wins !"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_press = pygame.key.get_pressed()
        blue_handle_movement(keys_press, blue)
        green_handle_movement(keys_press, green)

        handle_bullets(blue_bullets, green_bullets, blue, green)
        draw_window(blue, green, blue_bullets, green_bullets, green_health, blue_health)
    pygame.quit()
    pygame.display.update()


if __name__ == "__main__":
    main()
