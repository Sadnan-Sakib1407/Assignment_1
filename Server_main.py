import socket
import sys
import datetime

# defining the global variables
host = socket.gethostname()  # Server IP address
port = 2222  # Server port number
server_socket = None
client_socket = None


# status variable
status_variable = 'on'


# function to create a new socket
def create_socket():
    try:
        soc = socket.socket()
        return soc
    except socket.error:
        print('Socket creation error')
        return None


# function to bind the host and port with the server socket
def bind_socket():
    global host
    global port
    global server_socket

    try:
        server_socket.bind((host, port))
    except socket.error as err:
        print('Socket binding error. Message: ', str(err))


# function to accept a client connection request
def socket_accept():
    global server_socket
    global client_socket
    try:
        client_soc, client_address = server_socket.accept()
        print('Successfully connected to client.')
        return client_soc
    except socket.error as err:
        print('Socket accept error', str(err))


# function to send a message
def send_message(msg):
    global client_socket
    client_socket.send(msg.encode())


# function to receive a message
def receive_message():
    global client_socket
    msg = client_socket.recv(1024)
    msg = str(msg, 'utf-8')
    return msg


# function to handle task 1
def handle_receive_message_task():
    print('\n================= Task 1 ====================')
    text = receive_message()
    text = text.upper()
    print('Client says: ', text)
    send_message(text)


# function to handle task 2
def handle_calculator_task():
    print('\n================= Task 2 ==================')
    option_msg = """ 
    a. Choose + for addition
    b. choose - for subtraction 
    c. choose * for multiplication
    d. choose / for division """

    send_message(option_msg)
    operation = receive_message()
    print('client choice: ', operation)
    a = float(receive_message())
    b = float(receive_message())
    if operation == '+':
        ans = a + b
    elif operation == '-':
        ans = a - b
    elif operation == '*':
        ans= a * b
    elif operation == '/':
        ans = a/b
    else:
        print('Invalid operation')
        ans = 'err'
    print('Result: ', ans)
    send_message(str(ans))


# function to handle Task 3
def handle_current_date_and_time():
    print('================== Task3 ===================')
    date = (datetime.datetime.now())
    date_string = date.strftime('%d/%m/%Y')
    send_message(date_string)
    time = date.strftime('%X')
    send_message(time)


# function to handle Task 4
def handle_variable_status_task():
    global status_variable
    option_msg = "\na. Choose a to see the variable status\nb. Choose b to update the status\n"
    send_message(option_msg)
    choice = receive_message()
    print(choice)

    if choice == 'a':
        send_message(status_variable)
    elif choice == 'b':
        update_value = receive_message()
        status_variable = update_value
        send_message('Status variable has been updated successfully')


#  function to handle the main logics of the program
def main():
    global server_socket
    global client_socket
    server_socket = create_socket()
    print('Successfully created a socket')
    bind_socket()
    server_socket.listen(5)

    while True:
        client_socket = socket_accept()
        welcome_msg = """
         ====================================================================================================
                                    Hello. Welcome to my server.
         ====================================================================================================\n"""
        send_message(welcome_msg)
        while True:
            option_msg = """\nYou will be provided with 4 services using this program.
             
         1. Choose 1 to send a msg to server. 
         2. Choose 2 to use the calculator. 
         3. Choose 3 to see current date and time.
         4. Choose 4 to check and update variable status in the server.
         5. Choose 0 to exit\n"""

            send_message(option_msg)
            client_choice = receive_message()
            if client_choice == '1':
                handle_receive_message_task()
            elif client_choice == '2':
                handle_calculator_task()
            elif client_choice == '3':
                handle_current_date_and_time()
            elif client_choice == '4':
                handle_variable_status_task()
            elif client_choice == '0':
                client_socket.close()
                break
                print('Client connection is closed')

            else:
                print('Client wants to exit')
            # print('Successfully sends a message to client')
            #
            # text = receive_message()
            # print('Message from client:', text)


main()




















