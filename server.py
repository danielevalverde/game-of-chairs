import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

players = []  # Lista de jogadores conectados
lock = threading.Lock()  # Lock para garantir acesso exclusivo à lista de jogadores

def handle_client(conn):
    try:
        with lock:
            players.append(conn)  # Adiciona o novo jogador à lista de jogadores
        print('Novo jogador conectado:', conn.getpeername())

        while True:
            data = conn.recv(1024).decode()

            if not data:
                break

            guess = int(data)

            if guess == number:
                response = 'Correto! Você venceu o jogo!'
                break
            elif guess < number:
                response = 'Maior'
            else:
                response = 'Menor'

            conn.sendall(response.encode())

    finally:
        with lock:
            players.remove(conn)  # Remove o jogador da lista de jogadores
        conn.close()
        print('Jogador desconectado:', conn.getpeername())

def start_game():
    number = 42

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print('Aguardando conexões dos jogadores...')

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn,)).start()  # Inicia uma nova thread para cada jogador

if __name__ == '__main__':
    start_game()
