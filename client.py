from socket import *
from sys import argv

def main():
    # Parse command line args
    if len(argv) != 3 or not argv[2].isdigit():
        print("usage: python3 client.py <server name> <server port>")
        return 1

    hostname, serverTCPPort = argv[1], int(argv[2])
    print("Client is running...")
    print("Remote host: {}, remote TCP port: {}".format(hostname, serverTCPPort))

    # Prompt user for their name
    name = input("Please enter your name: ") #has to be 'start', then type 'start' again to receive instructions to play.
    # Create TCP socket
    clientsocketTCP = socket(AF_INET, SOCK_STREAM)

    # Get IP address of server via DNS and print it
    TCPaddr = (hostname, serverTCPPort)
    print('The server address is {}:{}'.format(TCPaddr[0], TCPaddr[1]))
    
    # Connect to the server program
    clientsocketTCP.connect(TCPaddr)

    # Send hello message to the server over TCP connection
    clientsocketTCP.send("hello {}".format(name).encode())

    # TCP Loop
    while True:
        # Read in from TCP port
        gameinput = clientsocketTCP.recv(1024)

        # Keep listening if it doesn't receive a gameport message
        if gameinput.startswith(B'gameport'):
            # Read the control message from the TCP socket and print its contents
            # Split message in two words separated by space, assign the second word to UDPport
            _, UDPport = gameinput.decode().split(' ')
            UDPport = int(UDPport)
            print('Received UDP port#: {}'.format(UDPport))
            # Break from loop once needed info is received
            break


    # Create a UDP socket
    UDPsocket = socket(AF_INET, SOCK_DGRAM)
    UDPaddr = (hostname, UDPport)
    print(UDPaddr)
    end = False # default end flag

    # Game loop
    while True:
        # Prompt
        command = input(">")
        valid_commands = ['start', 'end', 'guess', 'exit']
    
        if not any(command.startswith(x) for x in valid_commands):
            # If invalid command is entered, ignore and continue asking for input
            continue

        # Parse command
        if command.startswith('start'):
            UDPsocket.sendto(B'ready', UDPaddr)
        elif command.startswith('end'):
            UDPsocket.sendto(B'end', UDPaddr)
        elif command.startswith('guess'):
            UDPsocket.sendto(command.encode(), UDPaddr)
        elif command.startswith('exit'):
            UDPsocket.sendto(B'bye', UDPaddr)
            end = True

        # UDP loop
        while True:
            # Continuously Read in from UDP port
            message, _ = UDPsocket.recvfrom(2048)

            # print message
            if message.startswith(B'instr'):
                text = message[6:] 
                print(text.decode())
               
                message, _ = UDPsocket.recvfrom(2048)
                _, text1, text2 = message.split(B' ')
                print('Word: {} Attempts left: {}'.format(text1.decode(), text2.decode()))

            elif message.startswith(B'stat'):
                _, text1, text2 = message.split(B' ')
                print('Word: {} Attempts left: {}'.format(text1.decode(), text2.decode()))
                
            elif message.startswith(B'end'):
                text = message[4:]
                print(text.decode())
                
            elif message.startswith(B'na'):
                pass
                
            elif message.startswith(B'bye'):
                # Send bye message and exit
                UDPsocket.sendto(B'bye', UDPaddr)
                end = True
                    
            # Break once receiving info and reprompt user
            break

        # If end message received, end client process
        if end:
            break
        #end of Game loop

    # Close sockets
    print("Closing TCP and UDP sockets...")


###########################################

if __name__ == "__main__":
    main()
