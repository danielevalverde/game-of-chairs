Lógica do servidor



parada = Math.random() # vai definir o momento em que a musica para

clientes = [] # quantidade de clientes conectados ao servidor
cadeiras = [] # quantidade de cadeiras disponíveis
cadeiras = [x |numClient |x  |x  ] # vamos inicializar com x, as posições das cadeiras disponiveis, assim quando a gente fizer a verificação no vetor, só adicionamos um cliente se na posição que ele escolheu tiver um x ao invés de um numero. Esse numero representa o identificador do cliente

for (i ; i < parada; i++)
    print('...')

cadeirasDisponiveis = cadeiras.lenght

for (i ; i < Client.lenght; i++)
- aguarda o cliente digitar o numero da cadeira
- pegar numero da cadeira do cliente 
- verifica se a cadeira tá disponivel
- se disponivel
    cadeiras.push(numClient)
    cadeirasDisponiveis--
- se nao tiver disponivel  
    responde a negativa pro cliente "tente novamnte" e o cliente pode digitar outro numero

- percorre o vetor de cadeiras pra verificar se o pid do cliente tá no vetor
mensagem "voce perdeu! tururu" 
desconecta


após a rodada uma cadeira é removida
cadeiras.pop
