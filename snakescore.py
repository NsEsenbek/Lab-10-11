import pygame
import random
import psycopg2
import psycopg2.extras
nametoscore = input()
pygame.init()

screen = pygame.display.set_mode((700, 600))
skok_pls = 3
speed = 20
startapp = True
y = 20
x = 20
clock = pygame.time.Clock()
motion = 0
number = 0
lx = []
ly = []
pos_eda = [random.randrange(0, 700, 10), random.randrange(0, 600, 10)]
rezhim = False
game_over = False
font = pygame.font.SysFont('arial', 20)
now = 0
font_game_over = pygame.font.SysFont('arial', 30)
while startapp:
    if not game_over:
        screen.fill((0, 0, 0))         
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                       startapp = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and motion != 2:
                    motion = 1
                    break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and motion != 1:
                    motion = 2
                    break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and motion != 4:
                    motion = 3
                    break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and motion != 3:
                    motion = 4
                    break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    for i in range(skok_pls):
                        number += 1
                        rezhim = True
                        if number == 1:
                            lx.append(x)
                            ly.append(y)
                        elif number > 1:
                            lx.append(lx[number - 2])
                            ly.append(ly[number - 2])
                    break
    if x == pos_eda[0] and y == pos_eda[1]:
        for i in range(skok_pls):
            number += 1
            rezhim = True
            if number == 1:
                lx.append(x)
                ly.append(y)
            elif number > 1:
                lx.append(lx[number - 2])
                ly.append(ly[number - 2])
        now += 1
        pos_eda = [random.randrange(0, 700, 10), random.randrange(0, 600, 10)]
    for i in range(number - 1, -1, -1):
        if i != 0:
            lx[i] = lx[i - 1]
            ly[i] = ly[i - 1]
        else:
            lx[0] = x
            ly[0] = y
     #    lx[3] = lx[2]
     #    lx[2] = lx[1]
     #    lx[1] = lx[0]
     #    lx[0] = x
     #    ly[3] = ly[2]
     #    ly[2] = ly[1]
     #    ly[1] = ly[0]
     #    ly[0] = y
     #    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(lx[0], ly[0], 10, 10))
     #    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(lx[1], ly[1], 10, 10))
     #    pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(lx[2], ly[2], 10, 10))
     #    pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(lx[3], ly[3], 10, 10))
    for i in range(number):
        if game_over == False:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(lx[i], ly[i], 10, 10))
    for i in range(skok_pls, number):
        if x == lx[i] and y == ly[i]:
            motion = 0
            game_over = True
    if (x == 0 and motion == 1) or (x == 700 - 10 and motion == 2) or (y == 0 and motion == 4) or (y > 600 - 10 and motion == 3):
        game_over = True
        motion = 0
    if motion == 1 and x > 0 and game_over == False:
        x -= 10
    if motion == 2 and x < 700 - 10 and game_over == False:
        x += 10
    if motion == 3 and y < 600 - 10 and game_over == False:
        y += 10
    if motion == 4 and y > 0 and game_over == False:
        y -= 10
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(x, y, 10, 10))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(pos_eda[0], pos_eda[1], 10, 10))
    now_s = str(now)
    text = font.render(now_s, True, (155, 155, 155))
    screen.blit(text, (5, 5))
    if game_over:
            text_game_over = font_game_over.render('Game Over', True, (255, 0, 0))
            screen.blit(text_game_over, (280, 250))
            text_to = 'Your Score ' + str(now)
            text_game_over = font_game_over.render(text_to, True, (255, 0, 0))
            screen.blit(text_game_over, (280, 280))
    pygame.display.flip()
    clock.tick(speed)

username = "postgres"
pwd = "FuryRyosuke"
database = "demo"
port_id = "5432"
hostname = "localhost"
conn = None
end = False
try:    
    with psycopg2.connect(
        host = hostname,
        dbname = database,
        password = pwd,
        user = username,
        port = port_id
    ) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            # cur.execute('DROP TABLE employee')
            create_script = ''' CREATE TABLE IF NOT EXISTS snake (
                                    id serial PRIMARY KEY,
                                    name    varchar(40) NOT NULL,
                                    score   int NOT NULL) '''
            cur.execute(create_script)
            values = (nametoscore, now)
            print(values)
            insert_script = 'INSERT INTO snake (name, score) VALUES (%s, %s)'
            cur.execute(insert_script, values)
            conn.commit()
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()