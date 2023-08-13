# ==================================================
# define constant
# ==================================================

# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# obj default
obj_default_size_width = 50
obj_default_size_height = 50

# img path
character_img = "./character.png"
enemy_img = "./enemy.png"
carrot_img = "./carrot.png"

# bgm path
bgm_path = "./bgm.mp3"
coin_sound_effect = "./coinSoundEffect.mp3"

# ==================================================
# define class
# ==================================================

class object:
    def __init__(self, img, size_width, size_height, obj_coord_x, obj_coord_y, spped):
        self.img = img
        self.size_width = size_width
        self.size_height = size_height
        self.obj_coord_x = obj_coord_x
        self.obj_coord_y = obj_coord_y
        self.speed = spped
    
