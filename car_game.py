
import pygame
import time
import math


pygame.init()

# the screen amd soze
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Car Game")

#car image and it collison mask image
car_image = pygame.image.load("car_no_bg.png")
car_image = pygame.transform.scale(car_image, (25, 50))
car_collision = pygame.image.load("car_collision.png")
car_collision = pygame.transform.scale(car_collision, (20,45))

# finish line and if the line is on screen
finish_line = pygame.image.load("finish_line_no_bg.png")
finish_line = pygame.transform.scale(finish_line, (100, 50))
finish_line_active = False

# start screen and the buttons
start_screen = pygame.image.load("start_screen_improved.png")
start_screen_active = True
track1_button = pygame.image.load("buttons/track_1_button_improved.png")
track1_button = pygame.transform.scale(track1_button, (200, 80))
track1_button_hover = pygame.image.load("buttons/track_1_button_hover.png")
track1_button_hover = pygame.transform.scale(track1_button_hover, (200, 80))

exit_button = pygame.image.load("buttons/exit_button.png")
exit_button = pygame.transform.scale(exit_button, (100, 40))
exit_button_active = False

track2_button = pygame.image.load("buttons/track_2_button_improved.png")
track2_button = pygame.transform.scale(track2_button, (200, 80))
track2_button_hover = pygame.image.load("buttons/track_2_button_hover.png")
track2_button_hover = pygame.transform.scale(track2_button_hover, (200, 80))



#tracks and their masks for collison
track = pygame.image.load("track_improved.png")
track1_select = False
track_collision = pygame.image.load("Better_collision_track.png").convert()
track2 = pygame.image.load("track2_improved.png")
track2_select = False
track2_collision = pygame.image.load("track2_collision.png").convert()
grass_mask1 = pygame.mask.from_threshold(track_collision, (255, 255, 255), (10, 10, 10, 255) )
grass_mask2 = pygame.mask.from_threshold(track2_collision, (255, 255, 255), (10, 10, 10, 255) )

# if the car is visable
car_visable = False

try:
    with open("save_track1.txt", "r") as file:
        best_lap_time = float(file.read())
except FileNotFoundError:
    best_lap_time = 0


try:
    with open("save_track2.txt", "r") as file:
        best_lap_time_2 = float(file.read())
except FileNotFoundError:
    best_lap_time_2 = 0



#class for the car with all the cariables
class car:
    
    # all of hte inital variables for the car
    def __init__(self):
        
        self.speed = 0
        self.acceloration = 2
        self.angle = 0
        self.x = 125
        self.y = 500
    
    # how the car accelorates
    def accelorate_car(self):
        self.speed += self.acceloration

        if self.speed > 5:
            self.speed = 5
        if self.speed < -5:
            self.speed = -5
    
    # how the can slowes down
    def brake_car(self):
        if self.speed > 0:
            self.speed -= 0.2
            if self.speed < 0:
                self.speed = 0
        if self.speed < 0:
            self.speed += 0.2
            if self.speed > 0:
                self.speed = 0
    
    # this is just if i wanna add the car going backwards 
    def drive_backwards(self):
        radians = math.radians(self.angle)
        self.x += math.sin(radians) * self.speed
        self.y += math.cos(radians) * self.speed
    
    # how the car drives forward so that it folows the angle the car is facing
    def drive_forward(self):
        radians = math.radians(self.angle)
        self.x -= math.sin(radians) * self.speed
        self.y -= math.cos(radians) * self.speed
    
    # turn the angle of the far right
    def move_right(self):
        self.angle -= 4
        
    #turns the angle of the car left
    def move_left(self):
        self.angle += 4
    

# creates a car from the class
my_car = car()

# if the car has crossed the finish line
crossed_line = False

# hold all the past lap times
lap_time_list = []

# starting lap time
last_lap_time = 0

# starts the clock for fps so the screen updates ever 60 seconds
clock = pygame.time.Clock()

lap_time = 0

# gets time at the start
start_time = time.time()

# this is the game loop
while True:
    clicked = False
    screen.fill((0, 0, 0))
    
    # so that the x works on your screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        # so that if the mouse is put don it changes the clicked to true
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True
    
    # gets the position of your mouse      
    mouse_pos = pygame.mouse.get_pos()
   
    # take the positions out of the list
    mouse_pos_x = mouse_pos[0]
    mouse_pos_y = mouse_pos[1]
    
    font2 = pygame.font.SysFont("Arial", 15)


    # the start screen
    if start_screen_active:
        screen.blit(start_screen, (0, 0))
        if 220 >= mouse_pos_x >= 20 and 530 >= mouse_pos_y >= 450 and start_screen_active:
            screen.blit(track1_button_hover, (20, 450))
        else:
            screen.blit(track1_button, (20, 450))
        
        if 220 >= mouse_pos_x >= 20 and 650 >= mouse_pos_y >= 570 and start_screen_active:
            screen.blit(track2_button_hover, (20, 570))
        else:
            screen.blit(track2_button, (20, 570))
        
        high_score_text_1 = font2.render("High Score track 1: " + str(best_lap_time), True, (255, 255, 255))
        screen.blit(high_score_text_1, (800, 150))
        high_score_text_2 = font2.render("High Score track 2: " + str(best_lap_time_2), True, (255, 255, 255))
        screen.blit(high_score_text_2, (800, 450))
    # this is basicly the hit box for the 1st track button
   
    if 220 >= mouse_pos_x >= 20 and 530 >= mouse_pos_y >= 450 and clicked and start_screen_active:
        start_time = time.time()
        track1_select = True
        track2_select = False
        car_visable = True
        finish_line_active = True
        start_screen_active = False
        exit_button_active = True
        lap_time_list = []
    
    
    # this is the hit box for the second track button
    elif 220 >= mouse_pos_x >= 20 and 650 >= mouse_pos_y >= 570 and clicked and start_screen_active:
        # all of these change so that the track shows up
        start_time = time.time()
        track2_select = True
        car_visable = True
        finish_line_active = True
        track1_select = False
        start_screen_active = False
        exit_button_active = True
        lap_time_list = []
    if 400 >= mouse_pos_x >= 0 and 100 >= mouse_pos_y >= 0 and clicked and track1_select:
        
        track1_select = False
        track2_select = False
        car_visable = False
        finish_line_active = False
        start_screen_active = True
        exit_button_active = False
        my_car.x = 125
        my_car.y = 500
        my_car.angle = 0
    elif 400 >= mouse_pos_x >= 0 and 100 >= mouse_pos_y >= 0 and clicked and track2_select:
        track2_select = False
        track1_select = False
        car_visable = False
        finish_line_active = False
        start_screen_active = True
        exit_button_active = False
        my_car.x = 125
        my_car.y = 500
        my_car.angle = 0
        lap_time_list = []
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
    
    if exit_button_active:
        screen.blit(exit_button, (0, 0))

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
                
                
                
                if lap_time >= 5:
                    if track1_select:
                        if lap_time < best_lap_time:
                            best_lap_time = round(lap_time, 3)
                            with open("save_track1.txt", "w") as file:
                                file.write(str(best_lap_time))

                    elif track2_select:
                        if lap_time < best_lap_time_2:
                            best_lap_time_2 = round(lap_time, 3)
                            with open("save_track2.txt", "w") as file:
                                file.write(str(best_lap_time_2))
                    
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




        
        





