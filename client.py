import sys
from socketio import *
import time
from tabulate import tabulate
from colorama import init, Fore, Style
from termcolor import colored

init()

# (start) Game start
client = Client()
print(colored("\n ☺Welcome To Quarto☺", attrs=['bold']))

username = ""


# (end) Game start


# (start) Connection Part
def connecting_user():
    cond = False
    while not cond:
        address = input("\n\n\nPlease enter server address or enter 0 for its default : "
                        "\n--> ")
        if address == "0":
            client.connect('http://127.0.0.1:8257')
            cond = True
        else:
            try:
                client.connect(f"http://{address}")
            except:
                print(
                    "Unfortunately now there is a problem in communicating with that server :(\nPlease try again later.")
                quit()


# (end) Connection part


# (start) Connecting and disconnecting events
@client.event
def connect():
    print(Fore.LIGHTGREEN_EX + "\n You're connected!" + Style.RESET_ALL)


@client.event
def connect_error(data):
    print(Fore.LIGHTRED_EX + "\n The connection failed!" + Style.RESET_ALL)


@client.event
def disconnect():
    print("You're disconnected!")


# (end) Connecting and disconnecting events
# (start) Game events
is_game_started = False


@client.on("game started")
def start_message(data):
    global is_game_started
    print(Fore.LIGHTRED_EX + "\n\nGame started!!!" + Style.RESET_ALL)
    if data == "Player 2":
        print("\nPlease wait for your opponent...")
    is_game_started = True


@client.on("select piece")
def select_piece(recieved_data):
    piece_choices = []
    print(recieved_data[0])

    for n in range(1, (len(recieved_data[1]) + 1) // 2):
        print(f'{n}) [{recieved_data[1][n - 1]}]', end="  ")
        piece_choices.append(str(n))

    print()

    for n in range((len(recieved_data[1]) + 1) // 2, (len(recieved_data[1]) + 1)):
        print(f'{n}) [{recieved_data[1][n - 1]}]', end="  ")
        piece_choices.append(str(n))

    cond = False
    while not cond:
        selected_piece = input("\nPlease enter number of a piece : "
                               "\n--> ")
        if selected_piece in piece_choices:
            print("Please wait for your opponent...")
            return [selected_piece, recieved_data[2]]
        else:
            print("Invalid input :(\nPlease try again.")
            cond = False


@client.on("select location")
def select_location(table, piece, p_username, cell_choices):
    print("\n\n")
    print(tabulate(table, tablefmt='fancy_grid'))
    print(f"\n{p_username} selected ({piece}) for you.")
    cond = False
    while not cond:
        selected_location = input("Please enter number of one of empty places on table to put the piece on : "
                                  "\n--> ")
        if selected_location in cell_choices:
            print(tabulate([[i if i != selected_location else piece for i in row] for row in table]
                           , tablefmt='fancy_grid'))
            return selected_location
        else:
            print("Invalid input :(\nPlease try again.")
            cond = False


@client.on("game won")
def game_ended(data=Fore.LIGHTRED_EX + "You lost :("):
    def new_game():
        global is_game_started
        is_game_started = False
        cond = False
        while not cond:
            select = input("If you want to play again enter 1 or enter 0 to return to main menu : "
                           "\n--> ")
            if select == "1":
                return making_game(username)
            elif select == "0":
                client.emit("remove from on_game")
                return main_menu()
            else:
                print("Invalid input :(\nPlease try again.")
                cond = False

    print("\n ")
    print(Style.BRIGHT + data + Style.RESET_ALL + '\n')
    new_game()


@client.on("Draw!")
def game_ended():
    def new_game():
        global is_game_started
        is_game_started = False
        cond = False
        while not cond:
            select = input("If you want to play again enter 1 or enter 0 to return to main menu : "
                           "\n--> ")
            if select == "1":
                return making_game(username)
            elif select == "0":
                client.emit("remove from on_game")
                return main_menu()
            else:
                print("Invalid input :(\nPlease try again.")
                cond = False

    print("\n ")
    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + "Draw!" + Style.RESET_ALL + '\n')
    new_game()


# (end) Game events
# (start) All functions
# (start) First option of main menu
def draw_line(n):
    for i in range(n):
        print("-", end="")
    print()


def space_designer(n):
    for i in range(n):
        print(" ", end="")


def random_player(user_name):
    def countdown(t):
        print("Waiting for other players...")
        while t and not is_game_started:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
            if is_game_started:
                return

        choose()

    def choose():
        cond = False
        while not cond:
            n = input("\n\nEnter 1 to try again and enter 0 to return to main menu."
                      "\n--> ")
            if n == "1":
                return request()
            elif n == "0":
                client.call("canceled", data=username)
                return main_menu()
            else:
                print("Invalid input :(\nPlease try again.")
                cond = False

    def request():
        client.emit("add_on_queue", data=user_name)
        if not is_game_started:
            client.call("start game req")
        countdown(10)

    request()


def making_game(user_name):
    print('\n\n\n')
    space_designer(24)
    print((colored('|Start Game|', attrs=['bold'])))
    draw_line(59)

    cond = False
    while not cond:
        n = input("Please choose one of these options by entering its number : "
                  "\n1 - Ready To Play!"
                  "\n0 - Return to main menu"
                  "\n--> ")
        if n == "1":
            return random_player(user_name)
        elif n == "0":
            return main_menu()
        else:
            print("Invalid input :(\nPlease try again.")
            cond = False


# (end) First option of main menu
def login_details():
    print('\n\n\n')
    space_designer(23)
    print((colored('|Credentials|', attrs=['bold'])))
    draw_line(59)

    cond = False
    while not cond:
        n = input("Please choose one of these options by entering its number : \n1 - Sign Up\n2 - Log In\n--> ")
        if n == "1":
            user_name = input("\nPlease enter a user name : ")
            password = input("Please enter a password : ")
            return ["s", user_name, password]
        elif n == "2":
            user_name = input("\nPlease enter your user name : ")
            password = input("Please enter your password : ")
            return ["l", user_name, password]
        else:
            print("Invalid input :(\nPlease try again.")
            cond = False


def main_menu():
    print('\n\n\n')
    space_designer(24)
    print(colored('|Main Menu|', attrs=['bold']))
    draw_line(59)
    cond = False
    while not cond:
        n = input("Please choose one of these options by entering its number : "
                  "\n1 - Start a new game"
                  "\n2 - Scoreboard"
                  "\n3 - About Me"
                  "\n4 - Quit Game"
                  "\n--> ")
        if n == "1":
            return making_game(username)
        elif n == "2":
            return score_board()
        elif n == "3":
            return about()
        elif n == "4":
            client.disconnect()
            sys.exit()
        else:
            print("There isn't such option :(")
            cond = False


def login():
    def entry_gate(login_code):
        global username

        if login_code == "This username already exists.":
            print("\n", Fore.LIGHTRED_EX + login_code + Style.RESET_ALL)
            return login()

        elif login_code[0] == "Successfully registered.":
            print("\n", Fore.LIGHTGREEN_EX + login_code[0] + Style.RESET_ALL)
            username = login_code[1]
            return main_menu()

        elif login_code == "There isn't such username.":
            print("\n", Fore.LIGHTRED_EX + login_code + Style.RESET_ALL)
            return login()

        elif login_code[0] == "Successfully Loged In.":
            print("\n", Fore.LIGHTGREEN_EX + login_code[0] + Style.RESET_ALL)
            username = login_code[1]
            return main_menu()

        elif login_code == "Wrong password or username.":
            print("\n", Fore.LIGHTRED_EX + login_code + Style.RESET_ALL)
            return login()

    credentials = login_details()
    client.emit("attaching username to sid", data=credentials, callback=entry_gate)


def score_board():
    print('\n\n\n')
    space_designer(24)
    print((colored('|Scoreboard|', attrs=['bold'])))
    draw_line(60)

    def return_to_menu():
        score_cond = False
        while not score_cond:
            if input("\n\nEnter 0 to return to main menu : "
                     "\n--> ") == "0":
                return main_menu()
            else:
                print("Invalid input :(\nPlease try again.")
                score_cond = False

    def scores_delivery(delivery):
        print()
        if delivery == {}:
            print("There isn't any record yet :(")
            return return_to_menu()
        else:
            table_indexes = []
            i = 1
            for user in delivery:
                if i <= 10:
                    table_indexes.append(user)
                    i += 1
                else:
                    break
            table_headers = [header for header in delivery[table_indexes[0]]]

            print(tabulate([[delivery[user][parameter] for parameter in delivery[user]] for user in delivery]
                           , headers=table_headers, showindex=table_indexes, tablefmt='grid'))

            return return_to_menu()

    client.emit("getting_scores", callback=scores_delivery)


def about():
    print('\n\n\n')
    space_designer(25)
    print((colored('|About Me|', attrs=['bold'])))
    draw_line(60)

    print("This game has been created by Mohammad Ali Kazemi."
          "\nA beginner programmer who really loves computer :)")
    cond = False
    while not cond:
        if input("\nEnter 0 to Return to Main Menu"
                 "\n--> ") == "0":
            return main_menu()
        else:
            print("Invalid input :(\nPlease try again.")
            cond = False


connecting_user()
login()
