import socket
import threading
import random

HOST = '127.0.0.1'
PORT = 5555

players = []  # Lista de jogadores conectados
lock = threading.Lock()  # Lock para garantir acesso exclusivo à lista de jogadores

def handle_client(conn):
    try:
        with lock:
            players.append(conn)  # Adiciona o novo jogador à lista de jogadores
        print('Novo jogador conectado:', conn.getpeername())

        number = random.randint(1, 100)  # Gera um novo número aleatório para cada jogo

        while True:
            try:
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

            except OSError as e:
                print('Erro durante a comunicação com o jogador:', conn.getpeername(), '-', e)
                break

    finally:
        with lock:
            players.remove(conn)  # Remove o jogador da lista de jogadores
        print('Jogador acertou e foi desconectado:', conn.getpeername())
        conn.close()

def start_game():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print('Aguardando conexões dos jogadores...')

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn,)).start()  # Inicia uma nova thread para cada jogador

if __name__ == '__main__':
    start_game()

# lsof -i :5555
# kill -9 13942
# python3 server.py