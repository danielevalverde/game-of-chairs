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
import time
import random
import constants

HOST = '127.0.0.1'
PORT = 5556

players = []  # Lista de jogadores conectados
players_ready = 0
lock = threading.Lock()  # Lock para garantir acesso exclusivo à lista de jogadores
time_to_stop = None
is_game_on = False
curr_turn = 0
music_stopped = True
chairs = []


def play_music(conn):
    conn.sendall(constants.PLAY_MUSIC.encode())


def stop_music(conn):
    conn.sendall(constants.STOP_MUSIC.encode())


def handle_client(conn):
    try:
        with lock:
            players.append(conn)  # Adiciona o novo jogador à lista de jogadores
        print('Novo jogador conectado:', conn.getpeername())
        is_this_player_ready = False
        is_music_playing = False
        while True:
            # Espera todos os jogadores estarem prontos. Quando eles mandarem mensagem de estarem prontos, aí
            # iniciamos a partida

            global players_ready
            if len(players) == players_ready:
                if not is_music_playing:
                    # se todos os jogadores estão prontos.
                    #todo: setar o tempo de play

                    global is_game_on
                    if not is_game_on:
                        is_game_on = True
                        global curr_turn
                        curr_turn += 1

                    play_music(conn)
                    print('Sending play_music command to ', conn.getpeername())
                    is_music_playing = True
                else:
                    #Música está tocando. Quando parar, vamos enviar para o jogador as cadeiras disponíveis e esperar input do jogador
                    #Cada cliente vai ter a lista de cadeiras. A gente só envia atualizações. Tipo: cadeira x agora etá indisponível
                    if music_stopped:
                        #todo: aqui mandamos: teremos x cadeiras nessa rodada.
                        conn.sendall(("QTD_CADEIRAS=" + str(len(chairs))).encode())
                        data = conn.recv(1024).decode() #todo: fallta a lógica por parte do cliente

                    #todo: a música já está tocando. Testa se é hora de parar a música para mandar o comando de parada
                    pass
            else:
                #Jogadores não estão todos prontos ainda. Recupera o que o player atual quer fazer
                if not is_this_player_ready:
                    data = conn.recv(1024).decode()
                    if not data:
                        print("not data. Saindo da thread")
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
        conn.close()
        print('Jogador desconectado:', conn.getpeername())

def manage_game():
    global curr_turn
    _curr_turn = curr_turn

    #espera o jogo começar.
    while True:
        if is_game_on:
            break

    global chairs
    for i in range(0, players_ready):#tem sempre (numJogadores - 1) cadeiras. Aqui colocamos o tamanho até numJogadores e no while, retiramos 1
        chairs.append('x')
    global music_stopped
    #depois que começar, para cada turno:
    while True:
        while _curr_turn == curr_turn: #o turno não fui atualizado ainda
            _curr_turn = curr_turn

        music_stopped = False
        #Configura cadeiras disponíveis
        chairs.pop()

        # recuperar um tempo, esperar,  mandar o comando de parada
        time_to_wait = random.randint(5, 15)
        print("Waiting " + str(time_to_wait))
        time.sleep(time_to_wait)
        # manda comando de parada da música para todos os jogadores
        for p in players:
            stop_music(p)
        music_stopped = True


def start_game():
    threading.Thread(target=manage_game, args=()).start()  # Inicia uma nova thread para gerenciar as partidas
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print('Aguardando conexões dos jogadores...')

        while True:#TODO: impedir novas conn enquanto uma partida está acontecendo
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn,)).start()  # Inicia uma nova thread para cada jogador


if __name__ == '__main__':
    start_game()