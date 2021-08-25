#!/usr/bin/env python3
def intro():
    print("=============================================================")
    print("Welcome to the Best PvP Game ever invented, the Arena!!!!!!")
    print("=============================================================")


class Player:
    def __init__(self, name, health, posX, posY):
        self.name = name
        self.health = health
        self.posX = posX
        self.posY = posY

    def action(self, action):
        move_dict = {
            "l": True,
            "r": True,
            "u": True, 
            "d": True
            } 
        if(action in move_dict):
            self.move(action);

    def move(self, direction):
        if(direction == "l"):
            if(self.posX > 0):
                self.posX -= 1;
        elif(direction == "r"):
            if(self.posX < SIZE - 1):
                self.posX += 1;
        elif(direction == "u"):
            if(self.posY > 0):
                self.posY -= 1
        elif(direction == "d"):
            if(self.posY < SIZE - 1):
                self.posY += 1;
        return (self.posX, self.posY);

    def damage(self, damage):
        self.health -= damage;
        if(self.health < 0):
            self.health = 0
    
    def is_dead(self):
        return self.health <= 0

SIZE = 5
MAXHEALTH = 100
PLAYERS = []

def draw_health():
    for player in PLAYERS:
        print(player.name)
        health = player.health

        print("Health: [", end='')
        health_frac = int(health / MAXHEALTH * 20)

        print("=" * health_frac, end='')
        print("-" * (20 - health_frac), end='')
        print("] {0}/100".format(health))

def update_board():
    board = [["  " for i in range(SIZE)] for j in range(SIZE)]
    for player in PLAYERS:
        board[player.posY][player.posX] = "{0}".format(player.name);
    return board;

def draw_game_state(board):
    for i in board:
        print("-" * (5*SIZE + 1))
        print("|", end='')
        for j in i:
            print(" {0} |".format(j), end='')
        print()
    print("-" * (5*SIZE + 1))

    draw_health();

def is_action(string):
    #Valid actions:
    #L, U, R, D for movement
    #
    actions_dict = {
            "l": True,
            "r": True,
            "u": True, 
            "d": True
            } 
    return actions_dict.get(string, False);

def get_actions():
    print("Input actions:")

    valid = False
    while(not valid):
        actions_string = input().lower();
        actions_list = actions_string.split(" ")

        if(len(actions_list) != 3):
            print("Input three actions.")
            continue

        for i in actions_list:
            if(not is_action(i)):
                print("Invalid action.")
                break

        valid = True;

    return actions_list

def start_game():
    board = [["  " for i in range(SIZE)] for j in range(SIZE)]

    #Initialize player
    player1 = Player("P1", 100, 0, SIZE//2);

    PLAYERS.append(player1)

    board = update_board();
    draw_game_state(board); 
    actions_list = get_actions();

    for i in actions_list:
        player1.action(i)

        board = update_board();
        draw_game_state(board)

start_game()


    
