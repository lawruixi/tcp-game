#!/usr/bin/env python3

import time

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
        update_board();
        return result;

    def dash(self, direction):
        direction_string = ""

        if(direction == ""):
            return "{0} doesn't move.".format(self.name);
        if(direction == "l"):
            self.posX = max(self.posX - 2, 0);
            direction_string = "left"
        elif(direction == "r"):
            self.posX = min(self.posX + 2, SIZE - 1);
            direction_string = "right"
        elif(direction == "u"):
            self.posY = max(self.posY - 2, 0);
            direction_string = "up"
        elif(direction == "d"):
            self.posY = max(self.posY + 2, SIZE - 1);
            direction_string = "down"
        return "{0} dashes {1}!".format(self.name, direction_string);

    def move(self, direction):
        direction_string = "" #Commentary purposes

        if(direction == "l"):
            if(self.posX > 0):
                self.posX -= 1;
            direction_string = "left"
        elif(direction == "r"):
            if(self.posX < SIZE - 1):
                self.posX += 1;
            direction_string = "right"
        elif(direction == "u"):
            if(self.posY > 0):
                self.posY -= 1
            direction_string = "up"
        elif(direction == "d"):
            if(self.posY < SIZE - 1):
                self.posY += 1;
            direction_string = "down"
        self.last_moved = direction;
        return "{0} moves {1}!".format(self.name, direction_string);

    def attack(self, attack):
        attack_string = "" #Commentary purposes

        if(attack == "lw"):
            attack_square(WIDE_DAMAGE, self.posX - 1, self.posY - 1);
            attack_square(WIDE_DAMAGE, self.posX - 1, self.posY);
            attack_square(WIDE_DAMAGE, self.posX - 1, self.posY + 1);
            attack_string = "left wide attack"
        elif(attack == "rw"):
            attack_square(WIDE_DAMAGE, self.posX + 1, self.posY - 1);
            attack_square(WIDE_DAMAGE, self.posX + 1, self.posY);
            attack_square(WIDE_DAMAGE, self.posX + 1, self.posY + 1);
            attack_string = "right wide attack"
        elif(attack == "uw"):
            attack_square(WIDE_DAMAGE, self.posX - 1, self.posY - 1);
            attack_square(WIDE_DAMAGE, self.posX, self.posY - 1);
            attack_square(WIDE_DAMAGE, self.posX + 1, self.posY - 1);
            attack_string = "up wide attack"
        elif(attack == "dw"):
            attack_square(WIDE_DAMAGE, self.posX - 1, self.posY + 1);
            attack_square(WIDE_DAMAGE, self.posX, self.posY + 1);
            attack_square(WIDE_DAMAGE, self.posX + 1, self.posY + 1);
            attack_string = "down wide attack"

        return "{0} uses {1}!".format(self.name, attack_string);

    def damage(self, damage):
        self.health -= damage;
        if(self.health < 0):
            self.health = 0
    
    def is_dead(self):
        return self.health <= 0

SIZE = 5
MAXHEALTH = 100
PLAYERS = []
BOARD = [[]]

WIDE_DAMAGE = 15

def attack_square(damage, posX, posY):
    if(posX < 0 or posY < 0 or posX >= SIZE or posY >= SIZE):
        return
    target = BOARD[posY][posX];
    if(isinstance(target, Player)):
        target.damage(damage);
        return

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

def update_board():
    global BOARD
    BOARD = [[None for i in range(SIZE)] for j in range(SIZE)]
    for player in PLAYERS:
        if(isinstance(BOARD[player.posY][player.posX], Player)):
            #Another player is already standing there
            BOARD[player.posY][player.posX] = "**";
        else:
            BOARD[player.posY][player.posX] = player;
    return BOARD;

def draw_game_state():
    output_string = ""
    for i in BOARD:
        output_string += ("-" * (5*SIZE + 1)) + "\n"
        output_string += "|"
        for j in i:
            if j is None:
                output_string += "    |"
            elif j == "**":
                output_string += " ** |"
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
    global BOARD
    BOARD = [["  " for i in range(SIZE)] for j in range(SIZE)]

    #Initialize player
    player1 = Player(usernames[0][:2].upper(), 100, 0, SIZE//2);
    player2 = Player(usernames[1][:2].upper(), 100, SIZE - 1, SIZE//2);

    PLAYERS.append(player1)
    PLAYERS.append(player2)

    update_board();
    draw_game_state(); 

    turn = 1
    while(not player1.is_dead() and not player2.is_dead()): 
        actions_list = get_all_player_inputs("Input actions: ", action_constraint); #TODO: Split into two different lists and handle turn order and stuff
        actions_list_by_turn = list(zip(actions_list[0].split(" "), actions_list[1].split(" ")))
        print(actions_list_by_turn);

        for i in actions_list_by_turn:
            output_string = ""
            print("HELLO WORLD: ", i)
            if(is_attack(i[1])):
                #If player 2 is attacking, player 1 always goes first (even if player1 is attacking. It makes no difference in this case.)
                output_string += player1.action(i[0]) + "\n";
                output_string += player2.action(i[1]) + "\n";
            elif(is_attack(i[0])):
                #Likewise, if player 1 is attacking, player 2 goes first.
                output_string += player2.action(i[1]) + "\n";
                output_string += player1.action(i[0]) + "\n";
            else:
                #Otherwise 1 then 2.
                output_string += player1.action(i[0]) + "\n";
                output_string += player2.action(i[1]) + "\n";

            broadcast(("=" * 45) + "\n" + (" " * 19) + "TURN {0}".format(turn) + (" " * 19) + "\n" + ("=" * 45))
            update_board()
            draw_game_state();

            broadcast(output_string);
            broadcast("\n")

            time.sleep(1)

            turn += 1;

        if(player1.is_dead() and player2.is_dead()):
            broadcast("Draw!")
        elif(player1.is_dead()):
            broadcast("{0} Wins!".format(player2.name))
        elif(player2.is_dead()):
            broadcast("{0} Wins!".format(player1.name))

#Networking stuff goes here
import socket
import concurrent.futures

CLIENTS = []

def get_input(client, constraint = None):
    conn, addr = client;
    #Gets input from a specific connection and address.
    try:
        message = conn.recv(2048);
        message_str = message.decode("utf-8")
        if message:
            if(constraint):
                while(constraint(message_str) == False):
                    send("Invalid input.\n", client[0]);

                    message = conn.recv(2048);
                    message_str = message.decode("utf-8")
            print("<" + addr[0] + ">: {0}".format(message_str));
            return message_str;
    except Exception as e:
        print(e)

def action_constraint(string):
    actions_list = string.strip().split(" ")
    print(actions_list)

    if(len(actions_list) != 3):
        return False

    for i in actions_list:
        if(not is_action(i)):
            return False

    #1 attack per round
    numAttacks = 0
    for i in actions_list:
        if(is_attack(i)):
            numAttacks += 1
    if(numAttacks > 1): return False

    return True

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

    usernames = get_all_player_inputs("Enter username: ")
    start_game(usernames);

# start_game()

start_server();

    
