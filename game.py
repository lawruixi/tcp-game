#!/usr/bin/env python3

import time
import random
import sys

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

        self.last_moved = "";

    def action(self, action):
        move_dict = {
            "l": True,
            "r": True,
            "u": True, 
            "d": True
            } 
        attack_dict = {
            "lw": True,
            "rw": True,
            "uw": True,
            "dw": True,
            }
        #Dash
        if(action == "x"):
            result = self.dash(self.last_moved);
        if(action in move_dict):
            result = self.move(action); 
        elif(action in attack_dict):
            result = self.attack(action);
        return result;

    def dash(self, direction):
        direction_string = ""

        if(direction == ""):
            return "{0} doesn't move.".format(self.name);
        if(direction == "l"):
            for i in range(2, 0, -1):
                #find the furthest possible square that is dashable to.
                if(not board.is_passable(self.posX - i, self.posY)):
                    continue
                self.posX -= i;
                break
            direction_string = "left"
        elif(direction == "r"):
            for i in range(2, 0, -1):
                if(not board.is_passable(self.posX + i, self.posY)):
                    continue
                self.posX += i;
                break
            direction_string = "right"
        elif(direction == "u"):
            for i in range(2, 0, -1):
                if(not board.is_passable(self.posX, self.posY - i)):
                    continue
                self.posY -= i;
                break
            direction_string = "up"
        elif(direction == "d"):
            for i in range(2, 0, -1):
                if(not board.is_passable(self.posX, self.posY + i)):
                    continue
                self.posY += i;
                break
            direction_string = "down"
        return "{0} dashes {1}!".format(self.name, direction_string);

    def move(self, direction):
        direction_string = "" #Commentary purposes

        if(direction == "l"):
            if(board.is_passable(self.posX - 1, self.posY)):
                self.posX -= 1;
            direction_string = "left"
        elif(direction == "r"):
            if(board.is_passable(self.posX + 1, self.posY)):
                self.posX += 1;
            direction_string = "right"
        elif(direction == "u"):
            if(board.is_passable(self.posX, self.posY - 1)):
                self.posY -= 1
            direction_string = "up"
        elif(direction == "d"):
            if(board.is_passable(self.posX, self.posY + 1)):
                self.posY += 1;
            direction_string = "down"
        self.last_moved = direction;
        return "{0} moves {1}!".format(self.name, direction_string);

    def attack(self, attack):
        attack_string = "" #Commentary purposes

        if(attack == "lw"):
            board.attack_square(WIDE_DAMAGE, self.posX - 1, self.posY - 1);
            board.attack_square(WIDE_DAMAGE, self.posX - 1, self.posY);
            board.attack_square(WIDE_DAMAGE, self.posX - 1, self.posY + 1);
            attack_string = "left wide attack"
        elif(attack == "rw"):
            board.attack_square(WIDE_DAMAGE, self.posX + 1, self.posY - 1);
            board.attack_square(WIDE_DAMAGE, self.posX + 1, self.posY);
            board.attack_square(WIDE_DAMAGE, self.posX + 1, self.posY + 1);
            attack_string = "right wide attack"
        elif(attack == "uw"):
            board.attack_square(WIDE_DAMAGE, self.posX - 1, self.posY - 1);
            board.attack_square(WIDE_DAMAGE, self.posX, self.posY - 1);
            board.attack_square(WIDE_DAMAGE, self.posX + 1, self.posY - 1);
            attack_string = "up wide attack"
        elif(attack == "dw"):
            board.attack_square(WIDE_DAMAGE, self.posX - 1, self.posY + 1);
            board.attack_square(WIDE_DAMAGE, self.posX, self.posY + 1);
            board.attack_square(WIDE_DAMAGE, self.posX + 1, self.posY + 1);
            attack_string = "down wide attack"

        return "{0} uses {1}!".format(self.name, attack_string);

    def damage(self, damage):
        self.health -= damage;
        if(self.health < 0):
            self.health = 0
    
    def is_dead(self):
        return self.health <= 0

class Obstacle:
    def __init__(self, posX, posY):
        self.posX = posX;
        self.posY = posY;

class Board:
    def __init__(self, SIZE):
        self.board = [[None for i in range(SIZE)] for j in range(SIZE)]

    def get_board(self):
        return self.board;

    def set_square(self, thing, posX, posY):
        self.board[posY][posX] = thing;

    def get_square(self, posX, posY):
        return self.board[posY][posX];

    def is_obstacle(self, posX, posY):
        return isinstance(self.get_square(posX, posY), Obstacle);

    def is_player(self, posX, posY):
        return isinstance(self.get_square(posX, posY), Player);

    def is_passable(self, posX, posY):
        if(posX < 0 or posY < 0 or posX >= SIZE or posY >= SIZE):
            return False
        if(self.is_obstacle(posX, posY)):
            return False
        return True

    def attack_square(self, damage, posX, posY):
        if(posX < 0 or posY < 0 or posX >= SIZE or posY >= SIZE):
            return
        target = self.get_square(posX, posY);
        if(isinstance(target, Player)):
            target.damage(damage);
            broadcast("{0} took {1} damage!".format(target.name, damage))
            return

    def generate_obstacles(self):
        for i in range(NUM_OBSTACLES):
            random_posX = random.randrange(SIZE);
            random_posY = random.randrange(SIZE);
            while(not self.get_square(random_posX, random_posY) is None):
                #If there is no obstacle or player there already
                random_posX = random.randrange(SIZE);
                random_posY = random.randrange(SIZE);

            obstacle = Obstacle(random_posX, random_posY);
            OBSTACLES.append(obstacle);
            self.set_square(obstacle, random_posX, random_posY);

    def update_board(self):
        self.board = [[None for i in range(SIZE)] for j in range(SIZE)]
        for obstacle in OBSTACLES:
            self.set_square(obstacle, obstacle.posX, obstacle.posY);
        for player in PLAYERS:
            if(self.is_player(player.posX, player.posY)):
                #Another player is already standing there
                self.board[player.posY][player.posX] = "**";
            else:
                self.board[player.posY][player.posX] = player;

        return board;

SIZE = 7
MAXHEALTH = 100
PLAYERS = []
NUM_OBSTACLES = SIZE
OBSTACLES = []

WIDE_DAMAGE = 15

board = Board(SIZE);


def draw_health():
    output_string = "";
    for player in PLAYERS:
        output_string += player.name + ": "
        health = player.health

        output_string += "Health: ["
        health_frac = int(health / MAXHEALTH * 20)

        output_string += "=" * health_frac
        output_string += "-" * (20 - health_frac)
        output_string += "] {0}/100\n".format(health)
    broadcast(output_string)


def draw_game_state(board):
    output_string = "\n"
    for i in board.get_board():
        output_string += ("-" * (5*SIZE + 1)) + "\n"
        output_string += "|"
        for j in i:
            if j is None:
                output_string += "    |"
            elif j == "**":
                output_string += " ** |"
            elif isinstance(j, Obstacle):
                output_string += " // |"
            elif isinstance(j, Player):
                output_string += " {0} |".format(j.name)
        output_string += "\n"
    output_string += "-" * (5*SIZE + 1) + "\n"
    broadcast(output_string)

    draw_health();

def is_action(string):
    return is_dash(string) or is_movement(string) or is_attack(string);

def is_dash(string):
    return string == "x";

def is_movement(string):
    movement_dict = {
            "l": True,
            "r": True,
            "u": True, 
            "d": True
            } 
    return movement_dict.get(string, False);

def is_attack(string):
    #Valid attacks: 
    #LW, RW, UW, DW for the wide attacks
    attack_dict = {
            "lw": True,
            "rw": True,
            "uw": True, 
            "dw": True
            } 
    return attack_dict.get(string, False);


def start_game(usernames):
    global board;
    board = Board(SIZE);

    #Initialize player
    player1 = Player(usernames[0][:2].upper(), 100, 0, SIZE//2);
    player2 = Player(usernames[1][:2].upper(), 100, SIZE - 1, SIZE//2);

    PLAYERS.append(player1)
    PLAYERS.append(player2)

    board.update_board();
    board.generate_obstacles();
    draw_game_state(board); 

    turn = 1
    subturn = 1;
    while(not player1.is_dead() and not player2.is_dead()): 
        broadcast("\n");
        actions_list = get_all_player_inputs("Input actions: \n", action_constraint); #Get player inputs, with the constraints of them being an action.
        actions_list_by_turn = list(zip(actions_list[0].split(" "), actions_list[1].split(" ")))
        print(actions_list_by_turn);

        for i in actions_list_by_turn:
            output_string = ""
            print(actions_list_by_turn)
            if(is_attack(i[1])):
                #If player 2 is attacking, player 1 always goes first (even if player1 is attacking. It makes no difference in this case.)
                output_string += player1.action(i[0]) + "\n"; board.update_board();
                output_string += player2.action(i[1]) + "\n"; board.update_board();
            elif(is_attack(i[0])):
                #Likewise, if player 1 is attacking, player 2 goes first.
                output_string += player2.action(i[1]) + "\n"; board.update_board();
                output_string += player1.action(i[0]) + "\n"; board.update_board();
            else:
                #Otherwise 1 then 2.
                output_string += player1.action(i[0]) + "\n"; board.update_board();
                output_string += player2.action(i[1]) + "\n"; board.update_board();

            broadcast("\n");
            broadcast(("=" * 45) + "\n" + (" " * 19) + "TURN {0}-{1}".format(turn, subturn) + (" " * 19) + "\n" + ("=" * 45))
            broadcast("\n");
            board.update_board()
            draw_game_state(board);

            broadcast(output_string);

            time.sleep(1)

            subturn += 1;

        turn += 1; subturn = 1;

        if(player1.is_dead() and player2.is_dead()):
            broadcast("Draw!")
            end_game();
        elif(player1.is_dead()):
            broadcast("{0} Wins!".format(player2.name))
            end_game();
        elif(player2.is_dead()):
            broadcast("{0} Wins!".format(player1.name))
            end_game();


def end_game():
    #Broadcast to all clients to disconnect.
    broadcast("!TERMINATE")
    for client in CLIENTS:
        remove_connection(client);
    print("Game has ended.")
    sys.exit(0);

#Networking stuff goes here
import socket
import concurrent.futures

CLIENTS = []

def get_input(client, constraint = None):
    conn, addr = client;
    #Gets input from a specific connection and address.
    try:
        send("%> ", client[0]);
        message = conn.recv(2048);
        message_str = message.decode("utf-8")
        if message:
            if(constraint):
                result = constraint(message_str) #result is a tuple of (is valid, error message if any)
                while(result[0] == False):
                    send(result[1], client[0]);
                    send("%> ", client[0])

                    message = conn.recv(2048);
                    message_str = message.decode("utf-8")
                    result = constraint(message_str);
            print("<" + addr[0] + ">: {0}".format(message_str));
            return message_str;
    except Exception as e:
        print(e)

def action_constraint(string):
    #Returns a tuple of (is_valid, error message if any)
    actions_list = string.strip().split(" ")
    print(actions_list)

    if(len(actions_list) != 3):
        return (False, "Please input three actions.\n")

    for i in actions_list:
        if(not is_action(i)):
            return (False, "Invalid action.\n")

    #1 attack per round
    numAttacks = 0
    for i in actions_list:
        if(is_attack(i)):
            numAttacks += 1
    if(numAttacks > 1): return (False, "Only one attack per turn allowed.\n")

    return (True, None);

def get_all_player_inputs(message, constraint = None):
    #Sends a message, then tries to get all player inputs, blocking until it does.
    broadcast(message);
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_input, client, constraint) for client in CLIENTS];
    return [f.result().strip() for f in futures]

def send(message, connection):
    #Sends a message to a specific connection.
    for client in CLIENTS:
        if client[0] == connection:
            try:
                client[0].send(message.encode('utf-8'))
                print(message);
            except:
                client[0].close()
                remove_connection(client);


def broadcast(message, connection = None):
    #Broadcasts a message to all clients that are connected, except for the connection sending the message.
    print(message);
    for client in CLIENTS:
        if client[0] != connection:
            try:
                client[0].send(message.encode('utf-8'))
            except:
                client[0].close()

                # if the link is broken, we remove the client
                remove_connection(client)

def remove_connection(connection):
    #Remove a connection from the clients[] array.
    for client in CLIENTS:
        if client[0] == connection:
            CLIENTS.remove(client);
            broadcast("{0} disconnected.".format(client[1]))

def get_ip_address():
    #Gets ip address of the machine running the server by asking Google DNS. Man, what can't Google do these days?
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    res = s.getsockname()[0]
    s.close()
    return res

def get_free_port():
    #Generates a random available port to use.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    addr, port = s.getsockname()
    s.close()
    return port

def start_server():
    HOST = get_ip_address()
    PORT = get_free_port();

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Restart the TCP server to allow binding to the ports
    server.bind((HOST, PORT))

    print("Starting server at IP {0} on port {1}".format(HOST, PORT))

    server.listen(2)
    numClients = 0

    while numClients < 2:
        conn, addr = server.accept();
        CLIENTS.append((conn, addr));

        print(addr[0] + " connected")
        numClients += 1;

    usernames = get_all_player_inputs("Enter username: \n")

    for i in range(len(CLIENTS)):
        send("Welcome, {0}!\n".format(usernames[i]), CLIENTS[i])

    start_game(usernames);

# start_game()

if(__name__ == "__main__"):
    start_server();

    
