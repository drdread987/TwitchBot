import socket
import string

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "MythicPlus_BOT"
PASS = "oauth:rf981oujagec7cqhroplu0fdhk4x6s"
CHAN = "tcgdrdread987"
readbuffer = ""

# stores [[username, key], ...]
key_list = []

dungeons = ["brh", "cos", "dht", "eoa", "hov", "mos", "nlt", "arc", "vow"]

admin = "tcgdrdread987"


s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", 'UTF-8'))
s.send(bytes("NICK " + NICK + "\r\n", 'UTF-8'))
s.send(bytes("JOIN  #" + CHAN + "\r\n", 'UTF-8'))

key_min = 9
key_max = 15

def send_message(msg):
    s.send(bytes("PRIVMSG #" + CHAN + " :" + msg + "\r\n", 'UTF-8'))


while True:

    readbuffer = str(s.recv(1024))

    temp = readbuffer.split("\n")

    for line in temp:
        parts = line.split(":")
        if line[0] == "PING":
            s.send("PONG %s\r\n" % line[1])
        elif len(parts) > 1:

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:
                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""

                usernamesplit = parts[1].split("!")
                username = usernamesplit[0]

                message = message[:len(message)-4]
                if message[0:4] == "!key":
                    message = message[5:len(message)]

                    if message[:3].lower() in dungeons:
                        if message[3] == "+":
                            good = False
                            try:
                                int(message[4:len(message)])
                                good = True
                            except:
                                string = "Something messed up with your key entry there bud"
                                send_message(string)
                            if good:
                                if key_max >= int(message[4:len(message)]) >= key_min:

                                    not_in = True
                                    for key in key_list:
                                        if key[0] == username:
                                            not_in = False
                                            break
                                    if not_in:

                                        key_list.append([username, message[:len(message)]])
                                        print("key was added")
                                        string = "Hello " + username + " your key has been added, " + \
                                                 message[:len(message)] + " at position " + str(len(key_list))
                                        send_message(string)

                                    else:
                                        string = "Your key was not added because you are already in the list"
                                        send_message(string)
                                elif int(message[4:len(message)]) == 420:
                                    string = "Too dank for this streamer"
                                    send_message(string)
                                elif int(message[4:len(message)]) == 69:
                                    string = "Too sexy for this streamer"
                                    send_message(string)
                                elif int(message[4:len(message)]) == 666:
                                    string = "Too evil for this streamer"
                                    send_message(string)
                                elif int(message[4:len(message)]) == 42:
                                    string = "Ooooh I know! What is the meaning of life?"
                                    send_message(string)
                                else:
                                    string = "Your key was either too low or too high for this streamer"
                                    send_message(string)

                        else:
                            string = "Something messed up with your key entry there bud, !key dun+#"
                            send_message(string)

                    elif message[:7].lower() == "current":
                        if len(key_list) > 0:
                            string = "The current key is " + key_list[0][1] + " from " + key_list[0][0]
                            send_message(string)
                        else:
                            string = "There is currently no keys in the list"
                            send_message(string)

                    elif message[:10].lower() == "removeself":
                        found = False
                        pos = 0
                        for key in key_list:
                            if key[0] == username:
                                found = True
                                break
                            pos += 1
                        if found:
                            del key_list[pos]
                            string = "Your key has been removed from the list"
                            send_message(string)

                    elif message[:2].lower() == "me":
                        found = False
                        pos = 1
                        for key in key_list:
                            if key[0] == username:
                                string = "I found you, you are " + username + " with " + key[1] +\
                                         " at position " + str(pos)
                                found = True
                                break
                            pos += 1
                        if not found:
                            string = "I did not find you in the list " + username
                        send_message(string)

                    elif message[:4].lower() == "list":
                        string = ""
                        m = 0
                        if len(key_list) > 4:
                            m = 4
                        elif len(key_list) > 0:
                            m = len(key_list)
                        if m > 0:
                            for x in range(0, m):
                                string += key_list[x][0] + " with " + key_list[x][1] + ","

                            send_message(string)
                        else:
                            string = "There is no keys in the list right now"
                            send_message(string)

                    elif message[:3].lower() == "min" and username == admin:
                        if message[3] == "-":
                            try:

                                key_min = int(message[4:6])
                                string = "I updated the min key to " + str(key_min)
                            except:

                                string = "Something went wrong with that sir!"
                            send_message(string)
                        else:
                            string = "Format for the min command is !key min-#"
                            send_message(string)

                    elif message[:3].lower() == "max" and username == admin:
                        if message[3] == "-":
                            try:

                                key_max = int(message[4:6])
                                string = "I updated the max key to " + str(key_max)
                            except:

                                string = "Something went wrong with that sir!"
                            send_message(string)
                        else:
                            string = "Format for the max command is !key max-#"

                    elif message[:4].lower() == "next" and username == admin:
                        if len(key_list) > 0:
                            del key_list[0]
                            if len(key_list) > 0:
                                string = "It is time for a new key! " + key_list[0][0] + " with the key "\
                                         + key_list[0][1] + " step on up!" \
                                                            " Please whisper maset-Kel'Thuzad with your name-server"
                            else:
                                string = "There is currently no key in the list to do"
                        else:
                            string = "There is currently no key in the list to do"
                        send_message(string)

                    elif message[:8].lower() == "commands":
                        string = "To add a key just use the three letter abbreviation for the dungeon" \
                                 " add a + then add your difficulty example being !key brh+11, the dungeon " \
                                 "abbreviations are brh cos dht eoa hov mos nlt arc vow"
                        send_message(string)
                        string = "Other commands are 'current' which will display the current key," \
                                 "'removeself' which will remove your key from the list," \
                                 "'next' which is an admin only commands which will switch to the next key," \
                                 "'me' which will tell you where you are in the key list," \
                                 "'min-#' which is an admin only command that changes the min key," \
                                 "'max-#' which is an admin only command that changes the max key," \
                                 "'list' which will show the top 5 in the list"
                        send_message(string)

                    else:
                        string = "That command was not recognized type '!key commands' to learn the commands"
                        send_message(string)







