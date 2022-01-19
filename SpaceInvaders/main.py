import pygame, sys
from random import choice, randint
import obstacles
import lasers
from player import Player
from Invaders import Indvaders, Extra


class Game:
    def __init__(self):
        #Player
        player_sprite = Player((screen_width / 2, screen_hight))
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #Health
        self.lives = 3
        self.lives_surf = pygame.image.load('assets/player.png').convert_alpha()
        self.lives_startpos_X = screen_width - (self.lives_surf.get_size()[0] * 2 + 20)

        #Obstalce
        self.shape = obstacles.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.create_multi_obstacke(0, 100, 200, 300, 400, 500, 600, x_start=17.5, y_start=480)

        #Invaders
        self.invaders = pygame.sprite.Group()
        self.invaders_lasers = pygame.sprite.Group()
        self.invaders_setup(rows=6, cols=8)
        self.invaders_dir = 1

        #Extra
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spwan_time = randint(400, 800)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start +row_index * self.block_size
                    block = obstacles.Block(self.block_size,(255,127,36),x,y)
                    self.blocks.add(block)

    def create_multi_obstacke(self, *offset, x_start, y_start,):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def invaders_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 70):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    invaders_sprite = Indvaders('yellow', x, y,)
                elif 1 <= row_index <= 2:
                    invaders_sprite = Indvaders('green', x, y,)
                else:
                    invaders_sprite = Indvaders('red', x, y, )
                self.invaders.add(invaders_sprite)

    def invaders_position(self):
        all_invaders = self.invaders.sprites()
        for invader in all_invaders:
            if invader.rect.right >= screen_width:
                self.invaders_dir = -1
                self.invaders_invade(1)
            elif invader.rect.left <= 0:
                self.invaders_dir = 1
                self.invaders_invade(1)

    def invaders_invade(self, distance):
        if self.invaders:
            for invader in self.invaders.sprites():
                invader.rect.y += distance

    def invader_shoot(self):
        if self.invaders.sprites():
            random_invader = choice(self.invaders.sprites())
            laser_sprite = lasers.Laser(random_invader.rect.center, -6, screen_hight)
            self.invaders_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spwan_time -= 1
        if self.extra_spwan_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spwan_time = randint(400, 800)

    def collision_check(self):

        #player
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:

                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.invaders, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.extra, True):
                    laser.kill()

        if self.invaders_lasers:
            for laser in self.invaders_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.invaders:
            for invader in self.invaders:
                pygame.sprite.spritecollide(invader, self.blocks, True)

                if pygame.sprite.spritecollide(invader, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.lives_startpos_X + (live * (self.lives_surf.get_size()[0] + 10))
            screen.blit(self.lives_surf, (x, 8))

    def run(self):
        self.player.update()
        self.invaders.update(self.invaders_dir)
        self.invaders_position()
        self.invaders_lasers.update()
        self.extra_alien_timer()
        self.extra.update()

        self.display_lives()

        self.collision_check()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)
        self.invaders.draw(screen)
        self.invaders_lasers.draw(screen)
        self.extra.draw(screen)

if __name__ == '__main__':
    pygame.init()

    #----------Variablen------------------------------------------------------------------------------------------------
    screen_width = 600
    screen_hight = 600
    #----------Variablen------------------------------------------------------------------------------------------------

    #----------Screen---------------------------------------------------------------------------------------------------
    screen = pygame.display.set_mode((screen_width, screen_hight))
    #----------Screen---------------------------------------------------------------------------------------------------

    clock = pygame.time.Clock()
    game = Game()

    INVADERLASER = pygame.USEREVENT
    pygame.time.set_timer(INVADERLASER, 800)

    #----------While-Loop-----------------------------------------------------------------------------------------------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == INVADERLASER:
                game.invader_shoot()


        screen.fill((22, 22, 22))
        game.run()
        pygame.display.flip()
        clock.tick(60)

    #----------While-Loop-----------------------------------------------------------------------------------------------
