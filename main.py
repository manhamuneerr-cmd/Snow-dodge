import time
import random
import asyncio
import pygame

pygame.init()
hit = False
pygame.font.init()#initialize font module for us

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snow Dodge")

BG = pygame.transform.scale(pygame.image.load("snowimage.jpg"),(WIDTH, HEIGHT))
PLAYER_WIDTH =30
PLAYER_HEIGHT = 50
player_VILOCITY= 5
SNOW_WIDTH = 25
SNOW_HEIGHT = 25
snow_velocity = 5

FONT = pygame.font.SysFont("Times New Roman", 32, italic=True)#font object,we can use this to RENDER our text on screen
SNOW_FLAKE = pygame.image.load("snowflake.png")
SNOW_FLAKE = pygame.transform.scale(SNOW_FLAKE,(SNOW_WIDTH,SNOW_HEIGHT))


def draw(player, elapsed_time , snows):
    WINDOW.blit(BG, (0, 0))


    pygame.draw.rect(WINDOW,"#7EB7D8",player)#window name and colour rectangle and cordinate of rectangle


    time_text = FONT.render(f"Time:{round(elapsed_time)}s",1,"black")
    WINDOW.blit(time_text,(10,10))#draw mean blit means blocik transfer

    for SNOW in snows:
        WINDOW.blit(SNOW_FLAKE,(SNOW.x,SNOW.y))

    pygame.display.update()


async def main():
    run = True
    snows =[]

    player= pygame.Rect(200,HEIGHT - PLAYER_HEIGHT    ,PLAYER_WIDTH,PLAYER_HEIGHT)#x,y withdt and height,200 means place the coming code in200 left cordinates

    clock=pygame.time.Clock()
    start_time = time.time()#gave the current time,python save the number into the start time variable
    elapsed_time = 0


    snow_add_increment = 2000#means the first snow will add in 200 milli sec
    snow_count=0#tells us to count when we would add the next now after the incremen
    hit = False



    while run:

        snow_count +=clock.tick(60) # will tell us countinh how many millie sec since last tick
        elapsed_time = time.time()-(start_time)

        if snow_count>= snow_add_increment:
            for _ in range(3):#will generate 5 snows in screen
                snowx= random.randint(0, WIDTH-SNOW_WIDTH)
                snow = pygame.Rect(snowx, 0, SNOW_WIDTH, SNOW_HEIGHT)
                snows.append(snow)
                snow_add_increment = max(200, snow_add_increment - 50)

                snow_count=0





        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_VILOCITY >=0 :#.x means current position of player in horizontal
            player.x -= player_VILOCITY#. x means gave me value stores inside the player variable



        if keys[pygame.K_RIGHT]and   player.x + player_VILOCITY + player.width <=WIDTH :
            player.x += player_VILOCITY

        for snow in snows[:]:
            snow.y += snow_velocity
            if snow.y > HEIGHT:
                snows.remove(snow)
            elif snow.y + snow.height >= player.y and snow.colliderect(player):
                hit = True
                break

        if hit:
            gameover = True
            finaltime = round(elapsed_time)
            while gameover:

                WINDOW.blit(BG,(0,0))
                lost_text=FONT.render("YOU LOST SNOWY!",1,"RED")
                reply_text=FONT.render("Press R to play again,snowy",1,"#308EC5")
                quit_text=FONT.render("Press Q to quit",1,"RED")

                WINDOW.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2,HEIGHT/2 - lost_text.get_height()/2))

                WINDOW.blit(reply_text,(WIDTH/2 - reply_text.get_width()/2,HEIGHT/2 - reply_text.get_height()/2 + 50))

                WINDOW.blit(quit_text,(WIDTH/2 - quit_text.get_width()/2,HEIGHT/2 - quit_text.get_height()/2 + 100))

                final_time_text=FONT.render(f"YOUR TIME:{finaltime}s",1,"white")
                WINDOW.blit(final_time_text,(WIDTH/2 - final_time_text.get_width()/2,200))
                pygame.display.update()

                for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                    run = False
                    gameover = False
                 elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            gameover = False
                            hit = False
                            snows.clear()
                            player.x = 200
                            start_time = time.time()
                        elif event.key == pygame.K_q:
                            run = False
                            gameover = False

                await asyncio.sleep(0.05)#let the browser breathe (needed for the web version)

        draw(player, elapsed_time , snows)
        await asyncio.sleep(0)#let the browser breathe (needed for the web version)
    pygame.quit()

asyncio.run(main())
