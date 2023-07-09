Lógica do servidor

variavel Parada

parada = Math.random()
# O servidor será responsável por coordenar o jogo, reproduzir a música, controlar o
# tempo e gerenciar as cadeiras. Irá manter um registro dos jogadores conectados,
# monitorar constantemente o estado do jogo e verificar se os eventos estão
# ocorrendo conforme o esperado.
# O servidor também será responsável por receber e processar as ações dos
# jogadores, como solicitações para sentar ou sair das cadeiras.
# O servidor deve suportar conexões simultâneas de vários clientes para que possa
# ocorrer a participação de múltiplos jogadores.

# O que temos a fazer:
# Coordenar o jogo (novo jogo. Começar. Tem jogadores disponíveis...)
# reproduzir a música (hmmm envia a música para cada cliente e controla quando a música para)
# controlar o tempo (depois de x tempo, a música para)
# gerenciar as cadeiras (cadeira x está com pessoa a, cadeira z está livre)


import socket
import threading
import random

import constants

HOST = '127.0.0.1'
PORT = 5556

players = []  # Lista de jogadores conectados
players_ready = 0
is_music_playing = False
lock = threading.Lock()  # Lock para garantir acesso exclusivo à lista de jogadores
number = 42 #TODO: remover


def play_music(conn):
    conn.sendall(constants.PLAY_MUSIC)


def stop_music(conn):
    conn.sendall(constants.STOP_MUSIC)


def handle_client(conn):
    try:
        with lock:
            players.append(conn)  # Adiciona o novo jogador à lista de jogadores
        print('Novo jogador conectado:', conn.getpeername())
        is_this_player_ready = False
        while True:
            # Espera todos os jogadores estarem prontos. Quando eles mandarem mensagem de estarem prontos, aí
            # iniciamos a partida

            #estado_partida:
            # 0: Aguardando conexão e confirmação
            # 1: Acabou de começar
            # 2:
            global players_ready
            if len(players) == players_ready:
                global is_music_playing
                if not is_music_playing:
                    # se todos os jogadores estão prontos.
                    play_music(conn)
                    is_music_playing = True
                else:
                    #todo: a música já está tocando. Testa se é hora de parar a música para mandar o comando de parada
                    pass
            else:
                #Jogadores não estão todos prontos ainda. Recupera o que o player atual quer fazer
                data = conn.recv(1024).decode()
                if not is_this_player_ready:
                    if not data:
                        break#todo: continua aqui essa lógica do if com break?
                    is_ready = str(data)
                    if is_ready == constants.READY:
                        # cliente pronto para começar.
                        players_ready += 1
                        is_this_player_ready = True
                else:
                    #se o jogador já está pronto
                    pass

#TODO: precisamos coordenar os jogadores e quando eles mandam ou não mensagem...
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
clientes = []
cadeiras = []


for (i ; i < parada; i++)
    print('...')
    # o que foi impresso: . . . . . .
 cadeiras = [x |numClient |x  |x  ]

cadeirasDisponiveis = cadeiras.lenght
for (i ; i < Client.lenght; i++)
- aguarda o cliente digitar o numero da cadeira
- pegar numero da cadeira do cliente 
- verifica se a cadeira tá disponivel
- se disponivel
    cadeiras.push(numClient)
    disponiveis--
- se nao tiver disponivel  
    responde a negativa pro cliente "tente novamnte" e o cliente pode digitar outro numero

- percorre o vetor de cadeiras pra verificar se o pid do cliente tá no vetor
mensagem "voce perdeu! tururu" 
desconecta


após a rodada uma cadeira é removida
cadeiras.pop()
