import pygame

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

player = pygame.Rect(400, 300, 50, 50)
enemy1 = pygame.Rect(200, 200, 50, 50)
enemy2 = pygame.Rect(600, 200, 50, 50)
current_target = enemy1
walls = [pygame.Rect(350,250,100,50), pygame.Rect(500,400,150,30)]
player_speed = 5
enemy_speed = 2
camera_x, camera_y = 0, 0
camera_zoom = 1.0
lerp_speed = 0.1
zoom_min, zoom_max = 0.8, 1.5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_target = enemy2 if current_target == enemy1 else enemy1

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_w]: dy -= player_speed
    if keys[pygame.K_s]: dy += player_speed
    if keys[pygame.K_a]: dx -= player_speed
    if keys[pygame.K_d]: dx += player_speed

    player.move_ip(dx, 0)
    for wall in walls:
        if player.colliderect(wall):
            player.move_ip(-dx, 0)
    player.move_ip(0, dy)
    for wall in walls:
        if player.colliderect(wall):
            player.move_ip(0, -dy)

    for enemy in [enemy1, enemy2]:
        if enemy == current_target:
            dx_e = player.centerx - enemy.centerx
            dy_e = player.centery - enemy.centery
            dist_e = (dx_e**2 + dy_e**2)**0.5
            if dist_e != 0:
                enemy.move_ip(dx_e/dist_e*enemy_speed, dy_e/dist_e*enemy_speed)
            for wall in walls:
                if enemy.colliderect(wall):
                    enemy.move_ip(-dx_e/dist_e*enemy_speed, -dy_e/dist_e*enemy_speed)

    cam_target_x = (player.centerx + current_target.centerx)//2 - screen_width//2
    cam_target_y = (player.centery + current_target.centery)//2 - screen_height//2
    camera_x += (cam_target_x - camera_x) * lerp_speed
    camera_y += (cam_target_y - camera_y) * lerp_speed

    dist = ((player.centerx - current_target.centerx)**2 + (player.centery - current_target.centery)**2)**0.5
    if dist < 1:
        dist = 1
    target_zoom = max(min(300/dist, zoom_max), zoom_min)
    camera_zoom += (target_zoom - camera_zoom) * lerp_speed

    screen.fill((30, 30, 30))

    def draw_rect(rect, color):
        offset_rect = pygame.Rect((rect.x - camera_x) * camera_zoom,
                                  (rect.y - camera_y) * camera_zoom,
                                  rect.width * camera_zoom,
                                  rect.height * camera_zoom)
        pygame.draw.rect(screen, color, offset_rect)

    draw_rect(player, (0, 0, 255))
    draw_rect(enemy1, (255, 0, 0))
    draw_rect(enemy2, (0, 255, 0))
    for wall in walls:
        draw_rect(wall, (100, 100, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
