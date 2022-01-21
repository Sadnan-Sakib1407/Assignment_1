import socket
import sys
from termcolor import colored


host = socket.gethostname()
port = 2222
client_socket = None


# function to create socket
def create_socket():
    try:
        soc = socket.socket()
        return soc
    except socket.error:
        print('Socket creation error')
        return None


# function to connect socket
def connect_socket():
    global host
    global port
    global client_socket

    try:
        client_socket.connect((host, port))
    except socket.error as err:
        print('Socket connect error. Message: ', str(err))


# function to send message
def send_message(msg):
    global client_socket
    client_socket.send(msg.encode())


# function to receive message
def receive_message():
    global client_socket
    msg = client_socket.recv(1024)
    msg = str(msg, 'utf-8')
    return msg


def get_user_choice_input(choice_domain, input_prompt, error_prompt):
    choice = ''
    while choice == '':
        choice = input(input_prompt)
        if choice not in choice_domain:
            print(error_prompt)
            choice = ''
    return choice


# function to handle task 1
def handle_send_message_task():
    print(colored("\n================= Send message Task ====================", "yellow", attrs=['bold', 'blink']))
    text = input('\nGive the message to send to the server: ')
    send_message(text)
    text = receive_message()
    print('Your message: ', text)


def get_operands():

    while True:
        a = input('Give the first operand: ')
        b = input('Give the second operand: ')
        try:
            float(a)
            float(b)
            break
        except ValueError as err:
            print(str(err))
            print('The operands must be numbers................')
    return a, b


# function to handle task 2
def handle_calculator_task():
    print(colored('\n================= Task 2 ==================',"blue", attrs=['bold', 'blink']))
    option_message = receive_message()
    print(option_message)
    choice = get_user_choice_input(['+', '-', '*', '/'], 'Which operation do you want to choose: ',
                                   'Invalid choice.....Please try again')

    send_message(choice)

    a, b = get_operands()
    send_message(a)
    send_message(b)

    ans = receive_message()
    if ans == 'err':
        print('Invalid operation. Please try again')
    else:
        print('Result: ', ans)


def handle_current_date_and_time():
    print(colored('\n================= Date Time Task  ====================\n',"red", attrs=['bold', 'blink']))
    date = receive_message()
    print('Date: \t', date)
    time = receive_message()
    print('Time: \t', time)
    print('\n')


def handle_variable_status_task():
    option_msg = receive_message()
    print(option_msg)
    choice = get_user_choice_input(['a', 'b'], 'Which option do you want to choose: ',
                                   'Invalid choice.....Please try again')
    send_message(choice)

    if choice == 'a':
        status_variable = receive_message()
        print('\nStatus Variable : ', status_variable)
    elif choice == 'b':
        print('Update server variable status:\nPress c to turn on the variable\nPress d to turn off the variable')
        update_choice = get_user_choice_input(['c', 'd'], 'Which operation do you want to choose: ', 'Invalid choice.....Please try again')
        if update_choice == 'c':
            send_message('on')
        elif update_choice == 'd':
            send_message('off')
        verification_msg = receive_message()
        print(verification_msg)


# function to handle the main logics of the program
def main():
    global host
    global port
    global client_socket
    client_socket = create_socket()
    connect_socket()
    welcome_msg = receive_message()
    print(colored(welcome_msg, 'blue'))
    while True:
        option_msg = receive_message()
        print(option_msg)

        choice = get_user_choice_input(['0', '1', '2', '3', '4'], 'Which operation do you want to choose: ', 'Invalid choice.....Please try again')

        send_message(choice)
        if choice == '1':
            handle_send_message_task()
        elif choice == '2':
            handle_calculator_task()
        elif choice == '3':
            handle_current_date_and_time()
        elif choice == '4':
            handle_variable_status_task()
        elif choice == '0':
            client_socket.close()
            break
        else:
            print('Invalid choice')


main()
