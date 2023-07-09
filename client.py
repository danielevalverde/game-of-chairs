from pydub import AudioSegment
from pydub.playback import play
import socket
from playsound import playsound

import constants

HOST = '127.0.0.1'
PORT = 5555

def play_music():
    playsound('music/ciranda-cirandinha.mp3')


def play_game():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        global PORT
        while True:
            try:
                client_socket.connect((HOST, PORT))
                break
            except:
                PORT += 1

        print('Executando na porta ' + str(PORT) + '. Conectado ao servidor.')

        # play_music()

        while True:
            ready = input('Está pronto para jogar? s/n: ')
            client_socket.sendall(constants.READY.encode() if ready == 's' else constants.NOT_READY.encode())
            response = client_socket.recv(1024).decode()

            #Agora eu testo se o comando é para esperar ou começar a música
            if response == constants.PLAY_MUSIC:
                print("Tocando música")
                play_music()
                break
            else:
                print(response)


if __name__ == '__main__':
    play_game()
