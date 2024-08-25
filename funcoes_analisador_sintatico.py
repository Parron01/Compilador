import inspect
class Parser:
    def __init__(self, ListaTokens):
        self.tokens = ListaTokens
        self.indice_atual_token = 0
        self.token_atual = self.tokens[self.indice_atual_token]
        self.contador_token = 1  # Contador de tokens que chama match
        self.erro = False

    def advance(self):
        """Avança para o proximo token da lista de tokens provindas do léxico."""
        self.indice_atual_token += 1
        if self.indice_atual_token < len(self.tokens):
            self.token_atual = self.tokens[self.indice_atual_token]
        else:
            self.token_atual = None

    def match(self, token_esperado):
        """Confere se o token atual corresponde ao esperado e avança se corresponder."""
        self.contador_token += 1
        funcao_chamadora = inspect.stack()[1].function
        print(f"{self.contador_token}:token atual = `{self.token_atual}`")
        if self.token_atual == token_esperado:
            print(f"{self.contador_token}:Token {self.contador_token}: \"{token_esperado}\" correspondido com sucesso pela funcao = {funcao_chamadora}")
            self.advance()
        else:
            self.error(f"Erro de sintaxe na funcao: {self.funcao_atual}. Esperado '{token_esperado}', encontrado '{self.token_atual}' no token {self.contador_token}.")

    def error(self, message):
        raise Exception(message)

    def parse_PROG(self):
        """Funcao para o nao-terminal PROG."""
        self.funcao_atual = 'parse_PROG'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
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
        self.parse_CMDS()
        self.match('}')
        self.parse_METODO()
        self.match('}')
        print(f'Funcao: parse_PROG, finalizada.\n')


    def parse_METODO(self):
        """Funcao para o nao-terminal METODO."""
        self.funcao_atual = 'parse_METODO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == 'public':
            self.match('public')
            self.match('static')
            self.parse_TIPO()
            self.match('id')
            self.match('(')
            self.parse_PARAMS()
            self.match(')')
            self.match('{')
            self.parse_DC()
            self.parse_CMDS()
            self.match('return')
            self.parse_EXPRESSAO()
            self.match(';')
            self.match('}')
        elif self.token_atual == '}':  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em METODO: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_METODO, finalizada.\n')


    def parse_TIPO(self):
        """Funcao para o nao-terminal TIPO."""
        self.funcao_atual = 'parse_TIPO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == 'double':
            self.match('double')
        else:
            self.error(f"Erro de sintaxe em TIPO: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_TIPO, finalizada.\n')


    def parse_PARAMS(self):
        """Funcao para o nao-terminal PARAMS."""
        self.funcao_atual = 'parse_PARAMS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == 'double':
            self.parse_TIPO()
            self.match('id')
            self.parse_MAIS_PARAMS()
        elif self.token_atual == ')':  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em PARAMS: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_PARAMS, finalizada.\n')


    def parse_MAIS_PARAMS(self):
        """Funcao para o nao-terminal MAIS_PARAMS."""
        self.funcao_atual = 'parse_MAIS_PARAMS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == ',':
            self.match(',')
            self.parse_PARAMS()
        elif self.token_atual == ')':  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em MAIS_PARAMS: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_MAIS_PARAMS, finalizada.\n')


    def parse_DC(self):
        """Funcao para o nao-terminal DC."""
        self.funcao_atual = 'parse_DC'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == 'double':
            self.parse_VAR()
            self.parse_MAIS_DC()
        elif self.token_atual in ['}', 'return']:  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em DC: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_DC, finalizada.\n')


    def parse_MAIS_DC(self):
        """Funcao para o nao-terminal MAIS_DC."""
        self.funcao_atual = 'parse_MAIS_DC'
        
        if self.token_atual == 'double':
            self.parse_DC()
        elif self.token_atual != 'double':  # Produção nula (λ) quando não for 'double'
            return
        else:
            self.error(f"Erro de sintaxe em MAIS_DC: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_MAIS_DC, finalizada.\n')


    def parse_VAR(self):
        """Funcao para o nao-terminal VAR."""
        self.funcao_atual = 'parse_VAR'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        self.parse_TIPO()
        self.parse_VARS()
        self.match(';')
        print(f'Funcao: parse_VAR, finalizada.\n')



    def parse_VARS(self):
        """Funcao para o nao-terminal VARS."""
        self.funcao_atual = 'parse_VARS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        self.match('id')
        self.parse_MAIS_VAR()
        print(f'Funcao: parse_VARS, finalizada.\n')


    def parse_MAIS_VAR(self):
        """Funcao para o nao-terminal MAIS_VAR."""
        self.funcao_atual = 'parse_MAIS_VAR'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == ',':
            self.match(',')
            self.parse_VARS()
        elif self.token_atual == ';':
            print(f"vazei do mais_var = {self.token_atual}")  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em MAIS_VAR: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_MAIS_VAR, finalizada.\n')


    def parse_CMDS(self):
        """Funcao para o nao-terminal CMDS."""
        self.funcao_atual = 'parse_CMDS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual in ['if', 'while', 'System.out.println', 'id']:
            self.parse_CMD()
            self.parse_MAIS_CMDS()
        elif self.token_atual in ['}', 'return']:  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em CMDS: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_CMDS, finalizada.\n')


    def parse_MAIS_CMDS(self):
        """Funcao para o nao-terminal MAIS_CMDS."""
        self.funcao_atual = 'parse_MAIS_CMDS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == ';':
            self.match(';')
            self.parse_CMDS()
        elif self.token_atual in ["if"," while", "System.out.println", "id"]:
            self.parse_CMDS()
        elif self.token_atual in ['}', 'return']:  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em MAIS_CMDS: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_MAIS_CMDS, finalizada.\n')


    def parse_CMD(self):
        """Funcao para o nao-terminal CMD."""
        self.funcao_atual = 'parse_CMD'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        print(f"{self.token_atual} token atual")
        if self.token_atual == 'if':
            self.match('if')
            self.match('(')
            self.parse_CONDICAO()
            self.match(')')
            self.match('{')
            self.parse_CMDS()
            self.match('}')
            self.parse_PFALSA()

        elif self.token_atual == 'while':
            self.match('while')
            self.match('(')
            self.parse_CONDICAO()
            self.match(')')
            self.match('{')
            self.parse_CMDS()
            self.match('}')

        elif self.token_atual == 'System.out.println':
            self.match('System.out.println')
            self.match('(')
            self.parse_EXPRESSAO()
            self.match(')')
            self.match(';')

        elif self.token_atual == 'id':
            self.match('id')
            self.parse_RESTO_IDENT()
        
        else:
            self.error("Erro de sintaxe em CMD")
        print(f'Funcao: parse_CMD, finalizada.\n')

    def parse_PFALSA(self):
        """Funcao para o nao-terminal PFALSA."""
        self.funcao_atual = 'parse_PFALSA'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == 'else':
            self.match('else')
            self.match('{')
            self.parse_CMDS()
            self.match('}')
        elif self.token_atual in [';', '}']:
              # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em PFALSA: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_PFALSA, finalizada.\n')

    def parse_RESTO_IDENT(self):
        """Funcao para o nao-terminal RESTO_IDENT."""
        self.funcao_atual = 'parse_RESTO_IDENT'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == '=':
            self.match('=')
            self.parse_EXP_IDENT()
        elif self.token_atual == '(':
            self.match('(')
            self.parse_LISTA_ARG()
            self.match(')')
        else:
            self.error(f"Erro de sintaxe em RESTO_IDENT: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_RESTO_IDENT, finalizada.\n')


    def parse_LISTA_ARG(self):
        """Funcao para o nao-terminal LISTA_ARG."""
        self.funcao_atual = 'parse_LISTA_ARG'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == 'id':
            self.parse_ARGUMENTOS()
        elif self.token_atual == ')':  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em LISTA_ARG: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_LISTA_ARG, finalizada.\n')


    def parse_ARGUMENTOS(self):
        """Funcao para o nao-terminal ARGUMENTOS."""
        self.funcao_atual = 'parse_ARGUMENTOS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        self.match('id')
        self.parse_MAIS_IDENT()
        print(f'Funcao: parse_ARGUMENTOS, finalizada.\n')



    def parse_MAIS_IDENT(self):
        """Funcao para o nao-terminal MAIS_IDENT."""
        self.funcao_atual = 'parse_MAIS_IDENT'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == ',':
            self.match(',')
            self.parse_ARGUMENTOS()
        elif self.token_atual == ')':  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em MAIS_IDENT: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_MAIS_IDENT, finalizada.\n')


    def parse_EXP_IDENT(self):
        """Funcao para o nao-terminal EXP_IDENT."""
        self.funcao_atual = 'parse_EXP_IDENT'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual in ['id', 'num', '(']:
            self.parse_EXPRESSAO()
        elif self.token_atual == 'lerDouble()':
            self.match('lerDouble()')
        else:
            self.error(f"Erro de sintaxe em EXP_IDENT: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_EXP_IDENT, finalizada.\n')


    def parse_CONDICAO(self):
        """Funcao para o nao-terminal CONDICAO."""
        self.funcao_atual = 'parse_CONDICAO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        self.parse_EXPRESSAO()
        self.parse_RELACAO()
        self.parse_EXPRESSAO()
        print(f'Funcao: parse_CONDICAO, finalizada.\n')



    def parse_RELACAO(self):
        """Funcao para o nao-terminal RELACAO."""
        self.funcao_atual = 'parse_RELACAO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual in ['==', '!=', '>=', '<=', '>', '<']:
            self.match(self.token_atual)
        else:
            self.error(f"Erro de sintaxe em RELACAO: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_RELACAO, finalizada.\n')


    def parse_EXPRESSAO(self):
        """Funcao para o nao-terminal EXPRESSAO."""
        self.funcao_atual = 'parse_EXPRESSAO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        self.parse_TERMO()
        self.parse_OUTROS_TERMOS()
        print(f'Funcao: parse_EXPRESSAO, finalizada.\n')


    def parse_TERMO(self):
        """Funcao para o nao-terminal TERMO."""
        self.funcao_atual = 'parse_TERMO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        self.parse_OP_UN()
        self.parse_FATOR()
        self.parse_MAIS_FATORES()
        print(f'Funcao: parse_TERMO, finalizada.\n')


    def parse_OP_UN(self):
        """Funcao para o nao-terminal OP_UN."""
        self.funcao_atual = 'parse_OP_UN'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == '-':
            self.match('-')
        elif self.token_atual in ['id', 'num', '(']:  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em OP_UN: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_OP_UN, finalizada.\n')


    def parse_FATOR(self):
        """Funcao para o nao-terminal FATOR."""
        self.funcao_atual = 'parse_FATOR'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual == 'id':
            self.match('id')
        elif self.token_atual == 'num':
            self.match('num')
        elif self.token_atual == '(':
            self.match('(')
            self.parse_EXPRESSAO()
            self.match(')')
        else:
            self.error(f"Erro de sintaxe em FATOR: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_FATOR, finalizada.\n')


    def parse_MAIS_FATORES(self):
        """Funcao para o nao-terminal MAIS_FATORES."""
        self.funcao_atual = 'parse_MAIS_FATORES'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual in ['*', '/']:
            self.parse_OP_MUL()
            self.parse_MAIS_FATORES()
        elif self.token_atual in ['id','num', '(']:
            self.parse_FATOR()
            self.parse_MAIS_FATORES()
        elif self.token_atual in [';', ')', ']', '==', '!=', '>=', '<=', '>', '<', '}', '+','-']:  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em MAIS_FATORES: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_MAIS_FATORES, finalizada.\n')


    def parse_OUTROS_TERMOS(self):
        """Funcao para o nao-terminal OUTROS_TERMOS."""
        self.funcao_atual = 'parse_OUTROS_TERMOS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual in ['+', '-']:
            self.parse_OP_AD()
            self.parse_TERMO()
            self.parse_OUTROS_TERMOS()
        elif self.token_atual in [';', ')', ']', '==', '!=', '>=', '<=', '>', '<', '}']:  # Caminho nulo (λ)
            return
        else:
            self.error(f"Erro de sintaxe em OUTROS_TERMOS: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_OUTROS-TERMOS, finalizada.\n')


    def parse_OP_AD(self):
        """Funcao para o nao-terminal OP_AD."""
        self.funcao_atual = 'parse_OP_AD'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual in ['+', '-']:
            self.match(self.token_atual)
        else:
            self.error(f"Erro de sintaxe em OP_AD: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_OP_AD, finalizada.\n')


    def parse_OP_MUL(self):
        """Funcao para o nao-terminal OP_MUL."""
        self.funcao_atual = 'parse_OP_MUL'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        if self.token_atual in ['*', '/']:
            self.match(self.token_atual)
        else:
            self.error(f"Erro de sintaxe em OP_MUL: \"{self.token_atual}\" nao correspondido")
        print(f'Funcao: parse_OP_MUL, finalizada.\n')

