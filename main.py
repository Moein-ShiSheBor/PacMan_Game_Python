import pygame
import random as rand

pygame.init()

# clock
clock = pygame.time.Clock()
fps = 100

# screen size
screen_width = 800
screen_hight = 800

screen = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption('PacMan')

# define game variables
tile_size = 50
finish = False

# load image
bg_img = pygame.image.load('image/background.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_hight))
restart_image = pygame.image.load('image/restart.png')
restart_image = pygame.transform.scale(restart_image, (100, 100))


# Data
# 0 -> empty
# 1 -> block
# 2 -> pacman
# 3 -> food

class World_maker():
    def __init__(self):
        # self.data = [[0]*16]*16

        self.data = [[0 for i in range(screen_width // 50)] for j in range(screen_width // 50)]

        # block making
        self.make_floor_and_ceiling(0)
        self.make_floor_and_ceiling(screen_width // 50 - 1)
        self.make_column(0)
        self.make_column(screen_width // 50 - 1)
        self.random_block()

        self.make_pacman()
        self.make_food()

    def make_floor_and_ceiling(self, row):
        for i in range(0, screen_width // 50):
            self.data[row][i] = 1

    def make_column(self, col):
        for j in range(0, screen_width // 50):
            self.data[j][col] = 1

    def random_block(self):
        number_of_blocks = rand.randint(0, 10)
        counter = 0

        while counter < number_of_blocks:
            row, col = self.random_col_and_row()

            if self.data[row][col] == 0:
                self.data[row][col] = 1
                counter += 1

    def make_pacman(self):
        row, col = self.random_col_and_row()

        if self.data[row][col] == 0:
            self.data[row][col] = 2
        else:
            self.make_pacman()

    def make_food(self):
        row, col = self.random_col_and_row()

        if self.data[row][col] == 0:
            self.data[row][col] = 3
        else:
            self.make_food()

    def random_col_and_row(self):
        row = rand.randint(1, screen_width // 50 - 2)
        col = rand.randint(1, screen_width // 50 - 2)
        return row, col


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.click = False

    def draw(self):
        action = False
        # mouse position
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.click:
                action = True
                self.click = True

            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, finish):
        dx = 0
        dy = 0
        move_cooldown = 10

        if not finish:

            # key press
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT] and not self.right:
                dx += tile_size
                self.right = True
                self.direction = 1
            if not key[pygame.K_RIGHT]:
                self.right = False
            if key[pygame.K_LEFT] and not self.left:
                dx -= tile_size
                self.left = True
                self.direction = -1
            if not key[pygame.K_LEFT]:
                self.left = False
            if key[pygame.K_UP] and not self.up:
                dy -= tile_size
                self.up = True
                self.direction = 11
            if not key[pygame.K_UP]:
                self.up = False
            if key[pygame.K_DOWN] and not self.down:
                dy += tile_size
                self.down = True
                self.direction = -11
            if not key[pygame.K_DOWN]:
                self.down = False

            # animation
            self.counter += 1
            if self.counter > move_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.image_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.image_right[self.index]
                elif self.direction == -1:
                    self.image = self.image_left[self.index]
                elif self.direction == 11:
                    self.image = self.image_up[self.index]
                elif self.direction == -11:
                    self.image = self.image_down[self.index]

            # collision
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.wigth, self.height):
                    dx = 0
                elif tile[1].colliderect(self.rect.x, self.rect.y + dy, self.wigth, self.height):
                    dy = 0
            # end game
            if food.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.wigth, self.height):
                finish = True

            # update player movement
            self.rect.x += dx
            self.rect.y += dy

        # draw player
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return finish

    def reset(self, x, y):
        self.image_right = []
        self.image_left = []
        self.image_up = []
        self.image_down = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img_right = pygame.image.load(f'image/pacman{num}.png')
            img_right = pygame.transform.scale(img_right, (tile_size, tile_size))
            img_left = pygame.transform.flip(img_right, True, False)
            img_up = pygame.transform.rotate(img_right, 90)
            img_down = pygame.transform.rotate(img_right, 270)
            self.image_right.append(img_right)
            self.image_left.append(img_left)
            self.image_up.append(img_up)
            self.image_down.append(img_down)
        self.image = self.image_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.wigth = self.image.get_width()
        self.height = self.image.get_height()
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.direction = 0


class Food():
    def __init__(self, x, y):
        self.move = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f'image/food{num}.png')
            img_right = pygame.transform.scale(img_right, (tile_size, tile_size))
            img_left = pygame.transform.flip(img_right, True, False)
            self.move.append(img_right)
            self.move.append(img_left)
        self.img = self.move[self.index]
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 0

    def update(self):
        move_cooldown = 30

        # animation
        self.counter += 1
        if self.counter >= move_cooldown:
            self.counter = 0
            if self.index >= len(self.move):
                self.index = 0
            self.img = self.move[self.index]
            self.index += 1

        if not finish:
            screen.blit(self.img, self.rect)


class World():

    def __init__(self, data):
        self.tile_list = []
        self.pacman_place = []
        self.food_place = []

        # load_image
        block_img = pygame.image.load('image/block.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    rect = img.get_rect()
                    rect.x = col_count * tile_size
                    rect.y = row_count * tile_size
                    tile = (img, rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    self.pacman_place.append(col_count * tile_size)
                    self.pacman_place.append(row_count * tile_size)
                if tile == 3:
                    self.food_place.append(col_count * tile_size)
                    self.food_place.append(row_count * tile_size)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


# make objects
world_data = World_maker()
world = World(world_data.data)
food = Food(world.pacman_place[0], world.pacman_place[1])
player = Player(world.food_place[0], world.food_place[1])

# creat buttons
restart_button = Button(screen_width // 2 - 50, screen_hight // 2 - 50, restart_image)

run = True

while run:

    clock.tick(fps)
    screen.blit(bg_img, (0, 0))

    # draw
    world.draw()
    food.update()
    finish = player.update(finish)

    if finish:
        if restart_button.draw():
            player = Player(world.food_place[0], world.food_place[1])
            finish = not finish

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
