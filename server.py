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
import queue

# chairs = queue.Queue()

HOST = '127.0.0.1'
PORT = 5556

players = []  # Lista de jogadores conectados
players_ready = 0
players_playing = 0
players_lock = threading.Lock()  # Lock para garantir acesso exclusivo à lista de jogadores
chairs_lock = threading.Lock()
time_to_stop = None
is_game_on = False
curr_turn = 1
music_should_stop = False
chairs = []
music_stop_event = threading.Event()


def play_music(conn):
    conn.sendall(constants.PLAY_MUSIC.encode())


def stop_music(conn):
    conn.sendall(constants.STOP_MUSIC.encode())


def handle_client(conn, music_stop_event):
    try:
        with players_lock:
            players.append(conn)  # Adiciona o novo jogador à lista de jogadores
        print('Novo jogador conectado:', conn.getpeername())

        global players_ready
        global players_playing
        global curr_turn
        global is_game_on

        # Espera o jogador atual estar pronto
        while True:
            data = conn.recv(1024).decode()
            is_ready = str(data)
            if is_ready == constants.READY:
                # cliente pronto para começar.
                players_ready += 1
                break
        print("Jogador atual está pronto")

        # Espera todos os jogadores estarem prontos
        while len(players) != players_ready:
            pass
        print("Todos os jogadores estão prontos")

        while True:
            if players_ready == 1:
            # if len(chairs) == 0:
                print("O jogador " + str(conn.getpeername()) + " venceu!")
                conn.sendall(constants.YOU_WON.encode())
                break
            else:
                print("Começando o turno ", curr_turn)
                conn.sendall(constants.START_TURN.encode())


            # Espera a música começar
            players_playing += 1
            play_music(conn)
            print('Sending play_music command to ', conn.getpeername())
            is_game_on = True
            print("música começou")

            # Espera a música parar
            while not music_stop_event.is_set():
                pass
            stop_music(conn)
            print("música parou")

            # Espera o jogador conseguir uma cadeira ou não haver cadeira disponível
            conn.sendall(("QTD_CADEIRAS=" + str(len(chairs))).encode())
            response = ''
            while response != constants.SUCCESS and response != constants.YOU_LOST:
                resp = conn.recv(1024).decode()
                chosen_chair = int(resp)
                if 1 > chosen_chair or chosen_chair > len(chairs):
                    # print("tente novamente. cadeira inválida")
                    response = constants.INVALID
                else:
                    with chairs_lock:
                        if chairs[chosen_chair - 1] == '-':
                            # print("cliente", conn.getpeername(), " conseguiu a cadeira. invalida para os outros")
                            chairs[chosen_chair - 1] = conn.getpeername()
                            response = constants.SUCCESS
                        elif chairs.__contains__('-'):
                            # print("Cadeira já foi escolhida. Procure outra.")
                            response = constants.ALREADY_IN_USE
                        else:
                            response = constants.YOU_LOST

                conn.sendall(response.encode())
            print("chairs: ", chairs)
            print("Fim da escolha de cadeiras para ", conn.getpeername(), response)

            # Espera todos os jogadores terminarem
            players_playing -= 1
            while players_playing != 0: pass
            print("todos os jogadores terminaram")

            # Espera limpeza para prox turno
            curr_turn += 1
            if response != constants.SUCCESS:
                # mata a conexão (no finally)
                # conn.sendall(constants.YOU_LOST.encode())
                players_ready -= 1
                break
            print("restam " + str(players_ready) + " jogadores")

    finally:
        print('Jogador desconectado:', conn.getpeername())
        with players_lock:
            players.remove(conn)  # Remove o jogador da lista de jogadores
        conn.close()


def manage_game(music_stop_event):
    global curr_turn

    # espera o jogo começar.
    while True:
        if is_game_on:
            break

    global chairs
    # chairs = ['-'] * players_ready
    # for i in range (0, players)
    # tem sempre (numJogadores - 1) cadeiras. Aqui colocamos o tamanho até numJogadores e no while, retiramos 1
    # global music_should_stop
    # depois que começar, para cada turno:
    while True:
        last_turn = curr_turn
        # Aqui estamos no fim de um turno (ou começo do primeiro)
        chairs = []
        chairs = ['-'] * players_ready
        print("players ready: ", players_ready)
        # music_should_stop = False
        music_stop_event.clear()
        # Configura cadeiras disponíveis
        if chairs:
            chairs.pop()
            print("removida uma cadeira")
        if not chairs:
            print("Nenhuma cadeira. Fim do Jogo")
            break

        # recuperar um tempo, esperar,  mandar o comando de parada
        time_to_wait = random.randint(5, 10)
        print("Waiting " + str(time_to_wait))
        time.sleep(time_to_wait)
        # manda comando de parada da música para todos os jogadores
        print("Please just stop the music")
        # music_should_stop = True
        music_stop_event.set()
        while curr_turn == last_turn: pass



def espera_novo_turno(_curr_turn, curr_turn):
    old_turn = curr_turn
    # while True:
    while _curr_turn == curr_turn:  # o turno não fui atualizado ainda
        # _curr_turn = curr_turn
        pass
    print("Turno: ", curr_turn)


def start_game():
    threading.Thread(target=manage_game,
                     args=(music_stop_event,)).start()  # Inicia uma nova thread para gerenciar as partidas
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print('Aguardando conexões dos jogadores...')

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client,
                             args=(conn, music_stop_event)).start()  # Inicia uma nova thread para cada jogador


if __name__ == '__main__':
    start_game()
