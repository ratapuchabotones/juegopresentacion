import pygame, random, json

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

def load_high_score(filename="score.json"):
    try:
        with open(filename, 'r') as file:
            data = file.read().strip()
            if not data:
                return 0
            return json.loads(data).get("high_score", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_high_score(high_score, filename="score.json"):
    data = {"high_score": high_score}
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        pass

class Player(GameObject):
    def __init__(self, x, y):
        image = pygame.image.load("assets/player.png").convert()
        image.set_colorkey(BLACK)
        super().__init__(image, x, y)
        self.speed_x = 0
        self.shield = 100
        self.bullet_comp = Bullet(self.rect.centerx, self.rect.top)

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speed_x = -5
        if keystate[pygame.K_d]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        self.bullet_comp = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(self.bullet_comp)
        bullets.add(self.bullet_comp)
        laser_sound.play()

class Meteor(GameObject):
    def __init__(self, x, y):
        image = random.choice(meteor_images)
        image.set_colorkey(BLACK)
        super().__init__(image, x, y)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 22:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(1, 8)

class Bullet(GameObject):
    def __init__(self, x, y):
        image = pygame.image.load("assets/laser1.png")
        image.set_colorkey(BLACK)
        super().__init__(image, x, y)
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(GameObject):
    def __init__(self, center):
        image = explosion_anim[0]
        super().__init__(image, center[0], center[1])
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, [0, 0])
    draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT / 4)
    draw_text(screen, "(Instructions)", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press key to begin", 17, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

meteor_images = [pygame.image.load(img).convert() for img in [
    "assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png",
    "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png"
]]

explosion_anim = [pygame.transform.scale(pygame.image.load(f"assets/regularExplosion0{i}.png").convert_alpha(), (70, 70))
                  for i in range(9)]

background = pygame.image.load("assets/background.png").convert()
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/starwars.mp3")
pygame.mixer.music.set_volume(4)
pygame.mixer.music.play(loops=-1)

high_score = load_high_score()
game_over = True
running = True

while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player(WIDTH // 2, HEIGHT - 10)
        all_sprites.add(player)

        for _ in range(8):
            meteor = Meteor(random.randrange(WIDTH - 50), random.randrange(-100, -40))
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 0

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()

    all_sprites.update()

    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor(random.randrange(WIDTH - 50), random.randrange(-100, -40))
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 25
        meteor = Meteor(random.randrange(WIDTH - 50), random.randrange(-100, -40))
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True
            if score > high_score:
                high_score = score
                save_high_score(high_score)

    screen.blit(background, [0, 0])
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {score}", 25, WIDTH // 2, 10)
    draw_text(screen, f"High Score: {high_score}", 25, WIDTH // 2, 40)
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()

pygame.quit()
