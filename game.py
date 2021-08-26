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
        attack_dict = {
            "lw": True,
            "rw": True,
            "uw": True,
            "dw": True,
            }
        if(action in move_dict):
            self.move(action); 
        if(action in attack_dict):
            self.attack(action);

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

    def attack(self, attack):
        if(attack == "lw"):
            attack_square(WIDE_DAMAGE, self.posX - 1, self.posY - 1);
            attack_square(WIDE_DAMAGE, self.posX - 1, self.posY);
            attack_square(WIDE_DAMAGE, self.posX - 1, self.posY + 1);
        elif(attack == "rw"):
            attack_square(WIDE_DAMAGE, self.posX + 1, self.posY - 1);
            attack_square(WIDE_DAMAGE, self.posX + 1, self.posY);
            attack_square(WIDE_DAMAGE, self.posX + 1, self.posY + 1);
        elif(attack == "uw"):
            attack_square(WIDE_DAMAGE, self.posX - 1, self.posY - 1);
            attack_square(WIDE_DAMAGE, self.posX, self.posY - 1);
            attack_square(WIDE_DAMAGE, self.posX + 1, self.posY - 1);
        elif(attack == "dw"):
            attack_square(WIDE_DAMAGE, self.posX - 1, self.posY + 1);
            attack_square(WIDE_DAMAGE, self.posX, self.posY + 1);
            attack_square(WIDE_DAMAGE, self.posX + 1, self.posY + 1);

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

WIDE_DAMAGE = 25

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
    BOARD = [[None for i in range(SIZE)] for j in range(SIZE)]
    for player in PLAYERS:
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
            elif isinstance(j, Player):
                output_string += " {0} |".format(j.name)
        output_string += "\n"
    output_string += "-" * (5*SIZE + 1)
    broadcast(output_string)

    draw_health();

def is_action(string):
    #Valid actions:
    #L, U, R, D for movement
    #
    actions_dict = {
            "l": True,
            "r": True,
            "u": True, 
            "d": True,
            "lw": True,
            "rw": True,
            "uw": True, 
            "dw": True
            } 
    return actions_dict.get(string, False);


def start_game(usernames):
    global BOARD
    BOARD = [["  " for i in range(SIZE)] for j in range(SIZE)]

    #Initialize player
    player1 = Player(usernames[0][:2].upper(), 100, 0, SIZE//2);
    player2 = Player(usernames[1][:2].upper(), 100, SIZE - 1, SIZE//2);

    PLAYERS.append(player1)
    PLAYERS.append(player2)

    BOARD = update_board();
    draw_game_state(); 

    while(True): #TODO: while both players not dead 
        actions_list = get_all_player_inputs("Input actions: "); #TODO: Split into two different lists and handle turn order and stuff
        print("HELLO WORLD!")
        print(actions_list);
        for i in actions_list:
            player1.action(i)

            BOARD = update_board();
            draw_game_state()

#Networking stuff goes here
import socket
import concurrent.futures

CLIENTS = []

def get_input(client):
    conn, addr = client;
    #Gets input from a specific connection and address.
    try:
        message = conn.recv(2048);
        if message:
            message_str = message.decode("utf-8")
            print("<" + addr[0] + ">: {0}".format(message_str));
            return message_str;
    except Exception as e:
        print(e)

def get_action_input(client):
    valid = False
    while(not valid):
        actions_string = get_input(client);
        actions_list = actions_string.split(" ")

        if(len(actions_list) != 3):
            send("Input three actions.", client[0])
            continue

        for i in actions_list:
            if(not is_action(i)):
                send("Invalid action.", client[0])
                break

        valid = True;
    return actions_list

def get_all_player_inputs(message):
    #Sends a message, then tries to get all player inputs, blocking until it does.
    broadcast(message);
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_input, client) for client in CLIENTS];
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

    
