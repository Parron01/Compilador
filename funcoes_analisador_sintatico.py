class Parser:
    def __init__(self, ListaTokens):
        self.tokens = ListaTokens
        self.indice_atual_token = 0
        self.token_atual = self.tokens[self.indice_atual_token]
        self.contador_token = 0  # Contador de tokens que chama match
        self.erro = False

    def advance(self):
        """Avança para o próximo token."""
        self.indice_atual_token += 1
        if self.indice_atual_token < len(self.tokens):
            self.token_atual = self.tokens[self.indice_atual_token]
        else:
            self.token_atual = None

    def match(self, expected_type):
        """Verifica se o token atual corresponde ao esperado e avança."""
        self.contador_token += 1
        if self.token_atual == expected_type:
            print(f"Token {self.contador_token}: {expected_type} correspondido com sucesso.")
            self.advance()
        else:
            self.error(f"Erro de sintaxe na função: {self.current_function}. "
                       f"Esperado '{expected_type}', encontrado '{self.token_atual}' no token {self.contador_token}.")

    def error(self, message):
        """Registra um erro de sintaxe."""
        raise Exception(message)

    def parse_PROG(self):
        print("\nNao Terminal PROG")
        """Função para o não-terminal PROG."""
        self.current_function = 'parse_PROG'
        self.match('public')
        self.match('class')
        self.match('id')
        self.match('{')
        self.match('public')
        self.match('static')
        self.match('void')
        self.match('main')
        self.match('(')
        self.match('String')
        self.match('[')
        self.match(']')
        self.match('id')
        self.match(')')
        self.match('{')
        self.parse_CMDS()  # Placeholder, por enquanto vazio
        self.match('}')
        self.parse_METODO()  # Placeholder, por enquanto vazio
        self.match('}')

    def parse_CMDS(self):
        """Função para o não-terminal CMDS. Por enquanto, apenas uma função vazia."""
        self.current_function = 'parse_CMDS'
        pass

    def parse_METODO(self):
        """Função para o não-terminal METODO. Por enquanto, apenas uma função vazia."""
        self.current_function = 'parse_METODO'
        pass
