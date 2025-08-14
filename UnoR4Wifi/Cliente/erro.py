'''
    Arquivo que contém a definição de todas as classes de erro
    padrão definidas no projeto. Cada erro possui apenas uma simples
    mensagem de aviso para quando ele for disparado.
'''

class ErroPinoNaoConfigurado(Exception):
    """
        ERRO 0

        O pino não foi definido durante o processo de configuração do robô.
        Não é possível utilizar essa funcionalidade sem a correta configuração
        de pinos!

        Para mais detalhes, cheque a documentação na seção ---
    """
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return  "O pino não foi definido durante o processo de configuração do robô. " +\
                "Não é possível utilizar essa funcionalidade sem a correta configuração de pinos!"


class ErroValorParametroInvalido(Exception):
    """
        ERRO - 1
        
        Valor informado como parâmetro para o comando não é aceito.
        Verifique a documentação do comando em questão na seção --- 
        para observar os possíveis valores de entrada e saída válidos.
    """
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return  "Valor informado como parâmetro para o comando não é aceito."


class ErroComandoInvalido(Exception):
    """
        ERRO 2
        
        Comando Inválido - Envie somente os comandos aceitos pelo servidor.
        Os comandos válidos estão listados na documentação na seção ---
    """
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return  "Comando Inválido - Envie somente os comandos aceitos pelo servidor"


class ErroConexaoInexistente(Exception):
    """
        ERRO - 3        
        
        Cliente não conectado ao Servidor, impossível realizar a 
        transimissão/recepção de dados.
    """
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return  "Cliente não conectado ao Servidor, impossível realizar a " +\
                "transmissão/recepção de dados."