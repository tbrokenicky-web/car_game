
import pygame
import time
import math


pygame.init()

# the screen amd soze
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Car Game")

#car image and it collison mask image

car_red = pygame.image.load("carcolors/car_no_bg.png")
car_red = pygame.transform.scale(car_red, (25, 50))
car_collision = pygame.image.load("car_collision.png")
car_collision = pygame.transform.scale(car_collision, (20,45))
car_blue = pygame.image.load("carcolors/car_blue_no_bg.png")
car_blue = pygame.transform.scale(car_blue, (25, 50))
car_green = pygame.image.load("carcolors/car_green_no_bg.png")
car_green = pygame.transform.scale(car_green, (25, 50))
car_yellow = pygame.image.load("carcolors/car_yellow_no_bg.png")
car_yellow = pygame.transform.scale(car_yellow, (25, 50))
car_red_hover = pygame.image.load("carcolors/swatch_red_hover.png")
car_red_hover = pygame.transform.scale(car_red_hover, (80, 80))
car_blue_hover = pygame.image.load("carcolors/swatch_blue_hover.png")
car_blue_hover = pygame.transform.scale(car_blue_hover, (80, 80))
car_green_hover = pygame.image.load("carcolors/swatch_green_hover.png")
car_green_hover = pygame.transform.scale(car_green_hover, (80, 80))
car_yellow_hover = pygame.image.load("carcolors/swatch_yellow_hover.png")
car_yellow_hover = pygame. transform.scale(car_yellow_hover, (80, 80))
car_red_button = pygame.image.load("carcolors/swatch_red.png")
car_red_button = pygame.transform.scale(car_red_button, (80, 80))
car_blue_button = pygame.image.load("carcolors/swatch_blue.png")
car_blue_button = pygame.transform.scale(car_blue_button, (80, 80))
car_green_button = pygame.image.load("carcolors/swatch_green.png")
car_grenn_button = pygame.transform.scale(car_green_button, (80, 80))
car_yellow_button = pygame.image.load("carcolors/swatch_yellow.png")
car_yellow_button = pygame.transform.scale(car_yellow_button, (80, 80))
car_image = car_red
# finish line and if the line is on screen
finish_line = pygame.image.load("finish_line_no_bg.png")
finish_line = pygame.transform.scale(finish_line, (100, 50))
finish_line_active = False

# start screen and the buttons
start_screen = pygame.image.load("start_screen_improved.png")
start_screen_active = True
settings_screen = pygame.image.load("settings_screen_with_back.png")
settings_screen_active = False

track1_button = pygame.image.load("buttons/track_1_button_improved.png")
track1_button = pygame.transform.scale(track1_button, (200, 80))
track1_button_hover = pygame.image.load("buttons/track_1_button_hover.png")
track1_button_hover = pygame.transform.scale(track1_button_hover, (200, 80))
settings_button = pygame.image.load("buttons/settings_button.png")
settings_button = pygame.transform.scale(settings_button, (200, 80))
settings_button_hover = pygame.image.load("buttons/settings_button_hover.png")
settings_button_hover = pygame.transform.scale(settings_button_hover, (200, 80))
reset_button = pygame.image.load("buttons/reset_button.png")
reset_button = pygame.transform.scale(reset_button, (190, 60))
reset_button_hover = pygame.image.load("buttons/reset_button_hover.png")
reset_button_hover = pygame.transform.scale(reset_button_hover, (190, 60))

exit_button = pygame.image.load("buttons/exit_button.png")
exit_button = pygame.transform.scale(exit_button, (100, 40))
exit_button_active = False

track2_button = pygame.image.load("buttons/track_2_button_improved.png")
track2_button = pygame.transform.scale(track2_button, (200, 80))
track2_button_hover = pygame.image.load("buttons/track_2_button_hover.png")
track2_button_hover = pygame.transform.scale(track2_button_hover, (200, 80))

car_red_pv = pygame.image.load("carcolors/car_no_bg.png")
car_red_pv = pygame.transform.scale(car_red_pv, (80, 135))
car_blue_pv = pygame.image.load("carcolors/car_blue_no_bg.png")
car_blue_pv = pygame.transform.scale(car_blue_pv, (80, 135))
car_green_pv = pygame.image.load("carcolors/car_green_no_bg.png")
car_green_pv = pygame.transform.scale(car_green_pv, (80, 135))
car_yellow_pv = pygame.image.load("carcolors/car_yellow_no_bg.png")
car_yellow_pv = pygame.transform.scale(car_yellow_pv, (80, 135))
preview_car_color = car_red_pv



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
        self.angle -= 3.75
        
    #turns the angle of the car left
    def move_left(self):
        self.angle += 3.75

    
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
        
        
        
        if 220 >= mouse_pos_x >= 20 and 120 >= mouse_pos_y >= 30 and start_screen_active:
            screen.blit(settings_button_hover, (20, 30))

            if clicked:
                settings_screen_active = True
                start_screen_active = False
                clicked = False
        else:
            screen.blit(settings_button, (20, 30))
            
        high_score_text_1 = font2.render("High Score track 1: " + str(best_lap_time), True, (255, 255, 255))
        screen.blit(high_score_text_1, (800, 150))
        high_score_text_2 = font2.render("High Score track 2: " + str(best_lap_time_2), True, (255, 255, 255))
        screen.blit(high_score_text_2, (800, 450))
    
    reset_track1_text = font2.render(str(best_lap_time), True, (255, 255, 255))

    reset_track2_text = font2.render(str(best_lap_time_2), True, (255, 255, 255))
    
    if settings_screen_active:
        
        screen.blit(settings_screen, (0, 0))
        screen.blit(preview_car_color, (350, 215))
        screen.blit(reset_track1_text, (516, 480))
        screen.blit(reset_track2_text, (516, 562))
        if 620 >= mouse_pos_x >= 540 and 319 >= mouse_pos_y >= 239 and settings_screen_active:
            screen.blit(car_red_hover, (540, 239))
        else: 
            screen.blit(car_red_button, (540, 239))
        
        if 720 >= mouse_pos_x >= 640 and 319 >= mouse_pos_y >= 239 and settings_screen_active:
            screen.blit(car_blue_hover, (640, 239))
        else:
            screen.blit(car_blue_button, (640, 239))
        
        if 820 >= mouse_pos_x >= 740 and 319 >= mouse_pos_y >= 239 and settings_screen_active:
            screen.blit(car_green_hover, (740, 239))
        else:
            screen.blit(car_green_button, (740, 239))
        
        if 920 >= mouse_pos_x >= 840 and 319 >= mouse_pos_y >= 239 and settings_screen_active:
            screen.blit(car_yellow_hover, (840, 239))
        else:
            screen.blit(car_yellow_button, (840, 239))
        # track 1 reset over button
        if 940 >= mouse_pos_x >= 750 and 524 >= mouse_pos_y >= 464 and settings_screen_active:
            screen.blit(reset_button_hover, (750, 464))
        else:
            screen.blit(reset_button, (750, 464))
        
        if 940 >= mouse_pos_x >= 750 and 606 >= mouse_pos_y >= 546 and settings_screen_active:
            screen.blit(reset_button_hover, (750, 546))
        else:
            screen.blit(reset_button, (750, 546))


        

        # back button
        if 220 >= mouse_pos_x >= 20 and 110 >= mouse_pos_y >= 30 and clicked and settings_screen_active:
            
            settings_screen_active = False
            start_screen_active = True
        # red car selection
        elif 620 >= mouse_pos_x >= 540 and 319 >= mouse_pos_y >= 239 and clicked and settings_screen_active:
            car_image = car_image
            preview_car_color = car_red_pv
            
        # blue car
        elif 720 >= mouse_pos_x >= 640 and 319 >= mouse_pos_y >= 239 and clicked and settings_screen_active:
            car_image = car_blue
            preview_car_color = car_blue_pv
        # green car
        elif 820 >= mouse_pos_x >= 740 and 319 >= mouse_pos_y >= 239 and clicked and settings_screen_active:
            car_image = car_green
            preview_car_color = car_green_pv
        # yellow car
        elif 920 >= mouse_pos_x >= 840 and 319 >= mouse_pos_y >= 239 and clicked and settings_screen_active:
            car_image = car_yellow
            preview_car_color = car_yellow_pv
        # reset 1 hover
        
        # reset button track 1
        elif 940 >= mouse_pos_x >= 750 and 524 >= mouse_pos_y >= 464 and clicked and settings_screen_active:
            best_lap_time = 0
            with open("save_track1.txt", "w") as file:
                file.write(str(best_lap_time))
        # reset button track 2
        elif 940 >= mouse_pos_x >= 750 and 606 >= mouse_pos_y >= 546 and clicked and settings_screen_active:
            best_lap_time_2 = 0
            with open("save_track2.txt", "w") as file:
                file.write(str(best_lap_time_2))


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
    if not start_screen_active and not settings_screen_active:
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
                        if best_lap_time == 0 or lap_time < best_lap_time:
                            best_lap_time = round(lap_time, 3)
                            with open("save_track1.txt", "w") as file:
                                file.write(str(best_lap_time))

                    elif track2_select:
                        if best_lap_time_2 == 0 or lap_time < best_lap_time_2:
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




        
        





