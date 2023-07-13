import socket
from time import sleep

import random
# from playsound import playsound
import threading

import constants

# HOST = '127.0.0.1'
HOST = 'localhost'
PORT = 5502
chairs_available = []
sound_threads = []
stop_play_thread = False


def play_music_thread():
    cont = 1
    while not stop_play_thread:
        print("...", cont)
        sleep(1)
        cont += 1
    # try:
    #     playsound('music/ciranda-cirandinha.mp3')
    # except:
    #     playsound('music/ciranda-cirandinha-2.mp3')


def play_music():
    global stop_play_thread
    stop_play_thread = False
    sound_thread = threading.Thread(target=play_music_thread, args=())
    sound_thread.start()
    # sound_threads.append(sound_thread)
    sound_threads.append(False)
    # return sound_threads.index(sound_thread)
    return len(sound_threads) - 1


def stop_music(sound_thread_pos):
    global stop_play_thread
    stop_play_thread = True


def play_game():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        print('Executando na porta ' + str(PORT) + '. Conectado ao servidor.')

        # play_music()
        ready = 'n'
        while not ready == 's':
            # Ao iniciar partida
            ready = input('Está pronto para iniciar jogo? s/n: ')
        sound_thread_pos = -1
        client_socket.sendall(constants.READY.encode())
        perdeu = False
        while True:
            # Espera comando de início de turno
            response = client_socket.recv(1024).decode()
            if response == constants.START_TURN:
                print("Iniciando o turno")
            elif response == constants.YOU_WON:
                print("Parabéns, você venceu!")
                break

            # Espera comando para tocar música
            response = client_socket.recv(1024).decode()
            if response == constants.PLAY_MUSIC:
                print("Tocando música")
                sound_thread_pos = play_music()

            # Espera comando para parar a música
            response = client_socket.recv(1024).decode()
            if response == constants.STOP_MUSIC:
                print("Parando música")
                stop_music(sound_thread_pos)

            # Receber a quantidade de cadeiras disponíveis do servidor
            response = client_socket.recv(1024).decode()
            if response.startswith("QTD_CADEIRAS="):
                # Configura as cadeiras
                num_cadeiras = int(response.split("=")[1])
                print("Número de cadeiras disponíveis:", num_cadeiras)
                global chairs_available
                chairs_available = []
                for i in range(0, num_cadeiras):
                    chairs_available.append(i + 1)

            # Espera o jogador conseguir uma cadeira ou não haver cadeira disponível
            while True:
                # Solicitar ao jogador que escolha um número de cadeira:
                chosen_chair = input(
                    "Cadeiras disponíveis: {} \nEscolha uma cadeira (digite apenas o número): ".format(
                        chairs_available))
                # Enviar o número da cadeira escolhida para o servidor
                client_socket.sendall(chosen_chair.encode())
                try:
                    resp = client_socket.recv(1024).decode()
                except:
                    pass
                    print("Uma exception ocorreu")
                    break
                if resp == constants.SUCCESS:
                    print("Sucesso. Você conseguiu a cadeira")
                    break
                elif resp == constants.ALREADY_IN_USE:
                    print("Cadeira já em uso. Selecione uma outra")
                elif resp == constants.INVALID:
                    print("Valor inválido")
                elif resp == constants.YOU_LOST:
                    print("Você perdeu")
                    perdeu = True
                    break
                else:
                    print("[3] Mensagem não esperada: " + response)
            if perdeu:
                break

if __name__ == '__main__':
    play_game()
