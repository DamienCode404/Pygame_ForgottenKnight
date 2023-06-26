import pygame
pygame.init()

# Dimensions de la fenêtre de l'utilisateur pour ajuster la résolution
info = pygame.display.Info()
FULLSCREEN_WIDTH = info.current_w
FULLSCREEN_HEIGHT = info.current_h

# Création de la fenêtre
screen = pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT))
pygame.display.set_caption("Forgotten Knight")

# Variables pour gérer le mode plein écran
fullscreen = False
fullscreen_mode = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN

# Ajout du Background
BACKGROUND_1 = pygame.image.load("assets/img/Background.png")
BACKGROUND = pygame.transform.scale(
    BACKGROUND_1, (FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT))

# Dimensions des frames spritesheet
FRAME_WIDTH = 120
FRAME_HEIGHT = 80

# Redimensionner le personnage in game
RENDER_WIDTH = 800
RENDER_HEIGHT = 600

# Chargement des feuilles de sprites
Idle_spritesheet = pygame.image.load("assets/animation/_Idle.png")
Attack_spritesheet = pygame.image.load("assets/animation/_Attack.png")
Death_spritesheet = pygame.image.load("assets/animation/_Death.png")
Hit_spritesheet = pygame.image.load("assets/animation/_Hit.png")
Run_spritesheet = pygame.image.load("assets/animation/_Run.png")
TurnAround_spritesheet = pygame.image.load("assets/animation/_TurnAround.png")
Jump_spritesheet = pygame.image.load("assets/animation/_Jump.png")
Roll_spritesheet = pygame.image.load("assets/animation/_Roll.png")

# Découpage des Idle_frames
Idle_frames = []
for i in range(10):
    x = i * FRAME_WIDTH
    y = 0
    frame = Idle_spritesheet.subsurface(
        pygame.Rect(x, y, FRAME_WIDTH, FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (RENDER_WIDTH, RENDER_HEIGHT))
    Idle_frames.append(frame)

# Découpage des Attack_frames
Attack_frames = []
for i in range(4):
    x = i * FRAME_WIDTH
    y = 0
    frame = Attack_spritesheet.subsurface(
        pygame.Rect(x, y, FRAME_WIDTH, FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (RENDER_WIDTH, RENDER_HEIGHT))
    Attack_frames.append(frame)

# Découpage des Death_frames
Death_frames = []
for i in range(10):
    x = i * FRAME_WIDTH
    y = 0
    frame = Death_spritesheet.subsurface(
        pygame.Rect(x, y, FRAME_WIDTH, FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (RENDER_WIDTH, RENDER_HEIGHT))
    Death_frames.append(frame)

# Découpage des Hit_frames
Hit_frames = []
for i in range(1):
    x = i * FRAME_WIDTH
    y = 0
    frame = Hit_spritesheet.subsurface(
        pygame.Rect(x, y, FRAME_WIDTH, FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (RENDER_WIDTH, RENDER_HEIGHT))
    Hit_frames.append(frame)

# Découpage des Run_frames
Run_frames = []
for i in range(10):
    x = i * FRAME_WIDTH
    y = 0
    frame = Run_spritesheet.subsurface(
        pygame.Rect(x, y, FRAME_WIDTH, FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (RENDER_WIDTH, RENDER_HEIGHT))
    Run_frames.append(frame)

# Découpage des Idle_frames
TurnAround_frames = []
for i in range(3):
    x = i * FRAME_WIDTH
    y = 0
    frame = TurnAround_spritesheet.subsurface(
        pygame.Rect(x, y, FRAME_WIDTH, FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (RENDER_WIDTH, RENDER_HEIGHT))
    TurnAround_frames.append(frame)

# Découpage des Roll_frames
Jump_frames = []
for i in range(3):
    x = i * FRAME_WIDTH
    y = 0
    frame = Jump_spritesheet.subsurface(
        pygame.Rect(x, y, FRAME_WIDTH, FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (RENDER_WIDTH, RENDER_HEIGHT))
    Jump_frames.append(frame)

# Découpage des Roll_frames
Roll_frames = []
for i in range(12):
    x = i * FRAME_WIDTH
    y = 0
    frame = Roll_spritesheet.subsurface(
        pygame.Rect(x, y, FRAME_WIDTH, FRAME_HEIGHT))
    frame = pygame.transform.scale(frame, (RENDER_WIDTH, RENDER_HEIGHT))
    Roll_frames.append(frame)


# Classe pour le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.attacking = False
        self.Idle_frames = Idle_frames
        self.current_frame = 0
        self.image = self.Idle_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = FULLSCREEN_WIDTH // 2
        self.rect.y = FULLSCREEN_HEIGHT // 2
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        if not self.attacking or not self.run:
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y
            self.image = Idle_frames[self.current_frame]  # Animation Idle
            self.current_frame = (self.current_frame + 1) % len(Idle_frames)
        else:
            self.current_frame += 1
            if self.current_frame >= len(Attack_frames):
                self.current_frame = 0
                self.attacking = False
            self.image = Attack_frames[self.current_frame] # Animation d'attaque

    def move_left(self):
        self.velocity_x = -20

    def move_right(self):
        self.velocity_x = 20

    def stop_moving(self):
        self.velocity_x = 0

    def attack(self):
        self.attacking = True
        self.current_frame = 0

    def run(self):
        self.run = True
        self.current_frame = 0

# Création d'une instance du joueur
player = Player()

# Gestion de la boucle de jeu
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
            player.attack()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.move_right()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_LEFT or event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.stop_moving()

    # Mise à jour du joueur
    player.update()

    # Affichage
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(player.image, player.rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("Game closed")