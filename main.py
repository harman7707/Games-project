import pygame
import os
pygame.font.init()
pygame.mixer.init()



width, height = 900, 500
win=pygame.display.set_mode((width, height))
pygame.display.set_caption("HELLO!! THIS IS MY SPACE INVADERS GAME")

white =(255, 255, 255)
black =(0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 200, 0)


border = pygame.Rect(width//2 - 5, 0, 10, height )
bullet_hit_sound = (pygame.mixer.Sound(os.path.join('Assets','bulletcollide.mp3')))
bullet_fire_sound = (pygame.mixer.Sound(os.path.join('Assets','bulletfire.mp3')))

health_font = pygame.font.SysFont('comicsans', 40)
winner_font = pygame.font.SysFont('denmark', 100)
 

fps = 60
vel=5
bullet_vel=8
max_bullets=3

yellow_hit = pygame.USEREVENT + 1
red_hit =pygame.USEREVENT + 2

yellow_spaceship_image= pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image, (60, 45)), 90)
red_spaceship_image= pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
red_spaceship= pygame.transform.rotate(pygame.transform.scale(red_spaceship_image, (60, 45)),270)
space = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (900, 500))


def draw_window(red, yellow, red_bullets, yellow_bullets , red_health, yellow_health):
    win.blit(space, (0,0))
    pygame.draw.rect(win, black, border)

    red_health_text = health_font.render("Health: "+ str(red_health), 1, white)
    yellow_health_text = health_font.render("Health: "+ str(yellow_health), 1, white)
    win.blit(red_health_text,(width - red_health_text.get_width() - 10, 10))
    win.blit(yellow_health_text, (10, 10))

    win.blit(yellow_spaceship,(yellow.x, yellow.y))
    win.blit(red_spaceship,(red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(win, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(win, YELLOW, bullet)
    
    
    pygame.display.update()



def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - vel > 0: #LEFT 
        yellow.x -= vel
    if keys_pressed[pygame.K_d] and yellow.x + vel + yellow.width < border.x: #RIGHT 
        yellow.x += vel
    if keys_pressed[pygame.K_w] and yellow.y - vel > 0: #UP 
        yellow.y -= vel
    if keys_pressed[pygame.K_s] and yellow.y + vel + yellow.height < height - 15: #DOWN 
        yellow.y += vel

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - vel > border.x + border.width: #LEFT 
        red.x -= vel
    if keys_pressed[pygame.K_RIGHT] and red.x + vel + red.width < width: #RIGHT 
        red.x += vel
    if keys_pressed[pygame.K_UP] and red.y - vel > 0: #UP 
        red.y -= vel
    if keys_pressed[pygame.K_DOWN] and red.y + vel + red.height < height - 15: #DOWN 
        red.y += vel

def handle_bullets(yellow_bullets, red_bullets, yellow, red):

    for bullet in yellow_bullets:
        bullet.x +=  bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > width:
            yellow_bullets.remove(bullet)


    
    for bullet in red_bullets:
        bullet.x -=  bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)




def draw_winner(text):
    draw_text = winner_font.render(text, 1, white)
    win.blit(draw_text, (width/2 - draw_text.get_width()/2 , height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, 60, 45)
    yellow = pygame.Rect(100, 300, 60, 45)

    red_bullets = []
    yellow_bullets = []


    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True 
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()
                    

                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()

            if event.type == red_hit:
                red_health -= 2
                bullet_hit_sound.play()

            if event.type == yellow_hit:
                yellow_health -= 2
                bullet_hit_sound.play()

        winner_text= ""

        if red_health <=0:
            winner_text= "YELLOW WINS!"


        if yellow_health <=0:
            winner_text= "RED WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        
        keys_pressed= pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)


        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()

if __name__ == "__main__":
    main()