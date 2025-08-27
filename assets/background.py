import random
from objects import stele, stele_caz
from assets.assets import *
from constants import *

from objects import platform_obj, black_hole_obj
platforms = [platform_obj("left"), platform_obj("right")]  # PLATFORMS COORDINATES
mouse_positions = []  # the positions of the black holes
bhs = [black_hole_obj() for _ in range(3)]  # BLACK HOLES COORDINATES
bhs_size = [bh.size for bh in bhs]


stars = []
cazatoare = []
numar_stele_cazatoare = 0  # number of fallen stars (translated from Romanian)
numar_stele_prezente = 0
last_spawn_time = pygame.time.get_ticks()
last_spawn_time_1 = pygame.time.get_ticks()
last_time = pygame.time.get_ticks()


def gen_list_stele():
    global numar_stele_prezente
    for _ in range(STARS_NUM):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        stea = stele(x, y)
        stars.append(stea)
        numar_stele_prezente += 1


def afis_stele(screen):
    global stars
    for star in stars:
        star.draw(screen)


def gen_stele_caz():
    global numar_stele_cazatoare, last_spawn_time, cazatoare
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time >= SPAWN_TIME_FALL:
        numar_stele_cazatoare += 1
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        directie = random.randint(0, 3)
        speed = random.randint(5, 10)

        if numar_stele_cazatoare % random.randint(2, 6) == 0:
            stea_cazatoare = stele_caz(x, y, speed, directie, 1)
        else:
            stea_cazatoare = stele_caz(x, y, speed, directie, 0)

        if directie == 2:
            stea_cazatoare.image = pygame.transform.rotate(stea_cazatoare.image, 90)
        if directie == 3:
            stea_cazatoare.image = pygame.transform.rotate(stea_cazatoare.image, -90)
        if directie == 1:
            stea_cazatoare.image = pygame.transform.rotate(stea_cazatoare.image, 180)

        cazatoare.append(stea_cazatoare)
        last_spawn_time = current_time


def afis_stele_caz(screen):
    global cazatoare
    for caz in cazatoare:
        caz.draw(screen)
        caz.move()


def add_stele():
    current_time_1 = pygame.time.get_ticks()
    global last_time, numar_stele_prezente
    if current_time_1 - last_time >= ADD_REMOVE_TIME:
        for _ in range(8):
            xx = random.randint(0, SCREEN_WIDTH)
            yy = random.randint(0, SCREEN_HEIGHT)
            stea_noua = stele(xx, yy)
            stars.append(stea_noua)
            last_time = current_time_1
            numar_stele_prezente += 1


def rem_stele():
    global numar_stele_prezente, last_spawn_time_1, stars
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time_1 >= ADD_REMOVE_TIME and \
            numar_stele_prezente > 2:
        for _ in range(8):
            stars.pop(random.randint(0, numar_stele_prezente - 1))
            last_spawn_time_1 = current_time
            numar_stele_prezente -= 1


# function to call all function at once (ro: functie pentru a apela toate functiile de odata)
def zeus(screen, string=None):
    screen.blit(backgroundd, (0, 0))

    afis_stele(screen)

    add_stele()
    rem_stele()
    gen_stele_caz()

    if string is not None:
        afis_stele_caz(screen)
