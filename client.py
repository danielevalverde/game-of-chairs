import socket

HOST = '127.0.0.1'
PORT = 5555

def play_game():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print('Conectado ao servidor')

        while True:
            guess = input('Adivinhe o número (ou "q" para sair): ')

            if guess == 'q':
                break

            client_socket.sendall(guess.encode())
            response = client_socket.recv(1024).decode()

            if response.startswith('Correto'):
                print(response)
                break
            else:
                print(response)

if __name__ == '__main__':
    play_game()
