from core.utils import *
from constants import *
from assets.assets import platform, black_hole
import random, math, pygame


class stele_caz:
    def __init__(self, x, y, speed, directie, numar_poza):
        self.x = x
        self.y = y
        self.directie = directie
        self.image = pygame.image.load(f'images/stea_cazatoare{numar_poza}.png')
        self.speed = speed
        xx = random.randint(50, 100)
        self.image = pygame.transform.scale(self.image, (xx, xx))

    def move(self):
        di = [1, -1, 1, -1]
        dj = [1, -1, -1, 1]
        self.x += di[self.directie] * self.speed
        self.y += dj[self.directie] * self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class stele:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        number = random.randint(0, 1)
        self.image = pygame.image.load(f"images/stea{number}.png")
        xx = random.randint(10, 25)
        yy = random.randint(10, 25)
        self.image = pygame.transform.scale(self.image, (xx, yy))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class nava:
    def __init__(self, x, y, speed, angle, char):
        self.x_corner = x  # top left corner x, y
        self.y_corner = y
        self.x = x + NORMAL_SHIP_X / 2  # the ship center x, y
        self.y = y + NORMAL_SHIP_Y / 2

        self.land_end = False
        self.land_start = True
        self.dead = False  # for NEAT only

        self.counter = 0
        self.angle = angle
        self.speed = speed
        self.number = char  # c mean with fire, r mean without fire (from: ro: foc, en:fire and ro: fara, en:without)

        self.image_normal = pygame.image.load(f'images/nava_fr.png')  # normal ship
        self.image_fire = pygame.image.load(f'images/nava_fc.png')  # ship with fire
        self.image_normal = pygame.transform.scale(self.image_normal, (NORMAL_SHIP_X, NORMAL_SHIP_Y))
        self.image_fire = pygame.transform.scale(self.image_fire, (SHIP_FIRE_X, SHIP_FIRE_Y))
        self.image = self.image_fire
        self.rect = self.image_normal.get_rect(center=(self.x, self.y))

        self.vel_x = 0
        self.vel_y = 0
        self.thrust = 0
        self.acceleration = 0.15  # before it was 1.75
        self.rotation_speed = 1.5  # before it was 2.5
        self.angular_velocity = 0
        # we don't have precision when the speed is lower to none (angular_velocity <<)

    def move(self, thrust_input, platforms, bhs):
        if thrust_input:
            if self.land_start:  # i can only take off from the first platform   # or self.land_end:
                self.vel_y = -1.15  # how fast the ship takes off
                self.land_start = False
                self.thrust = thrust_input
                self.image = self.image_fire
            else:
                self.image = self.image_fire
                self.thrust = min(self.thrust + 0.02, 1.0)

                rad = math.radians(self.angle)
                self.vel_x += -math.sin(rad) * self.acceleration * self.thrust
                self.vel_y += -math.cos(rad) * self.acceleration * self.thrust  # i need cos (0) = 1, for up button
        else:
            self.image = self.image_normal
            self.thrust = max(self.thrust - 0.02, 0)

        # physics
        self.rect = pygame.Rect(0, 0, NORMAL_SHIP_X, NORMAL_SHIP_Y)
        self.rect.center = (self.x, self.y)

        # gravity
        self.vel_y += 0.05  # 0.05

        # collisions
        self.rect, self.vel_x, self.vel_y, self.land_start, self.land_end = \
            handle_collision_with_platform(self.rect, self.vel_x, self.vel_y, platforms, self.land_start, self.land_end)
        self.x += self.vel_x
        self.y += self.vel_y

        # something like an air resistance
        self.vel_x *= 0.9825
        self.vel_y *= 0.9825
        self.angular_velocity *= 0.95

        self.rect.center = (self.x, self.y)

        for plt in platforms:
            plat = plt.platform_rect
            if plat.colliderect(self.rect):
                if abs(self.vel_x) < 0.6 and abs(self.vel_y) < 0.6 and abs(self.angle % 360) < 10:
                    self.vel_x = 0
                    self.vel_y = 0
                    self.angular_velocity = 0
                    self.angle = 0

        # --------------- black hole gravity + spin --------------- END / START
        inside_bh = False
        for bh in bhs:
            # pygame.draw.circle(screen, RED, bh.bh_rect.center, int(bh.radius), 1)  # debugging

            dist = distance(self.x, bh.x, self.y, bh.y)

            if dist < bh.radius:  # if i am in the black hole
                inside_bh = True
                #  ship.vel_x, ship.vel_y = 0, 0  # we stop all the moving
                self.acceleration = 0.15 * (dist / bh.radius)  # ship.acceleration = 0
                self.angular_velocity += self.rotation_speed * 0.1
                self.angular_velocity += (bh.radius - dist) / bh.radius * 0.2

                dx = bh.x - self.x
                dy = bh.y - self.y
                pull_strength = ((bh.radius - dist) / bh.radius) * (bh.size / 50)  # 100)
                self.x += (dx / dist) * pull_strength * 2.5  # MAYBE WE MAKE LEVELS WITH ATTRACTION FORCE BIGGER
                self.y += (dy / dist) * pull_strength * 2.5  # play here with the PULL POWER FIRST IT WAS * 2 NOW * 3

                if dist < bh.size / 10:  # if we get too close to the bhs we respawn
                    # should_recreate_ship = True
                    self.dead = True

        if not inside_bh:
            self.acceleration = 0.15

    def left_right(self, screen, platforms, bhs):
        keys = pygame.key.get_pressed()
        push = keys[pygame.K_UP]
        thrust_input = 1.0 if push else 0.0

        self.move(thrust_input, platforms, bhs)

        moving = abs(self.vel_y) > 0.4 or abs(self.vel_x) > 0.4  # i modified this value from 0.1 -> 0.4
        if self.number == 'r' and moving:  # en: only if i move i can turn (ro: numai daca ma misc sa ma pot intoarce)
            if keys[pygame.K_LEFT]:  # push is true <-> i'm moving
                self.angular_velocity += self.rotation_speed * 0.1  # i added + and * 0.1
            elif keys[pygame.K_RIGHT]:
                self.angular_velocity += self.rotation_speed * 0.1 * (-1)

            # ----------- if i am near a platform i want to slow down for landing --------
            nearest_platform = min(platforms, key=lambda plat: get_distance(self.rect, plat.platform_rect))
            dist_to_platform = get_distance(self.rect, nearest_platform.platform_rect)

            self.angular_velocity *= 0.85 if dist_to_platform < 50 else 0.98  # before 0.9
            self.angle += self.angular_velocity
            # ---------------------------------------------------------------------------

        # self.move(push, platforms) # move up

        # ------------------- the ship with fire image has an offset of 22 px on y  --------------------
        if self.image == self.image_fire:
            rotated_img = pygame.transform.rotate(self.image, self.angle)

            rad = math.radians(self.angle)
            fire_center = (self.x + math.sin(rad) * 22, self.y + math.cos(rad) * 22)

            new_rect = rotated_img.get_rect(center=fire_center)
        else:
            rotated_img, new_rect = rotate_img(self.image, self.angle, (self.x, self.y))

        screen.blit(rotated_img, new_rect.topleft)

        return self.angle

    def draw_rect_ship(self, screen):
        pygame.draw.polygon(screen, BLUE, [pygame.math.Vector2(p).rotate(-self.angle) + (self.x, self.y) for p in
                                           [(-self.rect.width / 2, -self.rect.height / 2),
                                            (self.rect.width / 2, -self.rect.height / 2),
                                            (self.rect.width / 2, self.rect.height / 2),
                                            (-self.rect.width / 2, self.rect.height / 2)]], 2)

    def draw_ship(self, screen, x, y, photo):
        if photo == "normal":
            screen.blit(self.image_normal, (x, y))
        else:
            screen.blit(self.image_fire, (x, y))

    # NEAT use the next 3 functions :
    # update_ai is the copy of : left_right() but for NEAT with small changes which are marked with : '--'
    def update_ai(self, thrust, rotate_left, rotate_right, screen, platforms, bhs):
        moving = abs(self.vel_y) > 0.4 or abs(self.vel_x) > 0.4

        # thrust is push from left_right
        # self.move((thrust > 0.5), platforms)
        self.move(thrust, platforms, bhs)  # HERE I CHANGE  -------------------- AND ------------------

        if self.number == 'r' and moving:
            if rotate_left > 0.5:  # here i change to rotate_left / right ------------- HERE -------------
                self.angular_velocity += self.rotation_speed * 0.1
            elif rotate_right > 0.5:
                self.angular_velocity += self.rotation_speed * 0.1 * (-1)

            # slow down near platforms
            # nearest_platform = min(platforms, key=lambda plat: get_distance(self.rect, plat.platform_rect))
            dist_to_platform = get_distance(self.rect, platforms[1].platform_rect)
            self.angular_velocity *= 0.85 if dist_to_platform < 50 else 0.98

            self.angle += self.angular_velocity

        if self.image == self.image_fire:  # the fire offset
            rotated_img = pygame.transform.rotate(self.image, self.angle)

            rad = math.radians(self.angle)
            fire_center = (self.x + math.sin(rad) * 22, self.y + math.cos(rad) * 22)

            new_rect = rotated_img.get_rect(center=fire_center)
        else:
            rotated_img, new_rect = rotate_img(self.image, self.angle, (self.x, self.y))

        screen.blit(rotated_img, new_rect.topleft)
    def get_state(self, targetx, targety, bhs):
        return [
            self.vel_x,
            self.vel_y,
            self.angle,
            distance(self.x, targetx, self.y, targety),
            min(distance(self.x, bh.x, self.y, bh.y) for bh in bhs),
            # I can add more
        ]
    def crashed(self, bhs):
        for bh in bhs:
            dist = distance(self.x, bh.x, self.y, bh.y)
            if dist < bh.size / 2:
                return True
        return False


class platform_obj:
    def __init__(self, position):
        self.platform_corner_x = MIN_PLATFORM_X if position == "left" else MAX_PLATFORM_X
        self.platform_corner_y = random.randint(MIN_PLATFORM_Y, MAX_PLATFORM_Y)

        self.platform_rect = pygame.Rect(self.platform_corner_x, self.platform_corner_y,
                                         PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def draw_platform(self, screen):
        screen.blit(platform, (self.platform_corner_x, self.platform_corner_y))

    def draw_rect(self, screen):
        draw_rect(self.platform_corner_x, self.platform_corner_y, PLATFORM_WIDTH, PLATFORM_HEIGHT, screen)


class black_hole_obj:
    def __init__(self):
        self.x, self.y = None, None  # the black hole center  |   # in plus sterge daca nu trebuie
        self.bh_rect = None

        angles = [0, 45, 90, 135, 180, 225, 270, 315]               # z -> angle position in array
        self.size, z = random.randint(20, 100), random.randint(0, 7)  # size -> the size of bh's
        self.image_scale = pygame.transform.scale(black_hole, (self.size, self.size))

        self.angle = angles[z]
        self.image_rotate = pygame.transform.rotate(self.image_scale, self.angle)

        self.radius = 2.5 * self.size  # you can change here the radius of the black holes, first it was * 2

    def rect_draw(self, screen, xmouse, ymouse):
        self.bh_rect = pygame.Rect(0, 0, self.size, self.size)
        self.bh_rect.center = (xmouse, ymouse)

        self.x = self.bh_rect.center[0]   # the black hole center
        self.y = self.bh_rect.center[1]

        img_rect = self.image_rotate.get_rect(center=self.bh_rect.center)
        screen.blit(self.image_rotate, img_rect.topleft)
        # pygame.draw.rect(screen, (255, 0, 0), self.bh_rect, 1)



# press 2 times r to really reload all projects mentioned
# only "game.py" reload everytime -> (always_reload)

# angular_velocity >> means harder rotation, is useful near bhs / platform
#           i should make it .9 near bhs / platform and in rest .96


# (RO: stele) EN : stars
# (RO: stele_caz) EN : falling stars

