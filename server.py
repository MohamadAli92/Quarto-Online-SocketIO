from socketio import *
from modules import play
from modules import statics
from colorama import Fore
import json

server = Server(async_mode='gevent')
onlines = []
on_queue = []
game_usernames = []
on_game = []


# (start) Connecting event
@server.event
def connect(sid, environ, auth):
    print(sid, "connected!")
    onlines.append(sid)


@server.event
def disconnect(sid):
    global on_game
    global on_queue
    global game_usernames
    print(sid, "disconnected!")
    if sid in on_queue:
        on_queue.remove(sid)
    for game in on_game:
        if sid in game:
            on_game.remove(game)
            print(sid, "was in game :/")
            game.remove(sid)
            server.emit("game won", data=Fore.LIGHTGREEN_EX + "Other player disconnected!\nYou won.", room=game[0])
            with open("username_sid.txt", "r") as username_sid_file:
                username_sid_dic = json.loads(username_sid_file.read())

            for is_loser in username_sid_dic:
                if sid == username_sid_dic[is_loser]:
                    loser_username = is_loser
                    break
            for is_winner in username_sid_dic:
                if game[0] == username_sid_dic[is_winner]:
                    winner_username = is_winner
                    break

            return statics.main_func(winner_username, loser_username, 0)

    onlines.remove(sid)
    return


# (end) Connecting event


# (start) All functions
def attach_username_to_sid(sid, username):
    try:
        with open("username_sid.txt", "r") as username_sid_file:
            username_sid_dic = json.loads(username_sid_file.read())

            username_sid_dic[username] = sid
    except:
        print("There was problem in saving username")
        username_sid_dic = {username: sid}

    with open("username_sid.txt", "w") as username_sid_file:
        username_sid_file.write(json.dumps(username_sid_dic))


# (end) All functions


# # My events
# (start) Saving username
@server.on("attaching username to sid")
def attaching(sid, credentials):
    try:
        with open("usernames_passwords_file.txt", "r") as usernames_passwords_file:
            usernames_passwords_dic = json.loads(usernames_passwords_file.read())
    except:
        usernames_passwords_dic = {}
    mode = credentials[0]
    username = credentials[1]
    password = credentials[2]

    # Sign Up
    if mode == "s":
        if username in usernames_passwords_dic:
            print("This username already exists.")
            return "This username already exists."
        else:
            usernames_passwords_dic[username] = password
            with open("usernames_passwords_file.txt", "w") as usernames_passwords_file:
                usernames_passwords_file.write(json.dumps(usernames_passwords_dic))
            print("Successfully registered.")
            attach_username_to_sid(sid, username)
            return ["Successfully registered.", username]

    # Log In
    elif mode == "l":
        if username not in usernames_passwords_dic:
            print("There isn't such username.")
            return "There isn't such username."
        else:
            if usernames_passwords_dic[username] == password:
                print("Successfully Loged In.")
                attach_username_to_sid(sid, username)
                return ["Successfully Loged In.", username]
            else:
                print("Wrong password or username.")
                return "Wrong password or username."


# (end) Saving username

# (start) player fetch
@server.on("start game req")
def game_making(sid):
    global on_queue
    global game_usernames

    def start_game(s_server, s_player1, s_player2, s_p1_username, s_p2_username):
        global game_usernames
        global on_game

        if [s_player1, s_player2] not in on_game:
            on_game.append([s_player1, s_player2])

        print(on_game)
        game_usernames = []
        play.main(s_server, s_player1, s_player2, s_p1_username, s_p2_username)

    print(sid)
    if len(on_queue) == 1:
        p1_username = game_usernames[0]
        print(p1_username)
    elif len(on_queue) == 2:
        p2_username = game_usernames[1]
        print(p2_username)
    if len(on_queue) >= 2:
        player1, player2 = on_queue[0], on_queue[1]
        print("two")
        on_queue = []
        start_game(server, player1, player2, game_usernames[0], game_usernames[1])

    # global on_queue
    # global game_usernames
    # server.call()


@server.on("canceled")
def delete_from_lists(sid, username):
    global on_queue
    global game_usernames
    if sid in on_queue:
        on_queue.remove(sid)
    if username in game_usernames:
        game_usernames.remove(username)


@server.on("add_on_queue")
def add_player_on_queue(sid, username):
    global on_queue
    global game_usernames
    if sid not in on_queue:
        on_queue.append(sid)
    if username not in game_usernames:
        game_usernames.append(username)
    print(on_queue)
    print(username)


@server.on("remove from on_game")
def remove_from_on_game(sid):
    global on_game
    print("applied")
    print(sid)
    for game in on_game:
        print(game)
        if sid in game:
            print("deleted from on_game")
            on_game.remove(game)
            break


# (end) player fetch
# (start) Giving scores
@server.on("getting_scores")
def getting_scores(sid):
    try:
        with open("static_file.txt", "r") as scores:
            scores_dic = json.loads(scores.read())
            print(scores_dic)
    except:
        print("There was a problem in reading scores.")
        scores_dic = {}

    return statics.sort_scores(scores_dic)


app = WSGIApp(server)
from gevent import pywsgi

pywsgi.WSGIServer(("127.0.0.1", 8257), app).serve_forever()
