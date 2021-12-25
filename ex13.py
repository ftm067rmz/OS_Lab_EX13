import time
import math
import random
import threading 
import arcade

WIDTH = 700
HEIGHT = 500


class StarShip(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_orange.png")
        self.center_x = WIDTH//2
        self.center_y = 32
        self.width = 70
        self.height = 55
        self.angle = 0
        self.change_angle = 0
        self.speed = 4
        self.bullet_list = []
        self.score = 0
        self.joon = 3

    def fire(self):
        self.bullet_list.append(Bullet(self))

    def rotate(self):
        self.angle += self.change_angle * self.speed
    

class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/enemies/frog.png")
        self.center_x = random.randint(40,WIDTH-40)
        self.center_y = HEIGHT + 24
        self.width = 75
        self.height = 75
        self.speed = 3

    def move(self):
        self.center_y -= self.speed



class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__(":resources:images/space_shooter/meteorGrey_tiny1.png")
        
        self.center_x = host.center_x
        self.center_y = host.center_y
        self.speed = 6
        self.angle = host.angle
        self.music = arcade.load_sound(":resources:sounds/hurt5.wav")
        arcade.play_sound(self.music)
        
    def move(self):
        rad = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(rad)
        self.center_y += self.speed * math.cos(rad)
        
    

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Galaxy of Frogs🐸")
        arcade.set_background_color(arcade.color.DARK_IMPERIAL_BLUE)
        self.background_image = arcade.load_texture(":resources:images/backgrounds/stars.png")
        
        self.En = Enemy()
        self.user = StarShip()
        self.enemy_list = []

        self.flag = False
        self.my_thread = threading.Thread(target=self.add_enemy)
        self.my_thread.start()

        self.start_time = time.time()
        
        self.music_collision_bul = arcade.load_sound(":resources:sounds/laser1.wav")
        self.music_collision_enm = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.music_lose_joon = arcade.load_sound(":resources:sounds/error5.wav")
        self.music_GameOver = arcade.load_sound(":resources:sounds/gameover5.wav")
        

    def on_draw(self):
        arcade.start_render()
        
        if self.user.joon >=1:
            arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background_image)
            self.user.draw()

            Scores = f"SCORE : {self.user.score}"
            arcade.draw_text(Scores,WIDTH-97,7,arcade.color.WHITE,12,bold=True)
        
            if self.user.joon == 3:
                arcade.draw_text("♥ ♥ ♥", 8,7,arcade.color.WHITE,24,bold=True)
            elif self.user.joon == 2:
                arcade.draw_text("♥ ♥", 8,7,arcade.color.WHITE,24,bold=True)
            elif self.user.joon == 1:
                arcade.draw_text("♥", 8,7,arcade.color.WHITE,24,bold=True)
            
            for enemy in self.enemy_list:
                enemy.draw()
        
            for bul in self.user.bullet_list:
                bul.draw()
        
        else:
            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text("...GAME OVER...",WIDTH//3,HEIGHT//2,arcade.color.WHITE,20,bold=True)
            arcade.draw_text("Scores : "+str(self.user.score) ,WIDTH//2-60,HEIGHT//2-30,arcade.color.WHITE,15)

    def add_enemy(self):
        
        while True:
            self.enemy_list.append(Enemy())
            
            if self.user.score <= 8:
                time.sleep(5)
                
            elif 8 < self.user.score <= 15:
                time.sleep(4)
               
            elif 15 < self.user.score <= 20:
                time.sleep(3)

            elif 20 < self.user.score <= 25:
                time.sleep(2)
            
            elif self.user.score > 25:
                time.sleep(1)
                
            if self.flag==True:
                break
                
            
    def on_update(self, delta_time: float):
        
        self.user.rotate()
       
        self.end_time = time.time()

        
        if self.user.joon>=1:

            for enemy in self.enemy_list:
                enemy.move()

                if enemy.center_y <= 0:
                    self.user.joon -= 1
                    arcade.play_sound(self.music_lose_joon)
                    
                    if arcade.check_for_collision(self.user, enemy):
                        arcade.play_sound(self.music_collision_enm)
                        self.user.joon = 0
                    self.enemy_list.remove(enemy) 
        else:
            arcade.play_sound(self.music_GameOver)
            arcade.pause(1)
            self.flag = True
            

        for bul in self.user.bullet_list:
            bul.move()
    
        for bul in self.user.bullet_list:
            for enemy in self.enemy_list:
                if arcade.check_for_collision(bul, enemy):
                    arcade.play_sound(self.music_collision_bul)
                    self.enemy_list.remove(enemy)
                    self.user.bullet_list.remove(bul)
                    self.user.score += 1
                  

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.SPACE:
            self.user.fire()
        
        elif key == arcade.key.RIGHT:
            self.user.change_angle = -1

        elif key == arcade.key.LEFT:
            self.user.change_angle = 1
            

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.user.change_angle = 0



game = Game()
arcade.run()