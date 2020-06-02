import pygame
import random
import math

display_width = 800
display_height = 600

#initialize all imported pygame modules
pygame.init()

paths = [display_width * (1 / 6), display_width * (2 / 6), display_width * (3 / 6),
         display_width * (4 / 6), display_width * (5 / 6)]

def initialise_game_display():

    global Button_Click
    Button_Click = pygame.mixer.Sound("./Audio/Button_Click.wav")

    global Game_Over_Sound
    Game_Over_Sound = pygame.mixer.Sound("./Audio/Game_Over.wav")

    pygame.mixer.music.load("./Audio/Theme.wav")
    pygame.mixer.music.set_volume(0.1)

    pygame.mixer.music.play(-1)
    
    #print(pygame.mixer.music.get_volume())

    #Initialize a window or screen for display
    global game_display
    game_display = pygame.display.set_mode((display_width, display_height))

    #Set the current window caption
    pygame.display.set_caption("Meteorite Madness!")

    #Create an object to help track time
    global clock
    clock = pygame.time.Clock()

    Import = pygame.image.load

    #lists of sprites
    global meteorites_imgs
    meteorites_imgs = [Import("./Obstacles/Meteorites/Meteorite1 - 1.png").convert_alpha(),Import("./Obstacles/Meteorites/Meteorite1 - 2.png").convert_alpha(),
                      Import("./Obstacles/Meteorites/Meteorite1 - 3.png").convert_alpha(),Import("./Obstacles/Meteorites/Meteorite1 - 4.png").convert_alpha(),
                      Import("./Obstacles/Meteorites/Meteorite2 - 1.png").convert_alpha(),Import("./Obstacles/Meteorites/Meteorite2 - 2.png").convert_alpha(),
                      Import("./Obstacles/Meteorites/Meteorite2 - 3.png").convert_alpha(),Import("./Obstacles/Meteorites/Meteorite1 - 4.png").convert_alpha()]

    global sound_mute
    sound_mute = False
    
    global background_imgs
    background_imgs = [Import("./UI/SpaceBackground.png").convert_alpha()]

    global logo_img
    logo_img = (Import("./UI/MeteoriteMadnessLogo.png").convert_alpha())

    global rank_img
    rank_img = (Import("./UI/Rank_Block.png").convert_alpha())

    global button_imgs
    button_imgs = [Import("./UI/Button_idle.png").convert_alpha(),
                   Import("./UI/Button_hovering.png").convert_alpha(),
                   Import("./UI/Button_pressed.png").convert_alpha()]

    global mute_imgs
    mute_imgs = [Import("./UI/Button_small_green.png").convert_alpha(),Import("./UI/Button_small_red.png").convert_alpha(),
                 Import("./UI/Audio_on.png").convert_alpha(),Import("./UI/Audio_off.png").convert_alpha()]

    global pause_imgs
    pause_imgs = [Import("./UI/Pause_on.png").convert_alpha(),Import("./UI/Pause_off.png").convert_alpha()]

    global mute_button
    mute_button = Mute_Button(716, 20)

#Classes
class Pause_Button():

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.paused = False
        self.state = 0
        self.imgs = []
        self.imgs.append(mute_imgs[0])
        self.imgs.append(mute_imgs[1])
        self.imgs.append(pause_imgs[0])
        self.imgs.append(pause_imgs[1])

    def Hovering(self, mouse_pos):

        if (mouse_pos[0] > self.x_pos and mouse_pos[0] < self.x_pos + 64):
            if (mouse_pos[1] > self.y_pos and mouse_pos[1] < self.y_pos + 64):
                return True

        return False

    def pause_or_unpause(self):
        
        self.paused = not self.paused
        print(self.paused)

    def Display(self):

        game_display.blit(self.imgs[self.state], (self.x_pos, self.y_pos))

        if self.paused == False:
            game_display.blit(self.imgs[3], (self.x_pos, self.y_pos))
        elif self.paused == True:
            game_display.blit(self.imgs[2], (self.x_pos, self.y_pos))
            
class Meteorite():

    def __init__(self, rotation_current, rotation_amount, path, meteorite_img, meteorite_index):
        
        self.rotation_current = rotation_current
        self.rotation_amount = rotation_amount
        self.path = path
        self.x_axis = paths[path]
        self.meteorite_img = meteorite_img
        self.meteorite_index = meteorite_index

    def __del__(self):
        print((str(self)) + " was deconstructed")

    def Meteorite_Display(self, y_axis):

        meteorite_rotated = pygame.transform.rotate(self.meteorite_img, self.rotation_current)
        center = meteorite_rotated.get_rect()
        center.center = (self.x_axis, y_axis)
        game_display.blit(meteorite_rotated, center)
        self.rotation_current += self.rotation_amount

    def Check_Collision(self, player_path, player_height, meteorite_y_current):

        if player_path == self.path:
            if (player_height < meteorite_y_current + 35) and (player_height > meteorite_y_current or player_height + 100 > meteorite_y_current):
                Game_Over()

class game_stats():

    def __init__(self, meteorite_speed = 8.0, score_multiplier = 1, rocket_health = 1,
                 met_max_speed = 14.0, player_height = 400, player_path = 2, current_score = 0,
                 met_speed_increase = 0.001):
        self.meteorite_speed = meteorite_speed
        self.score_multiplier = score_multiplier
        self.rocket_health = rocket_health
        self.player_path = player_path
        self.player_height = player_height
        self.met_max_speed = met_max_speed
        self.current_score = current_score
        self.met_speed_increase = met_speed_increase

class Rocket():

    def __init__(self, rocket_img):

        self.rocket_imgs = []

        rocket_number = "Rocket" + str(rocket_img)

        for x in range(6):
            curr_rocket = "./Rockets/"+rocket_number+"/"+rocket_number+"-"+str(x)+".png"
            temp_rocket = pygame.image.load(curr_rocket).convert_alpha()
            self.rocket_imgs.append(temp_rocket)
        
        self.rocket_width = self.rocket_imgs[0].get_width()
        self.rocket_height = self.rocket_imgs[0].get_height()

        self.frame_count = 0
        
    def Rocket_Display(self, path, player_height):

        self.frame_count += 1

        if self.frame_count >= 24:
            self.frame_count = 0

        img_num = self.frame_count/4
        img_num = math.floor(img_num)
    
        game_display.blit(self.rocket_imgs[img_num],(path - self.rocket_width/2, player_height))

class Button():

    def __init__(self, x_pos, y_pos, text, function = "", function2 = ""):
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.sprites = [button_imgs[0],
                        button_imgs[1],
                        button_imgs[2]]
        
        self.height = self.sprites[0].get_height()
        self.width = self.sprites[0].get_width()
        self.font_width = 56        
        self.font = pygame.font.Font("freesansbold.ttf", self.font_width)
        self.text = self.font.render(text, True, (255,255,255))
        
        self.text_width = self.text.get_width()

        while self.text_width >= 160:
            
            self.font_width -= 1
            self.font = pygame.font.Font("freesansbold.ttf", self.font_width)
            self.text = self.font.render(text, True, (255,255,255))
            self.text_width = self.text.get_width()
                           
        self.difference = self.x_pos + self.width/2 - self.text_width/2
        
        self.function = function
        self.function2 = function2

    def Display_Button(self, state):

        pos = [(self.x_pos),(self.y_pos)]   
        if (state == 2):
            pos = (self.x_pos,self.y_pos+15)
        elif (state > 2 or state < 0):
            pass

        game_display.blit(self.sprites[state],(pos[0],pos[1]))

        button_text = game_display.blit(self.text, (self.difference,pos[1]+20))
        
    def On_Click(self):

        #pygame.mixer.music.stop()
        pygame.mixer.Sound.play(Button_Click)
        
        pygame.time.wait(350)

        eval(self.function)
        if self.function2 != "":
            eval(self.function2)
        

    def Hovering(self, mouse_pos):

        if (mouse_pos[0] > self.x_pos and mouse_pos[0] < self.x_pos + self.width):
            if (mouse_pos[1] > self.y_pos and mouse_pos[1] < self.y_pos + self.height):
                return True

        return False

class Rank_Block():

    def __init__(self, x_pos, y_pos, ranking, player = "???", score = "???"):
        self.sprite = rank_img
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.ranking = str(ranking)
        self.player = player
        self.score = score
        
        self.font = pygame.font.Font("freesansbold.ttf", 25)
        
        self.rank_rank = self.font.render("Rank: " + self.ranking, True, (0,0,0))        
        self.player_rank = self.font.render("User: " + self.player, True, (0,0,0))        
        self.score_rank = self.font.render("Score: " + self.score, True, (0,0,0))
        
    def Build_Block(self):

        game_display.blit(self.sprite,(self.x_pos,self.y_pos))
        
        game_display.blit(self.rank_rank,(self.x_pos+15,self.y_pos+25))
        game_display.blit(self.player_rank,(self.x_pos+125,self.y_pos+25))
        game_display.blit(self.score_rank,(self.x_pos+330,self.y_pos+25))
        
class Player_Statistics():

    def __init__(self, user_data_index):
        
        userdata = open("userdata.txt")
        lines = userdata.readlines()
        user_data = lines[user_data_index].replace("\n","")

        self.user_data_index = user_data_index
        self.username, self.password, highscore = user_data.split("-")
        self.highscore = int(highscore)
        self.score = 0

    def Update_Userdata(self, new_score):
        
        if new_score > self.highscore:
            
            self.highscore = new_score

            line = self.username + "-" + self.password + "-" + str(new_score) + "\n"

            userdata = open("userdata.txt", "r").readlines()
            userdata[self.user_data_index] = userdata[self.user_data_index].replace(userdata[self.user_data_index], "")
            userdata[self.user_data_index] = line
            
            userdata_write = open("userdata.txt", "w+")
            userdata_write.writelines(userdata)
            userdata_write.close()
        

#Functions
def Game_Over():

    if statistics.rocket_health <= 0:
        
        if statistics.current_score > player_object.highscore:
            player_object.Update_Userdata(statistics.current_score)

        pygame.mixer.Sound.play(Game_Over_Sound)
        
        pygame.time.wait(350)

        Game_Menu(statistics.current_score)

    else:
        
        statistics.rocket_health -= 1

def Spawn_New_Meteorites(statistics):

    objects = []
    meteorite_amount = random.randint(2, 3) # CHANGE THIS TO 0, 3!!!!

    #fills the lanes list with random non-repeating numbers
    lanes = []
    lanes.append(statistics.player_path)
    while len(lanes) != meteorite_amount:      
        rand = random.randint(0,4)       
        if (rand not in lanes):      
            lanes.append(rand)
    
    for x in range(meteorite_amount):

        # this creates a a random number between -3 and 3, but cannot be between -0.5 and 0.5.
        rotation = random.randrange(-3,3)      
        while rotation < 0.5 and rotation > -0.5:
            rotation = random.randrange(-3,3)
        
        meteorite_object = Meteorite(random.randrange(-360,360),
                                     rotation,
                                     lanes[x],
                                     meteorites_imgs[random.randint(0,len(meteorites_imgs)-1)], x)
        
        objects.append(meteorite_object)

    return objects


#Game
def Update():

    #pygame.mixer.music.play(-1)

    pause = Pause_Button(716, 20)
    
    game_exit = False
    
    global statistics
    statistics = game_stats()

    meteorite_y_origin = -100
    meteorite_y_current = meteorite_y_origin
    meteorite_speed = 8

    global meteorite_objects
    global power_ups_objects
    meteorite_objects = Spawn_New_Meteorites(statistics)

    player = Rocket(0)
    player_path = 2

    font = pygame.font.Font("freesansbold.ttf", 25)

    background_pos = [0,-600]
    
    while not game_exit:

        mouse_pos = pygame.mouse.get_pos()

        pause.state = 1
        if (pause.Hovering(mouse_pos)):
            pause.state = 0    

        for event in pygame.event.get():

            if event.type == pygame.QUIT:           
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (pause.Hovering(mouse_pos)):
                    pause.pause_or_unpause()
                    
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause.pause_or_unpause()
                        
                if pause.paused == False:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if statistics.player_path > 0:
                            statistics.player_path -= 1
                                
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if statistics.player_path < 4:
                            statistics.player_path += 1

        
        #Blits
        for x in range(len(background_pos)):
            game_display.blit(background_imgs[0], (0,background_pos[x]))
            background_pos[x] += 1
            if background_pos[x] >= 600:
                background_pos[x] = -600
                        
        player.Rocket_Display(paths[statistics.player_path], statistics.player_height)

        for x in range(len(meteorite_objects)):
            meteorite_objects[x].Meteorite_Display(meteorite_y_current)

        pause.Display()

        if pause.paused == False:
            
        #Variables
            statistics.current_score += (1)*statistics.score_multiplier
            
            meteorite_y_current += statistics.meteorite_speed
            
            if statistics.meteorite_speed <= statistics.met_max_speed:
                statistics.meteorite_speed += statistics.met_speed_increase

            #Resets
            if meteorite_y_current >= 700:
                for x in range(len(meteorite_objects)):
                    meteorite_objects[x].__del__()
                    
                meteorite_y_current = meteorite_y_origin
                meteorite_objects = Spawn_New_Meteorites(statistics)

        #Score
        text = font.render("Score: " + str(statistics.current_score), True, (255,255,255))
        game_display.blit(text, (10,10))

        pygame.display.update()
        clock.tick(60)
        
        if pause.paused == False:
            
            #Collision Check
            for x in range(len(meteorite_objects)):
                meteorite_objects[x].Check_Collision(statistics.player_path, statistics.player_height, meteorite_y_current)

class Mute_Button():

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.muted = False
        self.state = 0
        self.imgs = mute_imgs

    def Hovering(self, mouse_pos):

        if (mouse_pos[0] > self.x_pos and mouse_pos[0] < self.x_pos + 64):
            if (mouse_pos[1] > self.y_pos and mouse_pos[1] < self.y_pos + 64):
                return True

        return False

    def mute_or_unmute(self):
        
        self.muted = not self.muted
        print(self.muted)

        if self.muted == False:
            pygame.mixer.music.set_volume(0.1)
            Button_Click.set_volume(1)
            Game_Over_Sound.set_volume(1)
        elif self.muted == True:
            pygame.mixer.music.set_volume(0)
            Button_Click.set_volume(0)
            Game_Over_Sound.set_volume(0)

    def Display(self):

        game_display.blit(self.imgs[self.state], (self.x_pos, self.y_pos))

        if self.muted == False:
            game_display.blit(self.imgs[2], (self.x_pos, self.y_pos))
        elif self.muted == True:
            game_display.blit(self.imgs[3], (self.x_pos, self.y_pos))        



global Button_Click
Button_Click = pygame.mixer.Sound("./Audio/Button_Click.wav")

global Game_Over_Sound
Game_Over_Sound = pygame.mixer.Sound("./Audio/Game_Over.wav")

pygame.mixer.music.load("./Audio/Theme.wav")
pygame.mixer.music.set_volume(0.1)

pygame.mixer.music.play(-1)




#Game Menu
def Game_Menu(score = 0):

    #pygame.mixer.music.play(-1)

    game_exit = False
    
    play_button = Button(310, 400, "PLAY", "Update()")
    
    quit_button = Button(550, 400, "Quit", "pygame.quit()", "quit()")

    scores_button = Button(70, 400, "Scores", "Build_Rankings()")

    buttons = [play_button, quit_button, scores_button]
    states = []

    background_pos = [0,-600]

    if score > 0:
        text_string = "Score: " + str(score)
    else:
        text_string = "Welcome!"
        
    font = pygame.font.Font("freesansbold.ttf", 45)
    
    score_text = font.render(text_string, True, (255,255,255))
    text_coordinates = (400 - score_text.get_width()/2 ,340)

    highscore_text = font.render("Highscore: " + str(player_object.highscore), True, (255,255,255))
    highscore_text_coordinates = (400 - highscore_text.get_width()/2 ,280)

    font = pygame.font.Font("freesansbold.ttf", 30)
    player_text = font.render("User: " + player_object.username, True, (0,0,0))

    for x in range(len(buttons)):
        states.append(0)

    while not game_exit:

        mouse_pos = pygame.mouse.get_pos()

        for x in range(len(background_pos)):
            game_display.blit(background_imgs[0], (0,background_pos[x]))
            background_pos[x] += 1
            if background_pos[x] >= 600:
                background_pos[x] = -600
        
        game_display.blit(logo_img, (325,10))     
        game_display.blit(score_text, text_coordinates)
        game_display.blit(highscore_text, highscore_text_coordinates)
        
        game_display.blit(rank_img, (-250,-11))
        game_display.blit(player_text, (5,10))

        mute_button.state = 1
        if (mute_button.Hovering(mouse_pos)):
            mute_button.state = 0        

        for x in range(len(buttons)):
            if (buttons[x].Hovering(mouse_pos)):
                states[x] = 1
            else:
                states[x] = 0

        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (mute_button.Hovering(mouse_pos)):
                    mute_button.mute_or_unmute()
                
                for x in range(len(buttons)):
                    if (buttons[x].Hovering(mouse_pos)):
                        states[x] = 2

            if event.type == pygame.QUIT:           
                pygame.quit()
                quit()

        for x in range(len(buttons)):
            buttons[x].Display_Button(states[x])

        mute_button.Display()

        pygame.display.update()
        clock.tick(60)
            
        for x in range(len(buttons)):
            if states[x] == 2:
                buttons[x].On_Click()

#Highscores
def Bubblesort(data_list):
    Sorted = False
    x = len(data_list)-1
    while Sorted == False and x > 0:
        Sorted = True
        for y in range(x):
            if data_list[y][1] >= data_list[y+1][1]:
                Sorted = False
                temp = data_list[y]
                data_list[y] = data_list[y+1]
                data_list[y+1] = temp
                #print(data_list)
        x -= 1
        #print(x)
    return data_list


def Get_User_Scores():

    userdata = open("userdata.txt")
    lines = userdata.readlines()
    length = (len(lines))

    unsorted_ranks = []

    for x in range(length):
        temp = lines[x].split("-")
        unsorted_ranks.append([temp[0], int(temp[2].replace("\n",""))])

    #print(unsorted_ranks)
    return unsorted_ranks

def Build_Rankings():

    #pygame.mixer.music.play(-1)

    #create a list for background y positions
    background_pos = [0,-600]

    #get the list of players sorted in ascending order
    unsorted_scores = Get_User_Scores()
    sorted_rankings = Bubblesort(unsorted_scores)
    sorted_rankings.reverse()

    #Instantiate the return to menu button
    menu_button = Button(70, 400, "Menu", "Game_Menu()")
    buttons = [menu_button]
    states = []

    for x in range(len(buttons)):
        states.append(0)
    
    #Instantiate the rank block objects
    ranks = []
    for x in range(10):
        if len(sorted_rankings) > x:            
            temp = Rank_Block(290,((x)*59)-1, x+1, sorted_rankings[x][0], str(sorted_rankings[x][1]))
        elif len(sorted_rankings) <= x:
            temp = Rank_Block(290,((x)*59)-1, x+1)
        
        ranks.append(temp)

    while True:

        #Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        #Button states
        for x in range(len(buttons)):
            if (buttons[x].Hovering(mouse_pos)):
                states[x] = 1
            else:
                states[x] = 0

        #Display background at list positions and move the position
        #If the position is below the screen then move it back to -600
        for x in range(len(background_pos)):
            game_display.blit(background_imgs[0], (0,background_pos[x]))
            background_pos[x] += 1
            if background_pos[x] >= 600:
                background_pos[x] = -600

        #call the Build_Block function on all of my rank blocks
        for x in range(len(ranks)):
            ranks[x].Build_Block()
        
        #Get inputs from the player and check if the player presses
        #the mouse while hovering over the button.
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(len(buttons)):
                    if (buttons[x].Hovering(mouse_pos)):
                        states[x] = 2

            if event.type == pygame.QUIT:           
                pygame.quit()
                quit()
            
        #calls Display_Button on all of the buttons in my list
        for x in range(len(buttons)):
            buttons[x].Display_Button(states[x])

        pygame.display.update()
        clock.tick(60)

        #Calls the On_Click function if the player has clicked
        #while hovering over a button.
        for x in range(len(buttons)):
            if states[x] == 2:
                buttons[x].On_Click()

def Load_Player_Stats(player_data_index):

    userdata = open("userdata.txt")
    lines = userdata.readlines()

    global player_object
    player_object = Player_Statistics(player_data_index)

    initialise_game_display()
    Game_Menu()

#Load_Player_Stats(0)

#Game_Menu()
