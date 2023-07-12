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
lock = threading.Lock()  # Lock para garantir acesso exclusivo à lista de jogadores
time_to_stop = None
is_game_on = False
curr_turn = 0
music_should_stop = False
chairs = []
music_stop_event = threading.Event()


def play_music(conn):
    conn.sendall(constants.PLAY_MUSIC.encode())


def stop_music(conn):
    conn.sendall(constants.STOP_MUSIC.encode())


def handle_client(conn, music_stop_event):
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
                    # todo: setar o tempo de play

                    global is_game_on
                    if not is_game_on:
                        is_game_on = True
                        global curr_turn
                        curr_turn += 1

                    play_music(conn)
                    print('Sending play_music command to ', conn.getpeername())
                    is_music_playing = True
                else:
                    # Música está tocando. Quando parar, vamos enviar para o jogador as cadeiras disponíveis e esperar input do jogador
                    # Cada cliente vai ter a lista de cadeiras. A gente só envia atualizações. Tipo: cadeira x agora etá indisponível
                    # global music_should_stop
                    # if music_should_stop:
                    if music_stop_event.is_set():
                        is_music_playing = False
                        # Aqui vai ser onde paramos a música e tals
                        stop_music(conn)

                        # todo: aqui mandamos: teremos x cadeiras nessa rodada.
                        conn.sendall(("QTD_CADEIRAS=" + str(len(chairs))).encode())
                        # E recebemos o pedido do cliente com a cadeira que deseja
                        # o seguinte vai estar num loop até o cliente conseguir uma cadeira ou morrer tentando
                        resp = conn.recv(1024).decode()
                        chosen_chair = int(resp)
                        if 1 > chosen_chair or chosen_chair > len(chairs):
                            print("tente novamente. cadeira inválida")
                        else:
                            #TODO: fazer lock!!
                            if chairs[chosen_chair - 1] == '-':
                                print("cliente", conn.getpeername(), " conseguiu a cadeira. invalida para os outros")
                                chairs[chosen_chair - 1] = conn.getpeername()
                            else:
                                print("Cadeira já foi escolhida. Procure outra.")


                    # todo: a música já está tocando. Testa se é hora de parar a música para mandar o comando de parada

            else:
                # Jogadores não estão todos prontos ainda. Recupera o que o player atual quer fazer
                if not is_this_player_ready:
                    data = conn.recv(1024).decode()
                    if not data:
                        print("not data. Saindo da thread")
                        break  # todo: continua aqui essa lógica do if com break?
                    is_ready = str(data)
                    if is_ready == constants.READY:
                        # cliente pronto para começar.
                        players_ready += 1
                        is_this_player_ready = True
                else:
                    # se o jogador já está pronto
                    pass

    # TODO: precisamos coordenar os jogadores e quando eles mandam ou não mensagem...
    finally:
        with lock:
            players.remove(conn)  # Remove o jogador da lista de jogadores
        conn.close()
        print('Jogador desconectado:', conn.getpeername())


def manage_game(music_stop_event):
    global curr_turn
    _curr_turn = curr_turn

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
        #espera_novo_turno(_curr_turn, curr_turn)
        #se algum elemento dentro de chairs estiver com '-', não é fim de turno
        while chairs.__contains__('-'): pass
        #Aqui estamos no fim de um turno (ou começo do primeiro)

        chairs = ['-'] * players_ready #todo: temos que desconectar os clientes quando perdem
        print("players ready: ", players_ready)
        # music_should_stop = False
        music_stop_event.clear()
        # Configura cadeiras disponíveis
        if chairs:
            chairs.pop()
            print("removida uma cadeira")
        else:
            print("Nenhuma cadeira. Fim do Jogo")#TODO: dizer quem é o vencedor

        # recuperar um tempo, esperar,  mandar o comando de parada
        time_to_wait = random.randint(5, 10)
        print("Waiting " + str(time_to_wait))
        time.sleep(time_to_wait)
        # manda comando de parada da música para todos os jogadores
        # for p in players:
        #     stop_music
        print("Please just stop the music")
        # music_should_stop = True
        music_stop_event.set()


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

        while True:  # TODO: impedir novas conn enquanto uma partida está acontecendo
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client,
                             args=(conn, music_stop_event)).start()  # Inicia uma nova thread para cada jogador


if __name__ == '__main__':
    start_game()
