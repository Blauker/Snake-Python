# CREATED BY:
# ▀█████████▄   ▄█          ▄████████ ███    █▄     ▄█   ▄█▄    ▄████████    ▄████████ 
#   ███    ███ ███         ███    ███ ███    ███   ███ ▄███▀   ███    ███   ███    ███ 
#   ███    ███ ███         ███    ███ ███    ███   ███▐██▀     ███    █▀    ███    ███ 
#  ▄███▄▄▄██▀  ███         ███    ███ ███    ███  ▄█████▀     ▄███▄▄▄      ▄███▄▄▄▄██▀ 
# ▀▀███▀▀▀██▄  ███       ▀███████████ ███    ███ ▀▀█████▄    ▀▀███▀▀▀     ▀▀█████▀▀▀   
#   ███    ██▄ ███         ███    ███ ███    ███   ███▐██▄     ███    █▄  ▀█████████▄ 
#   ███    ███ ███▌    ▄   ███    ███ ███    ███   ███ ▀███▄   ███    ███   ███    ███ 
# ▄█████████▀  █████▄▄██   ███    █▀  ████████▀    ███   ▀█▀   ██████████   ███    ███ 
#              ▀                                   ▀                        ███    ███ 2023

import os
import time
from enum import Enum
import random
import keyboard
import configparser

SCREEN_X = 25
SCREEN_Y = 12
GAME_SPEED = 0.2

class Color(Enum):
    RED =       "🟥"
    ORANGE =    "🟧"
    YELLOW =    "🟨"
    GREEN =     "🟩"
    BLUE =      "🟦"
    PURPLE =    "🟪"
    BROWN =     "🟫"
    WHITE =     "⬜"
    BLACK =     "⬛"
    MANZANA =   "🍎"
    STAR =      "⭐"
class Movement(Enum):
    RIGHT = 1
    LEFT  = 2
    DOWN  = 3
    UP    = 4
COLOR_MAPPING = {
    'RED': Color.RED,
    'ORANGE': Color.ORANGE,
    'YELLOW': Color.YELLOW,
    'GREEN': Color.GREEN,
    'BLUE': Color.BLUE,
    'PURPLE': Color.PURPLE,
    'BROWN': Color.BROWN,
    'WHITE': Color.WHITE,
    'BLACK': Color.BLACK
}

class Game():
    def __init__(self, size_x: int = None, size_y: int = None, bg_color: Color = None, player_color: Color = None, game_speed: float = None) -> None:
        """Constructor of the Game class

        Args:
            size_x (int, optional): Number screen's pixels on X.
            size_y (int, optional): Number screen's pixels on Y.
            bg_color (Color, optional): Color of the background.
            player_color (Color, optional): Color of the player.
            game_speed (float, optional): Game speed.
        """
        if isinstance(size_x, type(None)): self.size_x = SCREEN_Y
        else: self.size_x = size_y
        
        if isinstance(size_y, type(None)): self.size_y = SCREEN_X
        else: self.size_y = size_x

        if isinstance(bg_color, type(None)): self.bg_color = Color.WHITE
        else: self.bg_color = bg_color

        if isinstance(player_color, type(None)): self.player_color = Color.GREEN
        else: self.player_color = player_color

        if isinstance(game_speed, type(None)): self.game_speed = GAME_SPEED
        else: self.game_speed = game_speed

        # Validating if colors are valid, if not, defaults will be set 
        self.ValidateColors() 

        self.data = [[0] * self.size_y for _ in range(self.size_x)] 
        self.player = [(0, 2), (0, 1), (0, 0)]
        self.apple = []
        self.score = 0
        self.movement = Movement.RIGHT

    def ValidateColors(self):
        """Function to validate bg_color and player_color
        If both are the same, default will be set instead
        """
        if self.bg_color == self.player_color:
            self.bg_color = Color.WHITE
            self.player_color = Color.GREEN
    def Start(self) -> None:
        """Main Funcion of the class, will start the game loop and read keyboard inputs
        """
        self.GenerateApple(3)
        self.Clear()

        last_move_time = time.time()
        while True:
            if   keyboard.is_pressed("w"): self.movement = Movement.UP
            elif keyboard.is_pressed("a"): self.movement = Movement.LEFT
            elif keyboard.is_pressed("s"): self.movement = Movement.DOWN
            elif keyboard.is_pressed("d"): self.movement = Movement.RIGHT
            if keyboard.is_pressed("esc"): exit()

            current_time = time.time()
            if current_time - last_move_time >= self.game_speed:
                self.MoveSnake(self.movement)
                last_move_time = current_time 
    def Clear(self):
        """Function to clear the screen setting all matrix values to 0
        """
        self.data = [[0] * self.size_y for _ in range(self.size_x)]
        self.Update()     
    def Update(self):
        """Function to update the matrix values with player position as 1 and apple position as 2
        """
        for s in self.player:
            self.data[s[0]][s[1]] = 1
        for a in self.apple:
            self.data[a[0]][a[1]] = 2
        self.Print()
    def Grow(self):
        """Function to append new 'block' to the snake
        """
        last_body = self.player[-1]
        self.player.append(last_body)
    def CheckIfApple(self, s) -> bool:
        """Function to check if the player's head is on an apple

        Args:
            s (tuple): player's head position

        Returns:
            bool: If the player's head is on an apple or not
        """
        res = False
        for a in self.apple:
            if s == a:
                self.score += 1
                self.apple.remove(a)
                self.GenerateApple(1)
                res = True
        return res
    def Go(self, _x, _y) -> bool:
        """Function to move the snake on the desired direction
        This function will also check if we have eat an apple or we have lose the game by eating ourselves or a wall

        Args:
            _x (int): movement on the X axis (0, 1)
            _y (int): movement on the Y axis (0, 1)

        Returns:
            bool: Return True if we can continue playing the game
        """
        aux_player = []
        cont = True
        for index, s in enumerate(self.player):
            if index == 0:
                s = tuple(x + y for x, y in zip(s, (_x, _y)))
                if s[0] < 0 or s[1] < 0 or s[0] >= self.size_x or s[1] >= self.size_y or any(s == b for b in self.player):
                    cont = False 
                    break
                if self.CheckIfApple(s):
                    self.Grow()
            else: s = self.player[index-1]
            if cont: aux_player.append(s)

        if cont:
            for i in range(len(self.player)):
                self.player[i] = aux_player[i]
        
        return cont 
    def MoveSnake(self, movement: Movement):
        """Function to call Go() with the desired direction
        Also will check if we have won or lose the game

        Args:
            movement (Movement): Direction of our next movement
        """
        cont = True
        match movement:
            case Movement.RIGHT: cont = self.Go(0, 1)
            case Movement.LEFT:  cont = self.Go(0, -1)
            case Movement.DOWN:  cont = self.Go(1, 0)
            case Movement.UP:    cont = self.Go(-1, 0)
        if cont: self.CheckIfWin(); self.Clear()
        else: self.GameOver()
    def CheckIfWin(self):
        """Function to check if we have won the game by comparing the player lenght with the game lenght
        """
        if len(self.player) >= (self.size_x * self.size_y): self.Win()
    def Win(self):
        """Win function will show win screen
        """
        os.system("cls")
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.data[i][j] == 1:
                    print(Color.STAR.value, end="")
                else:
                    print(Color.YELLOW.value, end="")
            if i == (self.size_x / 2 - 1): print( "    CONGRATULATIONS!", end="")
            if i == (self.size_x / 2): print(f"    You have beat the game", end="")
            print()
        exit(0) # end game
    def GameOver(self):
        """Game Over Function will show game over screen
        """
        os.system("cls")
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.data[i][j] == 1:
                    print(Color.BLACK.value, end="")
                else:
                    print(Color.RED.value, end="")
            if i == (self.size_x / 2 - 1): print( "    GAME OVER:", end="")
            if i == (self.size_x / 2): print(f"    Your score: {self.score}", end="")
            print()
        exit(0) # end game
    def Print(self):
        """Function to print the screen with different colors depending of the matrix values
        """
        os.system("cls")
        for i in range(self.size_x):
            for j in range(self.size_y):
                if   self.data[i][j] == 1:  print(self.player_color.value, end="")
                elif self.data[i][j] == 2:  print(Color.MANZANA.value, end="")
                else:                       print(self.bg_color.value, end="")
            if i == (self.size_x / 2 - 1): print( "    SCORE:", end="")
            if i == (self.size_x / 2): print(f"    {self.score}", end="")
            print()
    def GenerateApple(self, amount: int) -> None:
        """Function to generate apples on a valid spot

        Args:
            amount (int): Number of apples to generate
        """
        for _ in range(amount):
            while True:
                randX = random.randint(0, self.size_x-1)
                randY = random.randint(0, self.size_y-1)
                if self.data[randX][randY] == 0:
                    tuple = (randX, randY)
                    self.apple.append(tuple)
                    break

def SetConfig():
    """Function that reads config.ini file and set the Game values
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    global screen_x; screen_x = config.getint('GameSettings', 'SCREEN_X')
    global screen_y; screen_y = config.getint('GameSettings', 'SCREEN_Y')
    bg_color_to_map = config.get('Colors', 'BG_COLOR')
    global bg_color; bg_color = Color = COLOR_MAPPING.get(bg_color_to_map)
    player_color_to_map = config.get('Colors', 'PLAYER_COLOR')
    global player_color; player_color =  Color = COLOR_MAPPING.get(player_color_to_map)
    global game_speed; game_speed = config.getfloat('Speed', 'GAME_SPEED')
SetConfig()

game = Game(screen_x, screen_y, bg_color, player_color, game_speed)
game.Start()