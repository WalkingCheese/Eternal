import pygame, sys, time, random, math
from pygame.locals import *
pygame.init()
pygame.mixer.init()
w = 2440
h = 1345
fps = 60
black = (0, 0, 0)
white = (255, 255, 255)
red = (120, 0, 0)
green = (0, 200, 0)
blue = (1, 1, 120)
yellow = (255, 250, 51)
pinky = (245, 137, 200)
unknown = (70, 0, 135)
unknown2 = (255, 255, 135)
unknown3 = (170, 170, 170)
unknown4 = (50, 199, 60)
flagfr = 0
wnd = pygame.display.set_mode((w, h), 0, 32)
pygame.display.set_caption("Doom Eternal new horizons")
main_clock = pygame.time.Clock()
game_played = True
ground_level = h - 25
#music_r = random.randint(0,2)
#if music_r == 0:
#    pygame.mixer.music.load("SouNG/01 - Andrew Hulshult - At Doom's Gate.mp3")
#    pygame.mixer.music.play(-1)
#elif music_r == 1:
#    pygame.mixer.music.load("SouNG/09 - Andrew Hulshult - Hiding the Secrets.mp3")
#    pygame.mixer.music.play(-1)
#else:
#    pygame.mixer.music.load("SouNG/11 - Andrew Hulshult - I Sawed the Demons.mp3")
#    pygame.mixer.music.play(-1)

class banosTAPI:
    medkit = "medkit"
    ammo = "ammo"
    Brust_ammo = "brust_ammo"
    Shotgun_ammo = "shotgun_ammo"


class Bonussss:
    def __init__(self, x, y, bonus_type: banosTAPI, IMAGE, sounddddddddddddddddddddddddddddddddddddddddddddddddddddddd, value):
        self.image = pygame.image.load(IMAGE).convert_alpha()
        self.box = self.image.get_rect()
        self.box.center = (x, y)
        self.type = bonus_type
        self.pickUpSound = pygame.mixer.Sound(sounddddddddddddddddddddddddddddddddddddddddddddddddddddddd)
        self.value = value

    def png_draw(self, wnd: pygame.Surface):
        wnd.blit(self.image, self.box)

    def pickop(self):
        self.pickUpSound.play()
        return self.value

class AnimSprite:
    def __init__(self, img, col, row):
        self.img = img.copy()
        self.cell_w = self.img.get_width() / col
        self.cell_h = self.img.get_height() / row
        self.cells_num = col * row
        self.cell_list = list([(index % col * self.cell_w, index // col * self.cell_h, self.cell_w, self.cell_h) for index in range(self.cells_num)])

    def png_draw(self, wnd: pygame.Surface, index, posx, posy):
        wnd.blit(self.img, (posx - self.cell_w // 2, posy - self.cell_h // 2), self.cell_list[index])

class Single_Animation(AnimSprite):
    def __init__(self, img, col, row, fpa, posx, posy):
        super().__init__(img, col, row)
        self.fpa = fpa
        self.frame = 0
        self.index = 0
        self.posx = posx
        self.posy = posy
        self.is_active = True

    def png_draw(self, wnd: pygame.Surface):
        if not self.is_active:
            return
        super().png_draw(wnd, self.index, self.posx, self.posy)
        self.frame += 1
        if self.frame > self.fpa:
            self.frame = 0
            self.index += 1

        if self.index >= self.cells_num:
            self.is_active = False

class Expolosion(Single_Animation):
    def __init__(self, img, col, row, fpa, posx, posy, dmg):
        super().__init__(img, col, row, fpa, posx, posy)
        self.dmgRadius = [10, 20, 30, 40, 50, 60, 70, 80,
                          80, 90, 90, 90, 110, 120, 130, 140,
                          170, 170, 170, 170, 170, 170, 170, 170,
                          160, 150, 150, 150, 150, 150, 140, 0,
                          0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0]
        self.dmg = dmg
    def colliderect(self, box:pygame.Rect):
        r = self.dmgRadius[self.index]
        dt = abs(box.top - self.posy)
        db = abs(box.bottom - self.posy)
        dl = abs(box.left - self.posx)
        dr = abs(box.right - self.posx)
        if ((box.left < self.posx < box.right) and (dt <= r or db <= r)) or ((box.top < self.posy < box.bottom) and (dl < r or dr < r)):
            return True
        else:
            return False




class Hero:
    def __init__(self, cx, bot, w, h):
        self.player = pygame.Rect(0, 0, w, h) # 40, 80
        self.player.centerx = cx
        self.player.bottom = bot
        self.direction = 0
        self.speed = 10
        self.max_jump = 30
        self.jump_val = self.max_jump
        self.is_jump = False
        self.maxHP = 100
        self.HP = self.maxHP
        self.player_image_idle = pygame.image.load("img/p_idle.png").convert_alpha()
        self.player_image_left = [ pygame.image.load("img/p_left_1.png").convert_alpha(),
                        pygame.image.load("img/p_left_2.png").convert_alpha(),
                        pygame.image.load("img/p_left_3.png").convert_alpha(),
                        pygame.image.load("img/p_left_4.png").convert_alpha(),
                        pygame.image.load("img/p_left_5.png").convert_alpha(),
                        pygame.image.load("img/p_left_6.png").convert_alpha()]
        self.player_image_right = [pygame.image.load("img/p_right_1.png").convert_alpha(),
                        pygame.image.load("img/p_right_2.png").convert_alpha(),
                        pygame.image.load("img/p_right_3.png").convert_alpha(),
                        pygame.image.load("img/p_right_4.png").convert_alpha(),
                        pygame.image.load("img/p_right_5.png").convert_alpha(),
                        pygame.image.load("img/p_right_6.png").convert_alpha()]
        self.frame_count = 0

    def hit(self, power):
        if self.HP > 0:
            self.HP -= power
            if self.HP < 0:
                self.HP = 0

    def heck_cheat(self, val):
        self.HP += val
        if self.HP > self.maxHP:
            self.HP = self.maxHP

    def cheat(self):
        if keys[K_l]:
            self.HP = 10000
            self.maxHP = 10000

    def move(self):
        if self.direction == 1 and self.player.right < (w - self.speed):
            self.player.right += self.speed
        if self.direction == -1 and self.player.left > self.speed:
            self.player.left -= self.speed
        if self.is_jump:
            if self.jump_val > -self.max_jump:
                self.player.bottom -= self.jump_val
                self.jump_val -= 0.5
            else:
                self.is_jump = False
                self.jump_val = self.max_jump
                self.player.bottom = ground_level
        self.frame_count += 1
        if self.frame_count > 5 * 5:
            self.frame_count = 0

    def png_draw(self, wnd: pygame.Surface):
        draw_image = self.player_image_idle
        if self.direction == 1:
            draw_image = self.player_image_right[self.frame_count // 5]
        if self.direction == -1:
            draw_image = self.player_image_left[self.frame_count // 5]
        wnd.blit(draw_image, self.player)
        pygame.draw.rect(wnd, red, (self.player.left, self.player.top - 5 - self.player.h // 5, self.player.w, self.player.h // 5))
        pygame.draw.rect(wnd, green, (self.player.left, self.player.top - 5 - self.player.h // 5, int(self.player.w / self.maxHP * self.HP), self.player.h // 5))

        #  pygame.draw.rect(wnd, white, self.player, 1)



    def jump(self):
        if not self.is_jump:
            self.is_jump = True

class Zombie_bob:
    def __init__(self, cx, bot, w, h, attackSND, hitSND):

        self.hit_points = random.randint(1, 15)
        self.box = pygame.Rect(0, 0, w, h) # 40, 80
        self.box.centerx = cx
        self.box.bottom = bot
        self.direction = 0
        self.speed = 2
        self.frame_count = 0
        self.alive = True  # Maybe.
        self.is_attack = False
        self.attack_power = random.randint(0,20)
        self.attackSND = pygame.mixer.Sound("SouNG/Zumbi_attock.wav")
        self.HETSND = pygame.mixer.Sound("SouNG/Rum hited.wav")

        self.move_left_img = [pygame.image.load("img/ZwalkL1.png").convert_alpha(),
                              pygame.image.load("img/ZwalkL2.png").convert_alpha(),
                              pygame.image.load("img/ZwalkL3.png").convert_alpha(),
                              pygame.image.load("img/ZwalkL4.png").convert_alpha(),
                              pygame.image.load("img/ZwalkL5.png").convert_alpha(),
                              pygame.image.load("img/ZwalkL6.png").convert_alpha()]
        self.move_right_img = [pygame.image.load("img/ZwalkR1.png").convert_alpha(),
                               pygame.image.load("img/ZwalkR2.png").convert_alpha(),
                               pygame.image.load("img/ZwalkR3.png").convert_alpha(),
                               pygame.image.load("img/ZwalkR4.png").convert_alpha(),
                               pygame.image.load("img/ZwalkR5.png").convert_alpha(),
                               pygame.image.load("img/ZwalkR6.png").convert_alpha()]
        self.attack_right_img = [pygame.image.load("img/ZattackR1.png").convert_alpha(),
                                 pygame.image.load("img/ZattackR2.png").convert_alpha(),
                                 pygame.image.load("img/ZattackR3.png").convert_alpha(),
                                 pygame.image.load("img/ZattackR4.png").convert_alpha(),
                                 pygame.image.load("img/ZattackR5.png").convert_alpha(),
                                 pygame.image.load("img/ZattackR6.png").convert_alpha()]
        self.attack_left_img = [pygame.image.load("img/ZattackL1.png").convert_alpha(),
                                pygame.image.load("img/ZattackL2.png").convert_alpha(),
                                pygame.image.load("img/ZattackL3.png").convert_alpha(),
                                pygame.image.load("img/ZattackL4.png").convert_alpha(),
                                pygame.image.load("img/ZattackL5.png").convert_alpha(),
                                pygame.image.load("img/ZattackL6.png").convert_alpha()]
        self.idle_left_img = pygame.image.load("img/ZIdleL.png").convert_alpha()
        self.idle_right_img = pygame.image.load("img/ZIdleR.png").convert_alpha()
    def attack(self):
        if not self.is_attack:
            self.is_attack = True
            self.frame_count = 0
            self.attackSND.play()

    def hit(self, power):
        self.hit_points -= power
        if self.hit_points <= 0:
            self.hit_points = 0
            self.alive = False
        self.HETSND.play()

    def move(self, wallleftx, wallrightx):
        if self.direction == 1 and not self.is_attack:
            self.box.centerx += self.speed
        if self.direction == -1 and not self.is_attack:
            self.box.centerx -= self.speed
        if self.box.left <= wallleftx:
            self.direction = 1
        if self.box.right >= wallrightx:
            self.direction = -1
        if not self.alive:
            self.box.bottom += 1
        if self.is_attack and self.frame_count >= 5*5:
            self.is_attack = False
            self.frame_count = 0
        self.frame_count += 1
        if self.frame_count > 5 * 5:
            self.frame_count = 0

    def png_draw(self, wnd: pygame.Surface):
        draw_image = self.idle_right_img
        if self.is_attack:
            if self.direction == 1:
                draw_image = self.attack_right_img[self.frame_count // 5]
            if self.direction == -1:
                draw_image = self.attack_left_img[self.frame_count // 5]
        else:
           if self.direction == 1:
                draw_image = self.move_right_img[self.frame_count // 5]
           if self.direction == -1:
                draw_image = self.move_left_img[self.frame_count // 5]
        wnd.blit(draw_image, self.box)


class Zombie_bob_Boss(Zombie_bob):
    def __init__(self, cx, bot, w, h):
        super().__init__(cx, bot, w, h, " ", " ")
        self.hit_points = random.randint(13, 45)
        self.MAX_hit_points = self.hit_points
        self.attack_power = random.randint(18, 100)
        for i in range(len(self.move_right_img)):
            self.move_right_img[i] = pygame.transform.scale(self.move_right_img[i], (w, h))
        for i in range(len(self.move_left_img)):
            self.move_left_img[i] = pygame.transform.scale(self.move_left_img[i], (w, h))
        for i in range(len(self.attack_right_img)):
            self.attack_right_img[i] = pygame.transform.scale(self.attack_right_img[i], (w, h))
        for i in range(len(self.attack_left_img)):
            self.attack_left_img[i] = pygame.transform.scale(self.attack_left_img[i], (w, h))
        self.idle_right_img = pygame.transform.scale(self.idle_right_img, (w, h))
        self.idle_left_img = pygame.transform.scale(self.idle_left_img, (w, h))

    def png_draw(self, wnd: pygame.Surface):
        super().png_draw(wnd)
        pygame.draw.rect(wnd, red, (self.box.left, self.box.top - 5 - self.box.h // 5, self.box.w, self.box.h // 5))
        pygame.draw.rect(wnd, green, (self.box.left, self.box.top - 5 - self.box.h // 5, int(self.box.w / self.MAX_hit_points * self.hit_points),self.box.h // 5))


class Bullet:
    def __init__(self, x, y, speed, angel, rad, color, power):
        self.x = x
        self.y = y
        self.speedx = speed * math.cos(math.radians(angel))
        self.speedy = speed * math.sin(math.radians(angel))
        self.rad = rad
        self.color = color
        self.hit_box = pygame.Rect(0, 0, self.rad * 2, self.rad * 2)
        self.hit_box.center = (self.x, self.y)
        self.is_active = True
        self.power = power

    def hit(self, value):
        if self.is_active:
            self.power -= value
            if self.power <= 0:
                self.is_active = False  # Minecraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaft!! IDDQD gg ez

    def move(self):
        self.x += self.speedx
        self.y += self.speedy
        self.hit_box.center = (self.x, self.y)

    def png_draw(self, wnd: pygame.Surface):
        pygame.draw.circle(wnd, self.color, (int(round(self.x, 0)), int(round(self.y, 0))), self.rad)

        #  pygame.draw.rect(wnd, white, self.hit_box, 1)

class Rocket:
    def __init__(self, x, y, speed, angel, img_path, dmg):
        self.x = x
        self.y = y
        self.speedx = speed * math.cos(math.radians(angel))
        self.speedy = speed * math.sin(math.radians(angel))
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.rotate(self.img, -angel)
        self.hit_box = self.img.get_rect()
        self.hit_box.center = (self.x, self.y)
        self.is_active = True
        self.dmg = dmg

    def move(self):
        self.x += self.speedx
        self.y += self.speedy
        self.hit_box.center = (self.x, self.y)

    def png_draw(self, wnd: pygame.Surface):
        wnd.blit(self.img, self.hit_box)


class HandGun:
    def __init__(self, w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, ammo_type, realoadsound):
        self.box = pygame.Rect(0, 0, w, h)
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.SH_barrel_x = SH_barrel_x
        self.SH_barrel_y = SH_barrel_y
        self.bullet_dmg = random.randint(1, 10)
        self.bullet_speed = 20
        self.bullet_rad = 5
        self.direction = 0
        self.shoot_sound = pistol_sound = pygame.mixer.Sound(sound)
        self.imgR = pygame.image.load(imgR)
        self.imgL = pygame.transform.flip(self.imgR, True, False)
        self.FR = FR
        self.last_fire = 0
        self.bullet_x = self.box.centerx
        self.bullet_y = self.box.centery
        self.max_ammo = 200
        self.ammo = 50
        self.try_shoot = False
        self.ammo_type = ammo_type
        self.ang = 0
        self.max_clip = 15
        self.clip = self.max_clip
        self.reaload_sound = pygame.mixer.Sound(realoadsound)
        self.reaload_time = 1700
        self.reaload_start = 0
        self.isreload = False


    def update(self):
        self.check_reload()

    def check_reload(self):
        if self.isreload:
            if (pygame.time.get_ticks() - self.reaload_start) >= self.reaload_time:
                self.isreload = False
    def reloading(self):
        if self.isreload:
            return
        if self.ammo <= 0:
            return
        if self.clip == self.max_clip and flagfr == 0:
            return
        needed = self.max_clip - self.clip
        if self.ammo < needed:
            needed = self.ammo

        self.ammo -= needed
        self.clip += needed
        self.isreload = True
        self.reaload_start = pygame.time.get_ticks()
        self.reaload_sound.play()

    def can_Shoot(self):
        if (pygame.time.get_ticks() - self.last_fire) >= self.FR and self.clip > 0 and self.try_shoot and not self.isreload:
            return True
        else:
            return False

    def shoot(self):
        bullet_list = []
        if self.can_Shoot():
            bullet_ang = -math.degrees(self.ang) + 90
            bull = Bullet(self.bullet_x, self.bullet_y, self.bullet_speed, bullet_ang, self.bullet_rad, pinky, self.bullet_dmg)
            bullet_list.append(bull)
            self.last_fire = pygame.time.get_ticks()
            self.clip -= 1
            self.shoot_sound.play()
        self.try_shoot = False
        return bullet_list

    def addAmmo(self, value):
        self.ammo += value
        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo


    def move(self, cx, cy, direction, ang):
        self.direction = direction
        self.ang = ang
        if self.direction == 1:
            self.box.center = (cx + self.shift_x, cy - self.shift_y)
            self.bullet_x = self.box.centerx + self.SH_barrel_x
            self.bullet_y = self.box.centery + self.SH_barrel_y
        if self.direction == -1:
            self.box.center = (cx - self.shift_x, cy - self.shift_y)
            self.bullet_x = self.box.centerx - self.SH_barrel_x
            self.bullet_y = self.box.centery + self.SH_barrel_y

    def png_draw(self, wnd: pygame.Surface):
        if self.direction == 0:
            return
        if self.direction == 1:
            rot_ang = math.degrees(self.ang) - 90
            rot_img = pygame.transform.rotate(self.imgR, rot_ang)
            rot_rect = rot_img.get_rect()
            rot_rect.center = self.box.center
            wnd.blit(rot_img, rot_rect)
        if self.direction == -1:
            rot_ang = math.degrees(self.ang) + 90
            rot_img = pygame.transform.rotate(self.imgL, rot_ang)
            rot_rect = rot_img.get_rect()
            rot_rect.center = self.box.center
            wnd.blit(rot_img, rot_rect)


class Rocket_Launcher(HandGun):
    def __init__(self, w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, ammo_type, realoadsound, rocket_imgp):
        super().__init__(w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, ammo_type, realoadsound)
        self.rocket_image_path = rocket_imgp

    def shoot(self):
        bullet_list = []
        if self.can_Shoot():
            bullet_ang = -math.degrees(self.ang) + 90
            bull = Rocket(self.bullet_x, self.bullet_y, self.bullet_speed, bullet_ang, self.rocket_image_path, self.bullet_dmg)
            bullet_list.append(bull)
            self.last_fire = pygame.time.get_ticks()
            self.clip -= 1
            self.shoot_sound.play()
        self.try_shoot = False
        return bullet_list


class Brust_Rifle(HandGun):
    def __init__(self, w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, bull_inter, ammo_type, realoadsound):
        super().__init__(w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, ammo_type, realoadsound)
        self.max_ammo = 400
        self.ammo = 100
        self.bull_inter = bull_inter
        self.brust_num = 1
        self. max_brust = 3
        self.max_clip = 33
        self.clip = self.max_clip
        self.reaload_time = 2900

    def can_Brust_Shot(self):
        if self.brust_num > 0 and self.ammo > -1  and (pygame.time.get_ticks() - self.last_fire) > self.bull_inter:
            return True
        else:
            return False

    def shoot(self):
        bullet_list = []
        if self.can_Shoot():
            bullet_ang = -math.degrees(self.ang) + 90
            bull = Bullet(self.bullet_x, self.bullet_y, self.bullet_speed, bullet_ang, 3, yellow, self.bullet_dmg)
            bullet_list.append(bull)
            self.last_fire = pygame.time.get_ticks()
            self.clip -= 1
            self.brust_num = 1
            self.shoot_sound.play()
        elif self.can_Brust_Shot():
            bullet_ang = -math.degrees(self.ang) + 90
            bull = Bullet(self.bullet_x, self.bullet_y, self.bullet_speed, bullet_ang, 3, yellow, self.bullet_dmg)
            bullet_list.append(bull)
            bullet_ang = -math.degrees(self.ang) + 90
            bull = Bullet(self.bullet_x, self.bullet_y, self.bullet_speed, bullet_ang, 3, yellow, self.bullet_dmg)
            bullet_list.append(bull)
            self.last_fire = pygame.time.get_ticks()
            self.clip -= 1
            self.brust_num += 1
            if self.brust_num == self.max_brust:
                self.brust_num = 0
            self.shoot_sound.play()


        self.try_shoot = False
        return bullet_list

class Shotgun(HandGun):
    def __init__(self, w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, ammo_type, realoadsound):
        super().__init__(w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, ammo_type, realoadsound)
        self.disp = 15
        self.max_clip = 7
        self.clip = self.max_clip
        self.reaload_time = 3200

    def shoot(self):
        bullet_list = []
        if self.can_Shoot():
            bullet_ang = -math.degrees(self.ang) + 90
            bull = Bullet(self.bullet_x, self.bullet_y, self.bullet_speed, bullet_ang, 3, black, self.bullet_dmg)
            bullet_list.append(bull)
            bull = Bullet(self.box.centerx + self.SH_barrel_x, self.box.centery + self.SH_barrel_y, 1, bullet_ang, 1, green, self.bullet_dmg)
            bullet_list.append(bull)
            for doom in range(4):
                bull = Bullet(self.bullet_x, self.bullet_y, self.bullet_speed, bullet_ang + random.randint(-self.disp, self.disp), 3, black, self.bullet_dmg)
                bullet_list.append(bull)

            self.last_fire = pygame.time.get_ticks()
            self.clip -= 1
            self.shoot_sound.play()
        self.try_shoot = False
        return bullet_list

class Railgun(HandGun):
    def __init__(self, w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, realoadsound):
        super().__init__(w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, banosTAPI.ammo, realoadsound)
        self.bullet_speed = 20
        self.bullet_dmg = 50
        self.bullet_rad = 3
        self.clip = 0

    def reloading(self):
        pass

    def update(self):
        dif = pygame.time.get_ticks() - self.last_fire
        dif = int(dif / self.FR * 100)
        if dif > 100:
            dif = 100

        self.ammo = dif

    def can_Shoot(self):
        if (pygame.time.get_ticks() - self.last_fire) >= self.FR and self.try_shoot:
            return True
        else:
            return False

    def shoot(self):
        bullet_list = []
        if self.can_Shoot():
            bullet_ang = -math.degrees(self.ang) + 90
            bull = Bullet(self.bullet_x, self.bullet_y, self.bullet_speed, bullet_ang, self.bullet_rad, pinky, self.bullet_dmg)
            bullet_list.append(bull)
            self.last_fire = pygame.time.get_ticks()
            self.shoot_sound.play()
        self.try_shoot = False
        return bullet_list

class DBS(Shotgun):
    def __init__(self, w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, ammo_type, realoadsound):
        super().__init__(w, h, shift_x, shift_y, SH_barrel_x, SH_barrel_y, sound, imgR, FR, ammo_type, realoadsound)
        self.disp = 15
        self.max_clip = 2
        self.clip = self.max_clip
        self.reaload_time = 2000

    def shoot(self):
        bullets = []
        self.tmpTime = self.last_fire
        self.tmpFlag = self.try_shoot
        bullets = super().shoot()
        self.last_fire = self.tmpTime
        self.try_shoot = self.tmpFlag
        for b in super().shoot():
             bullets.append(b)
        return bullets

class GunInfo:
    def __init__(self, size, posx, posy, gun: HandGun):
        self.gun = gun
        self.size = size
        self.box = pygame.Rect(posx, posy, self.size, self.size)
        self.img = gun.imgR
        imgRect = self.img.get_rect()
        ratio = 1
        if imgRect.w > imgRect.h:
            ratio = imgRect.w / size
            print(ratio)
        else:
            ratio = imgRect.h / size
            print(ratio)
        self.img = pygame.transform.scale(self.img, (int(imgRect.w / ratio), int(imgRect.h / ratio)))
        self.bg_color = yellow
        self.border_color = red
        self.active_color = green
        self.text_color = blue
        self.is_active = False
        self.border_size = 3
        self.Font = pygame.font.SysFont("Terminal", self.size // 5, False, False)

    def png_draw(self, wnd):
        pygame.draw.rect(wnd, self.bg_color, self.box,)
        imgRect = self.img.get_rect()
        imgRect.center = self.box.center
        wnd.blit(self.img, imgRect)
        pygame.draw.rect(wnd, self.border_color, self.box, self.border_size)
        if self.is_active:
            pygame.draw.rect(wnd, self.active_color, self.box, self.border_size)
        textImg = self.Font.render(f"{self.gun.ammo}", True, self.text_color)
        imgRect = textImg.get_rect()
        imgRect.right = self.box.right - self.border_size
        imgRect.bottom = self.box.bottom - self.border_size
        wnd.blit(textImg, imgRect)

        textImg = self.Font.render(f"{self.gun.clip}", True, self.text_color)
        imgRect = textImg.get_rect()
        imgRect.left = self.box.left + self.border_size
        imgRect.bottom = self.box.bottom - self.border_size
        wnd.blit(textImg, imgRect)

class GunInfoPane():
    def __init__(self, box_size, start_x, start_y, gun_list):
        self.gun_list = gun_list
        self.hudG_list = []
        posx = start_x
        for gun in gun_list:
            hudG = GunInfo(box_size, posx, start_y, gun)
            self.hudG_list.append(hudG)
            posx += box_size

    def set_active(self, gun):
        for hudG in self.hudG_list:
            hudG.is_active = False
            if gun == hudG.gun:
                hudG.is_active = True
    def png_draw(self, wnd):
        for hudG in self.hudG_list:
            hudG.png_draw(wnd)

class Crosshair:
    def __init__(self, img_path, dist):
        self.img = pygame.image.load(img_path)
        self.box = self.img.get_rect()
        self.dist = dist
        self.posx = 0
        self.posy = 0
        self.ang = 0

    def move(self, cx, cy, ang):
        self.ang = -ang - (math.pi / 2)
        self.posy = self.dist * math.cos(self.ang) + cy
        self.posx = self.dist * math.sin(self.ang) + cx

    def pg_draw(self, wnd):
        self.box.centery = self.posy
        self.box.centerx = self.posx  #    l o l
        wnd.blit(self.img, self.box)


back_ground = pygame.image.load('img/bg.jpg').convert_alpha()
back_ground = pygame.transform.scale(back_ground, (w, h))
pistol_sound = pistol_sound = pygame.mixer.Sound("SouNG/Shoot to the cum.wav")

bullets = []
bonussus = []
zombies = [Zombie_bob(0, ground_level, 43, 71, " ", " ")]
plr = Hero(w//2, ground_level, 43, 55)
pistol = HandGun(50, 0, -10, 15, 11, 4, "SouNG/Shoot to the cum.wav", "img/Black PISTOL.png", 350, banosTAPI.ammo, "SouNG/reloadsound.wav")
rifle = Brust_Rifle(73, 23, -10, 15, 11, 4, "SouNG/Shoot to the cum.wav", "img/Brust Rifle.png", 400, 50, banosTAPI.Brust_ammo, "SouNG/reloadsound.wav")
shotgun = Shotgun(73, 23, -10, 15, 11, 4, "SouNG/Shotgun shoots into a zombie.wav", "img/SHOTGUN.png", 1500, banosTAPI.Shotgun_ammo, "SouNG/reloadsound.wav")
railgun = Railgun(104, 61, -10, 15, 46, 10, "SouNG/railgun.wav", "img/RAILGUN.png", 7000, "SouNG/reloadsound.wav")
dbs = DBS(73, 23, -10, 15, 11, 4, "SouNG/Shotgun shoots into a zombie.wav", "img/DBS.png", 4000, banosTAPI.Shotgun_ammo, "SouNG/reloadsound.wav")
RL = Rocket_Launcher(174, 83, -10, -15, 87, 42, "SouNG/rls.wav", "img/rocketlauncher.png", 1200, banosTAPI.ammo, "SouNG/reloadsound.wav", "img/rocket.png")
guns = [pistol, rifle, shotgun, railgun, dbs, RL]
active_gun = 1

crosshair = Crosshair("img/Cross.png", 55)

SCORE = 0
add_Zombie = 2
next_zombie = fps // 2
next_BBOOSSSS = 10
add_bullet = 0
next_bullet = fps // 3
drawFont = pygame.font.SysFont("Terminal", 104, False, True)
hudG = GunInfo(125, w // 2, 0, pistol)
effect_animations = []
exp_img = pygame.image.load("img/exp")
def png_draw(wnd: pygame.Surface):
    wnd.fill(blue)
    wnd.blit(back_ground, (0, 0))
    pygame.draw.line(wnd, black, (0, ground_level), (w, ground_level))
    for bullet in bullets:
        bullet.png_draw(wnd)

    for zombie in zombies:
        zombie.png_draw(wnd)

    for bonus in bonussus:
        bonus.png_draw(wnd)

    for ef in effect_animations:
        ef.png_draw(wnd)

    plr.png_draw(wnd)
    crosshair.pg_draw(wnd)
    guns[active_gun].png_draw(wnd)
    #  pygame.draw.rect(wnd, unknown4, player)
    text_image = drawFont.render(f"Score: {SCORE}", True, black)
    wnd.blit(text_image,(2, 2, 2, 2))
    hud2.png_draw(wnd)

def quit_game():
    sys.exit()
    pygme.quit()

def add_new_zombie():
    global add_Zombie, next_zombie, next_BBOOSSSS, SCORE
    if SCORE >= next_BBOOSSSS:
        zombies.append(Zombie_bob_Boss(random.choice([0, w]), ground_level, 87, 143))
        next_BBOOSSSS += random.randint(1, 3)
    elif add_Zombie >= next_zombie:
        zombies.append(Zombie_bob(random.choice([0, w]), ground_level, 43, 71, " ", " "))
        add_Zombie = 0
        next_zombie = fps
    else:
        add_Zombie += 1

def move_bullet():
    for bullet in bullets[:]:
        bullet.move()
        if 0 >= bullet.x >= w:
            bullets.remove(bullet)

def bonus_recommended(bonus_list, x, y):
    random_gun = random.choice(guns)
    if random.randint(1, 10) == 1:
        bonus = Bonussss(x, y, banosTAPI.medkit, "img/Hp_medkit.png", "SouNG/HPBONUSAMMOOMG.wav", 20)
        bonus_list.append(bonus)
    elif (random_gun.ammo) < 50 and random.randint(1, 2) == 2 and random_gun.ammo_type is not None:
        img_path = "img/AMMO bag.png"
        if random_gun.ammo_type == banosTAPI.Brust_ammo:
            img_path = "img/Brust Rifle Ammo.png"
        if random_gun.ammo_type == banosTAPI.Shotgun_ammo:
            img_path = "img/Shotgun_ammo.png"
        bonus = Bonussss(x, y, random_gun.ammo_type, img_path, "SouNG/HPBONUSAMMOOMG.wav", random.choice([30, 50]))
        bonus_list.append(bonus)


def BOSSES_must_die(z:Zombie_bob , dmg):
    global SCORE
    if z.alive:
        z.hit(dmg)
        if not z.alive:
            SCORE += 1
            print(f'score : {SCORE}')
            bonus_recommended(bonussus, z.box.centerx, z.box.centery)

def make_explosion(bullet):
    print("boom?")
    ex = Expolosion(exp_img, 8, 6, 1, bullet.hit_box.centerx, bullet.hit_box.centery, bullet.dmg)
    #enter sound here(expsound.play()
    effect_animations.append(ex)
    bullet.is_active = False

def check_exp_dmg(zombie_list, exp_list):
    for exp in exp_list:
        if exp.is_active:
            for z in zombie_list:
                if exp.colliderect(z.box):
                    BOSSES_must_die(z, exp.dmg)
        else:
            exp_list.remove(exp)

def check_zombie_hit(zombie_list, bullet_list):
    for zombie in zombie_list:
        for bullet in bullet_list[:]:
            if bullet.is_active:
                if zombie.box.colliderect(bullet.hit_box):
                    if isinstance(bullet, Rocket):
                        make_explosion(bullet)
                    else:
                        BOSSES_must_die(zombie, bullet.power)
                        bullet.hit(random.randint(1,2))
                        if not bullet.is_active:
                            bullet_list.remove(bullet)

def gun_shoot():
    bullet_list = guns[active_gun].shoot()
    for bull in bullet_list:
        bullets.append(bull)

def try_shoot():
    guns[active_gun].try_shoot = True

def check_zombie_attack(hero, zombie_list):
    global game_played
    for zombie in zombie_list:
        if zombie.alive and not zombie.is_attack:
            if hero.player.colliderect(zombie.box):
                zombie.attack()
                hero.hit(zombie.attack_power)
    if  hero.HP == 0:
        game_played = False


def move_zombie():
    for zombie in zombies[:]:
        zombie.move(0, w)
        if zombie.box.top > h:
            zombies.remove(zombie)

def AAAAAAAAAAAA(hero, speed):
    hero.player.top -= speed

def move_gun(hero: Hero, ang):
    guns[active_gun].move(hero.player.centerx, hero.player.centery, hero.direction, ang)

def png_drawGO(wnd: pygame.Surface):
    png_draw(wnd)
    plr.png_draw(wnd)
    #  pygame.draw.rect(wnd, unknown4, player)
    drawFont = pygame.font.SysFont("Terminal", 56, False, False)
    tExT_ImAgE = drawFont.render("Game over, fool!", True, black)
    TexT_RecT = tExT_ImAgE.get_rect()
    TexT_RecT.center = (w // 2, h // 2 + 2 )
    wnd.blit(tExT_ImAgE, TexT_RecT)
    bw = w // 3
    bh = h// 10
    rect = pygame.Rect(w // 2 - bw, h // 2 - bw // 2, bw, bh)
    drawFont = pygame.font.SysFont("Terminal", bh, False, False)
    tExT_ImAgE = drawFont.render("Go back!", True, black)
    TexT_RecT = tExT_ImAgE.get_rect()
    TexT_RecT.center = rect.center
    pygame.draw.rect(wnd, green, rect)
    wnd.blit(tExT_ImAgE, TexT_RecT)

    rect = pygame.Rect(w // 2, h // 2 - bw // 2, bw, bh)
    drawFont = pygame.font.SysFont("Terminal", bh, False, False)
    tExT_ImAgE = drawFont.render("Run away!", True, black)
    TexT_RecT = tExT_ImAgE.get_rect()
    TexT_RecT.center = rect.center
    pygame.draw.rect(wnd, red, rect)
    wnd.blit(tExT_ImAgE, TexT_RecT)

def check_Bonus_Pick_Up(player:Hero, bonus_list:list):
    for bon in bonus_list:
        if bon.box.colliderect(plr.player):   # in problem plr is wrong player good
            val = bon.pickop()
            if bon.type == banosTAPI.medkit:
                player.heck_cheat(val)  # in problem player is wrong plr good
            if bon.type == banosTAPI.ammo:
                guns[0].addAmmo(val)
            if bon.type == banosTAPI.Brust_ammo:
                guns[1].addAmmo(val)
            if bon.type == banosTAPI.Shotgun_ammo:
                guns[2].addAmmo(val)

            bonus_list.remove(bon)

def update():
    for gun in guns:
        gun.update()

def findAimAng(player: Hero, mx, my):
    dx = plr.player.centerx - mx
    dy = plr.player.centery - my
    ang = math.atan2(dy, dx)
    return ang


while True:
    bullets = []
    bonussus = []
    zombies = [Zombie_bob(0, ground_level, 43, 71, " ", " ")]
    plr = Hero(w // 2, ground_level, 43, 55)
    pistol = HandGun(50, 0, -10, 15, 11, 4, "SouNG/Shoot to the cum.wav", "img/Black PISTOL.png", 350, banosTAPI.ammo, "SouNG/reloadsound.wav")
    rifle = Brust_Rifle(73, 23, -10, 15, 11, 4, "SouNG/Shoot to the cum.wav", "img/Brust Rifle.png", 400, 50,
                        banosTAPI.Brust_ammo, "SouNG/reloadsound.wav")
    shotgun = Shotgun(73, 23, -10, 15, 11, 4, "SouNG/Shotgun shoots into a zombie.wav", "img/SHOTGUN.png", 1500,
                      banosTAPI.Shotgun_ammo, "SouNG/reloadsound.wav")
    railgun = Railgun(104, 61, -10, 15, 46, 10, "SouNG/railgun.wav", "img/RAILGUN.png", 7000, "SouNG/reloadsound.wav")
    dbs = DBS(73, 23, -10, 15, 11, 4, "SouNG/Shotgun shoots into a zombie.wav", "img/DBS.png", 4000,
              banosTAPI.Shotgun_ammo, "SouNG/reloadsound.wav")
    RL = Rocket_Launcher(174, 83, -10, -15, 87, 42, "SouNG/rls.wav", "img/rocketlauncher.png", 1200, banosTAPI.ammo,
                         "SouNG/reloadsound.wav", "img/rocket.png")
    guns = [pistol, rifle, shotgun, railgun, dbs, RL]
    active_gun = 1
    hud2 = GunInfoPane(125, w // 2 - int(125 * 3), 0, guns)
    hud2.set_active(guns[active_gun])
    add_Zombie = 2
    next_zombie = fps // 2
    next_BBOOSSSS = 10
    SCORE = 0

    game_played = True
    while game_played:
        main_clock.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()

        keys = pygame.key.get_pressed()
        if keys[K_o]:
            flagfr = 1
        if keys[K_ESCAPE]:
            quit_game()
        if keys[K_a]:
            plr.direction = -1
        if keys[K_d]:
            plr.direction = 1
        if keys[K_r]:
            plr.direction = 0
        if keys[K_q]:
            plr.speed = 50
        else:
            plr.speed = 10
        if keys[K_SPACE]:
            plr.jump()

        if not guns[active_gun].isreload:
            if keys[K_1]:
                active_gun = 0

            if keys[K_2]:
                active_gun = 1
            if keys[K_3]:
                active_gun = 2
            if keys[K_4]:
                active_gun = 3
            if keys[K_5]:
                active_gun = 4
            if keys[K_6]:
                active_gun = 5

        if keys[K_r]:
            guns[active_gun].reloading()

        hud2.set_active(guns[active_gun])

        mx, my = pygame.mouse.get_pos()
        mkeys = pygame.mouse.get_pressed()

        plr.move()
        crosshair.move(plr.player.centerx, plr.player.centery, findAimAng(plr, mx, my))
        check_Bonus_Pick_Up(plr, bonussus)
        move_gun(plr, crosshair.ang)
        if mkeys[0] and  plr.direction != 0:
            try_shoot()

        update()
        gun_shoot()
        plr.cheat()
        move_bullet()
        add_new_zombie()
        move_zombie()
        check_zombie_hit(zombies, bullets)
        check_exp_dmg(zombies, effect_animations)
        check_zombie_attack(plr, zombies)
        png_draw(wnd)
        pygame.display.update()
    gameOver = True
    while gameOver:
        main_clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                testRect = pygame.Rect(x, y, 9, 9)
                bw = w // 3
                bh = h // 10

                GoBackBtn = pygame.Rect(w // 2 - bw, h // 2 - bw // 2, bw, bh)
                RunAwayBtn = pygame.Rect(w // 2, h // 2 - bw // 2, bw, bh)
                if GoBackBtn.colliderect(testRect):
                    gameOver = False
                elif  RunAwayBtn.colliderect(testRect):
                    quit_game()
        plr.direction = 0

        AAAAAAAAAAAA(plr, 3)
        crosshair.move(plr.player.centerx, plr.player.centery, findAimAng(plr, mx, my))

        move_gun(plr, 0)
        png_drawGO(wnd)
        pygame.display.update()
#     wnd.fill(blue)
#     wnd.blit(back_ground, (0, 0))
#     pygame.draw.line(wnd, black, (0, ground_level), (w, ground_level))
#     for zombie in zombies:
#         zombie.png_draw(wnd)


# if add_bullet >= next_bullet:
#               bullet = Bullet(plr.player.centerx, plr.player.centery, 51, plr.direction, 6, yellow)
#               bullets.append(bullet)
#               add_bullet = 0
#               pistol_sound.play()

