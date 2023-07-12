### Estudantes: Daniele Valverde de Jesus e Joanderson Gonçalves Santos

### Proposta de jogo: Jogo de Dança das Cadeiras

### Resumo do Jogo:
O jogo de Dança das Cadeiras é um jogo onde os jogadores devem se movimentar ao redor de um conjunto de cadeiras enquanto a música toca. Quando a música para, os jogadores devem encontrar uma cadeira vazia para sentar-se. O jogador que não conseguir encontrar uma cadeira é eliminado, e uma cadeira é removida a cada rodada subsequente. O jogo continua até que reste apenas um jogador, que é declarado o vencedor.

### Implementação Distribuída:
Para implementar o jogo de Dança das Cadeiras de forma distribuída será permitido a participação de mais de um jogador, através da utilização de uma arquitetura cliente-servidor.

### Servidor:

O servidor será responsável por coordenar o jogo, reproduzir a música, controlar o tempo e gerenciar as cadeiras. Irá manter um registro dos jogadores conectados, monitorar constantemente o estado do jogo e verificar se os eventos estão ocorrendo conforme o esperado.
O servidor também será responsável por receber e processar as ações dos jogadores, como solicitações para sentar ou sair das cadeiras.
O servidor deve suportar conexões simultâneas de vários clientes para que possa ocorrer a participação de múltiplos jogadores. 
```
- O servidor usa a biblioteca socket para estabelecer conexões de rede e receber dados dos clientes.
- A variável HOST define o endereço IP do servidor e a variável PORT define o número da porta em que o servidor estará ouvindo.
- As variáveis players, players_ready e players_playing são usadas para controlar o estado dos jogadores e a contagem de jogadores prontos e jogadores em jogo.
- As variáveis chairs e chairs_lock são usadas para gerenciar o estado das cadeiras disponíveis e garantir o acesso exclusivo a elas.
- A variável music_stop_event é um objeto de threading.Event() que controla quando a música deve parar de tocar.
- As funções play_music() e stop_music() enviam comandos para os clientes para reproduzir e parar a música.
- A função handle_client() é responsável por lidar com as ações dos jogadores. Ela recebe e processa as solicitações dos jogadores para sentar em uma cadeira e atualiza o estado do jogo conforme necessário.
- A função manage_game() é uma thread separada que coordena o fluxo do jogo. Ela controla o tempo de cada turno, define as cadeiras disponíveis e envia comandos para parar a música no momento certo.
- A função start_game() é responsável por iniciar o servidor e aguardar conexões dos jogadores. Ela cria uma nova thread para cada jogador conectado.
```

### Clientes:

Cada jogador é representado por um cliente conectado ao servidor.
O cliente exibe a interface gráfica do jogo para o jogador, mostrando a posição das cadeiras, a música em reprodução e o estado atual do jogo.
Os clientes enviam ações para o servidor, como solicitações para sentar ou sair das cadeiras.
Eles também recebem atualizações do servidor, como alterações nas cadeiras disponíveis e notificações sobre a eliminação de jogadores.

### Etapas do jogo:

Os jogadores iniciam o cliente e se conectam ao servidor.
O servidor inicia o jogo e inicia a música.
Os clientes exibem a interface gráfica do jogo para os jogadores.
Quando a música para, os jogadores enviam solicitações ao servidor para encontrar uma cadeira vazia, e as cadeiras são numeradas.
O servidor verifica as solicitações, remove a cadeira correspondente e atualiza os clientes. Se mais de um cliente solicitar a mesma cadeira, o primeiro que escolher leva a cadeira e o segundo tem que procurar outra cadeira.
Os jogadores que não conseguiram encontrar uma cadeira são eliminados.
O servidor repete os passos 4-6 até que reste apenas um jogador.
O último jogador é declarado o vencedor e o jogo termina.

O servidor precisa rastrear o estado do jogo, incluindo as cadeiras disponíveis e os jogadores eliminados oque requer uma estrutura de dados adequada. Podemos utilizar uma implementação de pub/sub ou stream, como disponíveis no banco de dados em memória Redis.

### Executando o jogo
Defina o endereço IP e a porta em que o servidor será executado, ajustando as variáveis HOST e PORT no código do servidor.
Abra um terminal ou prompt de comando e navegue até o diretório onde o arquivo do servidor está localizado.
Execute o servidor usando, por exemplo, seguinte comando:
`python3 server.py`
O servidor será iniciado e aguardará conexões dos jogadores.
Execute os clientes nos dispositivos dos jogadores
O servidor coordenará o jogo de Dança das Cadeiras, reproduzirá a música, gerenciará as cadeiras e processará as ações dos jogadores de acordo com a lógica descrita acima.
Certifique-se de ajustar as configurações do servidor de acordo com sua rede e ambiente de execução.

