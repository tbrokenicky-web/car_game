
import pygame
import time
import math


pygame.init()


screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Car Game")

car_image = pygame.image.load("car_no_bg.png")
car_image = pygame.transform.scale(car_image, (25, 50))
car_collision = pygame.image.load("car_collision.png")
car_collision = pygame.transform.scale(car_collision, (20,45))

finish_line = pygame.image.load("finish_line_no_bg.png")
finish_line = pygame.transform.scale(finish_line, (100, 50))
finish_line_active = False

start_screen = pygame.image.load("start_screen.png")
start_screen_active = True
track1_button = pygame.image.load("track_1_button.png")
track1_button = pygame.transform.scale(track1_button, (100, 20))
track2_button = pygame.image.load("track_2_button.png")
track2_button = pygame.transform.scale(track2_button, (100, 20))

track = pygame.image.load("track.png")
track1_select = False
track_collision = pygame.image.load("Better_collision_track.png").convert()
track2 = pygame.image.load("track2.png")
track2_select = False
track2_collision = pygame.image.load("track2_collision.png").convert()
grass_mask1 = pygame.mask.from_threshold(track_collision, (255, 255, 255), (10, 10, 10, 255) )
grass_mask2 = pygame.mask.from_threshold(track2_collision, (255, 255, 255), (10, 10, 10, 255) )

car_visable = False
class car:
    def __init__(self):
    
        self.speed = 0
        self.acceloration = 2
        self.brake_time = 0
        self.bounce = 0.5
        self.angle = 0
        self.x = 125
        self.y = 500
      
    def accelorate_car(self):
        
        self.speed += self.acceloration

        if self.speed > 5:
            self.speed = 5
        if self.speed < -5:
            self.speed = -5
    def brake_car(self):
        if self.speed > 0:
            self.speed -= 0.2
            if self.speed < 0:
                self.speed = 0
        if self.speed < 0:
            self.speed += 0.2
            if self.speed > 0:
                self.speed = 0
        
    def drive_backwards(self):
        radians = math.radians(self.angle)
        self.x += math.sin(radians) * self.speed
        self.y += math.cos(radians) * self.speed
        
    def drive_forward(self):
        radians = math.radians(self.angle)
        self.x -= math.sin(radians) * self.speed
        self.y -= math.cos(radians) * self.speed
    
    def move_right(self):
        self.angle -= 4
        
    
    def move_left(self):
        self.angle += 4
    


my_car = car()

crossed_line = False

lap_time_list = []

last_lap_time = 0

clock = pygame.time.Clock()

lap_time = 0
# gets time at the start
start_time = time.time()
while True:
    clicked = False
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True
            
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos_x = mouse_pos[0]
    mouse_pos_y = mouse_pos[1]
    
    if start_screen_active:
        screen.blit(start_screen, (0, 0))
        screen.blit(track1_button, (20, 450))
        screen.blit(track2_button, (20, 570))
    if 420 >= mouse_pos_x >= 20 and 470 >= mouse_pos_y >= 450 and clicked and start_screen_active:
        track1_select = True
        track2_select = False
        car_visable = True
        finish_line_active = True
        start_screen_active = False
    elif 420 >= mouse_pos_x >= 20 and 590 >= mouse_pos_y >= 570 and clicked and start_screen_active:
        track2_select = True
        car_visable = True
        finish_line_active = True
        track1_select = False
        start_screen_active = False
    lap_time = int(time.time() - start_time) 
    
    grass_mask = grass_mask1
    if track2_select:
        grass_mask = grass_mask2
        current_track = track2
    elif track1_select:
        grass_mask = grass_mask1
        current_track = track
    if not start_screen_active:
        screen.blit(current_track, (0, 0))
    
    

    font = pygame.font.SysFont("Arial", 30)
    font2 = pygame.font.SysFont("Arial", 15)
    text = font.render("Lap Time: " + str(lap_time), True, (0, 0, 0))
    
    mouse_pos = pygame.mouse.get_pos()
    
    
    screen.blit(text, (1000, 20))
    if finish_line_active:
        screen.blit(finish_line, (80, 400))
    
    for i in range(len(lap_time_list)):
        lap_time_text = font2.render("lap:" + str(i + 1) + " " + str(lap_time_list[i]), True, (0, 0, 0))
        screen.blit(lap_time_text, (1100, 50 + i * 20))
    keys = pygame.key.get_pressed()
    
    old_x = my_car.x
    old_y = my_car.y
    
    if keys[pygame.K_UP]:
        my_car.accelorate_car()
        my_car.drive_forward()
    else:
        my_car.brake_car()
    
    if keys[pygame.K_DOWN]:
        my_car.drive_backwards()
    
    if keys[pygame.K_LEFT]:
        my_car.move_left()
    
    if keys[pygame.K_RIGHT]:
        my_car.move_right()
    

    if car_visable == True:
        rotate_car = pygame.transform.rotate(car_image, (my_car.angle))
        car_rect = rotate_car.get_rect(center= (my_car.x, my_car.y))
        
        rotate_collision = pygame.transform.rotate(car_collision, (my_car.angle))
        collision_rect = rotate_collision.get_rect(center= (my_car.x, my_car.y))
        car_mask = pygame.mask.from_threshold(rotate_collision, (0, 0, 0), (10, 10, 10, 255))
        

        
        offset = collision_rect.topleft
        


        if 180 >= my_car.x >= 80 and 450 >= my_car.y >= 400:
            # if it hasent happend
            if not crossed_line:
                total_time = time.time() - start_time

                lap_time = total_time - last_lap_time

                lap_time_list.append(round(lap_time, 3))
                crossed_line = True
                last_lap_time = total_time

        else:
            crossed_line = False
        
        if grass_mask.overlap(car_mask, offset) is not None:
            
            
            my_car.x = old_x 
            my_car.y = old_y  
            my_car.speed = 0
        
          
        screen.blit(rotate_car, car_rect)

    pygame.display.flip()

    clock.tick(60)




        
        





