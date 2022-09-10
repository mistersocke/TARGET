import pygame
from sys import exit

# pygame imports
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

start_screen = pygame.image.load("graphics/start_screen3.png")
background = pygame.image.load("graphics/background_entwurf2.png")
game_active = False

bg_music = pygame.mixer.Sound("graphics/bg_music.mp3")
bg_music.play(-1)


class NameBanner:
    font = pygame.font.Font("graphics/Thintel.ttf", 270)
    surface = font.render("TARGET", False, (255, 0, 0))
    rect = surface.get_rect(center=(955, 210))

    outline_font = pygame.font.Font("graphics/Thintel.ttf", 283)
    outline_surface = outline_font.render("TARGET", False, (0, 0, 0))
    outline_rect = outline_surface.get_rect(center=(955, 211))


class HighScoreBanner:
    high_score_txt = open("high score.txt", "r")
    read_it = high_score_txt.read()

    font = pygame.font.Font("graphics/Thintel.ttf", 230)
    surface = font.render(f"High Score: {read_it}", False, (255, 70, 0))
    rect = surface.get_rect(center=(955, 420))

    outline_font = pygame.font.Font("graphics/Thintel.ttf", 234)
    outline_surface = outline_font.render(f"High Score: {read_it}", False, (0, 0, 0))
    outline_rect = outline_surface.get_rect(center=(955, 420))

    high_score_txt.close()


class Arrow:
    animation_count = 0
    frame = pygame.image.load("graphics/arrow.png")
    x = 100
    y = 100
    rect = frame.get_rect(center=(x, y))
    shoot = False
    number = 3  # score ginge auch
    do_it_once = 0
    count_till_shoot = 0
    calculate_number = False
    animation = False
    shoot_sound = pygame.mixer.Sound("graphics/shoot sound.mp3")
    shoot_sound.set_volume(0.1)


class Player:
    frame1 = pygame.image.load("graphics/player_frame1.png")
    frame2 = pygame.image.load("graphics/player_frame2.png")
    frame3 = pygame.image.load("graphics/player_frame3.png")
    frame4 = pygame.image.load("graphics/player_frame4.png")
    frame5 = pygame.image.load("graphics/player_frame5.png")
    frame6 = pygame.image.load("graphics/player_frame6.png")
    frame_list = [frame2, frame3, frame4, frame5, frame6, frame1]
    index = 0
    current_frame = frame1
    speed = 4
    x = 500
    y = 1080
    rect = frame1.get_rect(midbottom=(x, y))


class Score:
    font = pygame.font.Font("graphics/Thintel.ttf", 150)
    surface = font.render(f"Score: {Arrow.number}", False, (25, 149, 213))
    rect = surface.get_rect(center=(955, 200))


class Target:
    points = 0
    yellow_target = pygame.image.load("graphics/yellow_target3.png")
    red_target = pygame.image.load("graphics/red_target3.png")
    blue_target = pygame.image.load("graphics/blue_target3.png")
    black_target = pygame.image.load("graphics/black_target3.png")

    black_rect1 = black_target.get_rect(topright=(1920, 180))
    blue_rect1 = blue_target.get_rect(topright=(1920, 330))
    red_rect1 = red_target.get_rect(topright=(1920, 430))
    yellow_rect = yellow_target.get_rect(topright=(1920, 500))
    red_rect2 = red_target.get_rect(topright=(1920, 560))
    blue_rect2 = blue_target.get_rect(topright=(1920, 630))
    black_rect2 = black_target.get_rect(topright=(1920, 730))

    plus_sound = pygame.mixer.Sound("graphics/hit_plus_target.mp3")
    plus_sound.set_volume(0.1)
    minus_sound = pygame.mixer.Sound("graphics/hit_minus_target.mp3")
    minus_sound.set_volume(0.1)


while True:
    for event in pygame.event.get():  # anderer quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:  # esc quit
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            if event.key == pygame.K_SPACE and game_active and Arrow.count_till_shoot == 0:
                Arrow.rect = Arrow.frame.get_rect(center=(Arrow.x, Arrow.y))
                Arrow.animation = True
                Arrow.shoot = True

    if game_active:
        screen.blit(background, (0, 0))
        screen.blit(Score.surface, Score.rect)

        screen.blit(Target.black_target, Target.black_rect1)
        screen.blit(Target.blue_target, Target.blue_rect1)
        screen.blit(Target.red_target, Target.red_rect1)
        screen.blit(Target.yellow_target, Target.yellow_rect)
        screen.blit(Target.red_target, Target.red_rect2)
        screen.blit(Target.blue_target, Target.blue_rect2)
        screen.blit(Target.black_target, Target.black_rect2)

        Player.rect = Player.current_frame.get_rect(midbottom=(Player.x, Player.y))
        screen.blit(Player.current_frame, Player.rect)

        # player movement
        Player.y += Player.speed
        if Player.y >= 1080:
            Player.y = 1080
            Player.speed *= -1
            Player.speed -= 0.4
        if Player.y <= 200:
            Player.y = 200
            Player.speed *= -1
            Player.speed += 0.4

        if Arrow.animation:
            Arrow.animation_count += 1
            if Arrow.animation_count == 7:
                Player.index += 1
                Player.current_frame = Player.frame_list[Player.index]
                Arrow.animation_count = 0
                if Player.index >= 5:
                    Player.index = 0
                    Arrow.animation = False
                    Arrow.shoot = True
                    Arrow.shoot_sound.play()

        if Arrow.shoot:
            Arrow.count_till_shoot += 1
            if Arrow.count_till_shoot >= 35:
                Arrow.rect = Arrow.frame.get_rect(center=(Arrow.x, Arrow.y))
                screen.blit(Arrow.frame, Arrow.rect)
                Arrow.x += 50
                if Arrow.x >= 1950:
                    Arrow.shoot = False
                    Arrow.count_till_shoot = 0
            else:
                Arrow.x = Player.x
                Arrow.y = Player.y - 115

        # hit targets
        if Target.yellow_rect.colliderect(Arrow.rect):
            Target.points = 2
            Arrow.calculate_number = True
        elif Target.red_rect1.colliderect(Arrow.rect) or Target.red_rect2.colliderect(Arrow.rect):
            Target.points = 0.5
            Arrow.calculate_number = True
        elif Target.blue_rect1.colliderect(Arrow.rect) or Target.blue_rect2.colliderect(Arrow.rect):
            Target.points = -1
            Arrow.calculate_number = True
        elif Target.black_rect1.colliderect(Arrow.rect) or Target.black_rect2.colliderect(Arrow.rect):
            Target.points = -2
            Arrow.calculate_number = True
        elif Arrow.x > 1630 and (Arrow.y < 180 or Arrow.y > 880):  # daneben
            Target.points = -3
            Arrow.calculate_number = True
        else:
            Arrow.calculate_number = False

        if Arrow.calculate_number:
            if Arrow.do_it_once == 0:
                if Target.points > 0:
                    Target.plus_sound.play()
                elif Target.points < 0:
                    Target.minus_sound.play()
                Arrow.number += Target.points
                Score.surface = Score.font.render(f"Score: {Arrow.number}", False, (25, 149, 213))
                high_score_txt = open("high score.txt", "r")
                read_it = high_score_txt.read()
                high_score_txt.close()
                if Arrow.number > float(read_it):
                    high_score_txt = open("high score.txt", "w")
                    high_score_txt.write(str(Arrow.number))
                    high_score_txt.close()
            Arrow.do_it_once += 1  # nur dazu da, dass die aktion oben nur einmal passiert
        else:
            Arrow.do_it_once = 0
            Target.points = 0
        if Arrow.number <= 0:
            game_active = False

    else:
        screen.blit(start_screen, (0, 0))
        screen.blit(NameBanner.outline_surface, NameBanner.outline_rect)
        screen.blit(NameBanner.surface, NameBanner.rect)
        high_score_txt = open("high score.txt", "r")
        read_it = high_score_txt.read()
        high_score_txt.close()
        HighScoreBanner.surface = HighScoreBanner.font.render(f"High Score: {read_it}", False, (255, 70, 0))
        HighScoreBanner.outline_surface = HighScoreBanner.outline_font.render(f"High Score: {read_it}", False, (0, 0, 0))
        screen.blit(HighScoreBanner.outline_surface, HighScoreBanner.outline_rect)
        screen.blit(HighScoreBanner.surface, HighScoreBanner.rect)

        keys = pygame.key.get_pressed()
        if not keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
            for i in keys:
                if i:
                    game_active = True
                    Arrow.number = 10
                    Score.surface = Score.font.render(f"Score: {Arrow.number}", False, (25, 149, 213))
                    Player.speed = 4
                    Player.index = 0
                    Player.current_frame = Player.frame1
                    Player.speed = 4
                    Player.x = 500
                    Player.y = 1080
                    Player.rect = Player.frame1.get_rect(midbottom=(Player.x, Player.y))
                    Arrow.shoot = False
                    Arrow.animation = False
                    Arrow.count_till_shoot = 0

    pygame.display.update()
    clock.tick(60)
