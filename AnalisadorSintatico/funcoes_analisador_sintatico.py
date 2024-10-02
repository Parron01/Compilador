import inspect
import pickle
from .ArvoreSintaticaAbstrata import *  # Importando todas as classes necessárias da AST
import json  # Para serializar a AST em JSON

class Parser:
    def __init__(self, ListaTokens):
        self.tokens = ListaTokens
        self.indice_atual_token = 0
        self.token_atual = self.tokens[self.indice_atual_token]
        self.contador_token = 1  # Contador de tokens que chama match
        self.erro = False
        self.ast = None  # Armazenará a AST completa do programa
        self.last_matched_id = None
    
    def save_ast_to_pickle(self, filename='ast_output.pickle'):
        """Salva a AST em um arquivo binário utilizando pickle."""
        if self.ast:
            with open(filename, 'wb') as file:
                pickle.dump(self.ast, file)  # Salva a AST no formato binário com pickle
                print(f"AST salva com sucesso no arquivo {filename}")
        else:
            print("Erro: AST não foi gerada corretamente.")

    def advance(self):
        """Avança para o próximo token da lista de tokens provindas do léxico."""
        self.indice_atual_token += 1
        if self.indice_atual_token < len(self.tokens):
            self.token_atual = self.tokens[self.indice_atual_token]
        else:
            self.token_atual = (None, None)

    def match(self, token_esperado):
        """Confere se o token atual corresponde ao esperado e avança se corresponder."""
        self.contador_token += 1
        token_type, token_value = self.token_atual
        funcao_chamadora = inspect.stack()[1].function
        print(f"{self.contador_token}:token atual = `{token_value}`")

        if token_esperado == token_type or token_esperado == token_value:
            print(f"{self.contador_token}:Token {self.contador_token}: \"{token_value}\" correspondido com sucesso pela função = {funcao_chamadora}")
            # Armazena o identificador se o token esperado for 'id'
            if token_esperado == 'id':
                self.last_matched_id = token_value
            self.advance()
            return token_value  # Retorna o valor real do identificador ou número, se aplicável
        else:
            self.error(f"Erro de sintaxe na função: {self.funcao_atual}. Esperado '{token_esperado}', encontrado '{token_value}' no token {self.contador_token}.")


    def error(self, message):
        raise Exception(message)


    def parse_PROG(self):
        """Funcao para o nao-terminal PROG."""
        self.funcao_atual = 'parse_PROG'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        # Montando a AST
        self.match('public')
        self.match('class')
        class_name = self.match('id')  # Armazenar o nome real da classe
        self.match('{')

        # Parse da main
        self.match('public')
        self.match('static')
        self.match('void')
        self.match('main')
        self.match('(')
        self.match('String')
        self.match('[')
        self.match(']')
        main_arg = self.match('id')  # Armazenar o argumento real
        self.match(')')
        self.match('{')

        main_commands = self.parse_CMDS()
        self.match('}')
        
        # Parse dos métodos (pode retornar None, então devemos inicializar como uma lista vazia)
        methods = []
        metodo = self.parse_METODO()
        if metodo:  # Se um método for encontrado, adicione à lista
            methods.append(metodo)

        self.match('}')
        
        # Criação do nó da AST ProgramNode
        self.ast = ProgramNode(main_class=main_commands, methods=methods if methods else [])
        
        print(f'Funcao: parse_PROG, finalizada.\n')

    def parse_METODO(self):
        """Função para o não-terminal METODO."""
        self.funcao_atual = 'parse_METODO'
        print(f'\nIniciou a Função: {self.funcao_atual}')
        
        token_type, token_value = self.token_atual  # Desempacota o tipo e valor do token atual
        
        # Verifica se é o início de um método
        if token_value == 'public':  # Compara o valor do token, pois 'public' é uma palavra reservada
            self.match('public')
            self.match('static')
            return_type = self.parse_TIPO()  # Tipo de retorno
            method_name = self.match('id')  # Nome real do método
            self.match('(')
            params = self.parse_PARAMS()
            self.match(')')
            self.match('{')
            
            var_declarations = self.parse_DC()  # Declarações de variáveis
            commands = self.parse_CMDS()  # Comandos
            self.match('return')
            return_expression = self.parse_EXPRESSAO()  # Expressão de retorno
            self.match(';')
            self.match('}')
            
            # Criação do nó MethodNode
            return MethodNode(return_type, method_name, params, var_declarations, commands, return_expression)
        elif token_value == '}':  # Caminho nulo (λ)
            return None
        else:
            self.error(f"Erro de sintaxe em METODO: \"{self.token_atual}\" não correspondido")
        print(f'Função: parse_METODO, finalizada.\n')



    def parse_TIPO(self):
        """Funcao para o nao-terminal TIPO."""
        self.funcao_atual = 'parse_TIPO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        token_type, token_value = self.token_atual  # Captura o tipo e valor do token atual
        
        if token_value == 'double':
            self.match('double')  # Verifica e consome o token 'double'
            # Criando um nó para o tipo
            tipo_node = TypeNode('double')
            print(f'Funcao: parse_TIPO, finalizada.\n')
            return tipo_node
        else:
            self.error(f"Erro de sintaxe em TIPO: \"{self.token_atual}\" nao correspondido")

    def parse_PARAMS(self):
        """Funcao para o nao-terminal PARAMS."""
        self.funcao_atual = 'parse_PARAMS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        params = []
        
        token_type, token_value = self.token_atual  # Obtém o tipo e valor do token atual
        
        # Verifica se o tipo do parâmetro é um tipo esperado, como 'double'
        if token_value == 'double':
            tipo = self.parse_TIPO()  # Tipo do parâmetro
            param_name = self.match('id')  # Armazena o nome real do identificador
            params.append(ParamNode(tipo, param_name))  # Adiciona o parâmetro à lista
            
            # Verifica se existem mais parâmetros
            mais_params = self.parse_MAIS_PARAMS()
            if mais_params:
                params += mais_params  # Adiciona mais parâmetros se houver
        
        # Caminho nulo (λ) quando o token é ')', o que significa que não há mais parâmetros
        elif token_value == ')':
            return params  # Retorna uma lista vazia ou com os parâmetros capturados
        
        else:
            self.error(f"Erro de sintaxe em PARAMS: esperado um tipo de parâmetro, encontrado '{token_value}'")
        
        print(f'Funcao: parse_PARAMS, finalizada.\n')
        return params


    def parse_MAIS_PARAMS(self):
        """Funcao para o nao-terminal MAIS_PARAMS."""
        self.funcao_atual = 'parse_MAIS_PARAMS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        mais_params = []
        
        if self.token_atual == ',':
            self.match(',')
            mais_params += self.parse_PARAMS()  # Adiciona os próximos parâmetros
        elif self.token_atual == ')':  # Caminho nulo (λ)
            return mais_params  # Nenhum parâmetro adicional
        else:
            self.error(f"Erro de sintaxe em MAIS_PARAMS: \"{self.token_atual}\" nao correspondido")
        
        print(f'Funcao: parse_MAIS_PARAMS, finalizada.\n')
        return mais_params

    def parse_DC(self):
        """Funcao para o nao-terminal DC."""
        self.funcao_atual = 'parse_DC'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        var_declarations = []  # Lista de declarações de variáveis
        
        token_type, token_value = self.token_atual  # Captura o tipo e valor do token atual
        
        if token_value == 'double':  # Verifica se o valor do token é 'double'
            var_declarations.append(self.parse_VAR())  # Adiciona declaração de variável
            var_declarations.extend(self.parse_MAIS_DC())  # Adiciona mais declarações, se houver
        elif token_value in ['}', 'return']:  # Caminho nulo (λ) - se encontrar '}' ou 'return'
            return var_declarations  # Retorna a lista de declarações vazia ou preenchida
        else:
            self.error(f"Erro de sintaxe em DC: \"{self.token_atual}\" nao correspondido")
        
        print(f'Funcao: parse_DC, finalizada.\n')
        return var_declarations  # Retorna as declarações de variáveis



    def parse_MAIS_DC(self):
        """Funcao para o nao-terminal MAIS_DC."""
        self.funcao_atual = 'parse_MAIS_DC'
        
        declarations = []
        
        if self.token_atual == 'double':
            declarations += self.parse_DC()  # Adiciona mais declarações
        elif self.token_atual != 'double':  # Produção nula (λ)
            return declarations
        else:
            self.error(f"Erro de sintaxe em MAIS_DC: \"{self.token_atual}\" nao correspondido")
        
        print(f'Funcao: parse_MAIS_DC, finalizada.\n')
        return declarations


    def parse_VAR(self):
        """Funcao para o nao-terminal VAR."""
        self.funcao_atual = 'parse_VAR'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        var_type = self.parse_TIPO()  # Obtenha o tipo da variável
        var_names = self.parse_VARS()  # Obtenha os nomes das variáveis
        self.match(';')
        
        var_decl_node = VarDeclarationNode(var_type, var_names)  # Criação do nó AST para VarDeclarationNode
        
        print(f'Funcao: parse_VAR, finalizada.\n')
        return var_decl_node



    def parse_VARS(self):
        """Funcao para o nao-terminal VARS."""
        self.funcao_atual = 'parse_VARS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        var_names = [self.match('id')]  # Captura o nome real da variável
        
        additional_vars = self.parse_MAIS_VAR()
        var_names.extend(additional_vars)
        
        print(f'Funcao: parse_VARS, finalizada.\n')
        return var_names


    def parse_MAIS_VAR(self):
        """Funcao para o nao-terminal MAIS_VAR."""
        self.funcao_atual = 'parse_MAIS_VAR'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        var_names = []
        
        if self.token_atual[0] == ',':  # Verifica se o token é uma vírgula
            self.match(',')  # Consome a vírgula
            var_names = self.parse_VARS()  # Continua a análise para mais variáveis
        
        elif self.token_atual[0] == ';':  # Caminho nulo (λ), pois o ';' encerra a declaração de variáveis
            return var_names  # Retorna a lista de nomes de variáveis (pode ser vazia)

        else:
            token_type, token_value = self.token_atual
            self.error(f"Erro de sintaxe em MAIS_VAR: Esperado ',' ou ';', mas encontrado '{token_value}' do tipo '{token_type}'")
        
        print(f'Funcao: parse_MAIS_VAR, finalizada.\n')
        return var_names



    def parse_CMDS(self):
        """Funcao para o nao-terminal CMDS."""
        self.funcao_atual = 'parse_CMDS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        commands = []
        
        # Captura o tipo e valor do token atual
        token_type, token_value = self.token_atual
        
        # Verifica se é um comando ou uma declaração de variável
        if token_value in ['if', 'while', 'System.out.println'] or token_type == 'id':
            cmd_node = self.parse_CMD()
            commands.append(cmd_node)
            commands += self.parse_MAIS_CMDS()  # Adiciona comandos adicionais
        
        # Verifica se é uma declaração de variável (por exemplo, 'double')
        elif token_value in ['double']:
            var_decl_node = self.parse_VAR()
            commands.append(var_decl_node)
            commands += self.parse_MAIS_CMDS()
        
        # Caminho nulo (λ) - fim de comandos
        elif token_value in ['}', 'return']:
            return commands
        
        else:
            self.error(f"Erro de sintaxe em CMDS: esperado comando ou declaração de variável, mas encontrado \"{self.token_atual}\"")
        
        print(f'Funcao: parse_CMDS, finalizada.\n')
        return commands

    def parse_MAIS_CMDS(self):
        """Funcao para o nao-terminal MAIS_CMDS."""
        self.funcao_atual = 'parse_MAIS_CMDS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        additional_cmds = []
        
        # Verifica o tipo e valor do token
        token_type, token_value = self.token_atual
        
        # Verifica o ponto e vírgula e processa os próximos comandos
        if token_value == ';':
            self.match(';')  # Verifica o ponto e vírgula como valor
            additional_cmds += self.parse_CMDS()  # Adiciona os comandos seguintes
        elif token_value in ["if", "while", "System.out.println"] or token_type == 'id':
            additional_cmds += self.parse_CMDS()  # Adiciona os comandos seguintes
        elif token_value in ['}', 'return']:  # Produção nula (λ)
            return additional_cmds
        else:
            self.error(f"Erro de sintaxe em MAIS_CMDS: \"{token_value}\" não correspondido")
        
        print(f'Funcao: parse_MAIS_CMDS, finalizada.\n')
        return additional_cmds



    def parse_CMD(self):
        """Funcao para o nao-terminal CMD."""
        self.funcao_atual = 'parse_CMD'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        token_type, token_value = self.token_atual  # Captura o tipo e valor do token atual
        
        if token_type == 'if':
            self.match('if')
            self.match('(')
            condition = self.parse_CONDICAO()  # Condição do 'if'
            self.match(')')
            self.match('{')
            if_commands = self.parse_CMDS()  # Comandos dentro do 'if'
            self.match('}')
            else_commands = self.parse_PFALSA()  # Comandos do 'else'
            return IfNode(condition, if_commands, else_commands)  # Criação do nó 'IfNode'

        elif token_type == 'while':
            self.match('while')
            self.match('(')
            condition = self.parse_CONDICAO()  # Condição do 'while'
            self.match(')')
            self.match('{')
            commands = self.parse_CMDS()  # Comandos dentro do 'while'
            self.match('}')
            return WhileNode(condition, commands)  # Criação do nó 'WhileNode'

        elif token_type == 'System.out.println':
            self.match('System.out.println')
            self.match('(')
            expression = self.parse_EXPRESSAO()  # Expressão a ser impressa
            self.match(')')
            self.match(';')
            return PrintNode(expression)  # Criação do nó 'PrintNode'

        elif token_type == 'id':
            var_name = self.match('id')
            next_token_type, next_token_value = self.token_atual
            if next_token_value == '=':
                self.match('=')
                expr_node = self.parse_EXP_IDENT()
                self.match(';')
                return AssignmentNode(var_name, expr_node)
            elif next_token_value == '(':
                self.match('(')
                arguments = self.parse_LISTA_ARG()
                self.match(')')
                self.match(';')
                return FunctionCallNode(var_name, arguments)
            else:
                self.error(f"Erro de sintaxe em CMD: esperado '=' ou '(', mas encontrado '{next_token_value}'")
        
        else:
            self.error("Erro de sintaxe em CMD")
        
        print(f'Funcao: parse_CMD, finalizada.\n')

    def parse_PFALSA(self):
        """Funcao para o nao-terminal PFALSA."""
        self.funcao_atual = 'parse_PFALSA'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        token_type, token_value = self.token_atual  # Captura o tipo e o valor do token

        # Verifica se o token é a palavra-chave 'else'
        if token_value == 'else':
            self.match('else')  # Consome o token 'else'
            self.match('{')  # Consome a abertura de chave
            else_commands = self.parse_CMDS()  # Comandos dentro do bloco 'else'
            self.match('}')  # Consome o fechamento de chave
            return else_commands  # Retorna os comandos do 'else'
        
        # Produção nula (λ) quando o próximo token é ';' ou '}'
        elif token_value in [';', '}']:
            return None
        
        # Caso contrário, erro de sintaxe
        else:
            self.error(f"Erro de sintaxe em PFALSA: esperado 'else', ';' ou '}}', mas encontrado \"{token_value}\" do tipo \"{token_type}\"")
        
        print(f'Funcao: parse_PFALSA, finalizada.\n')
        return None


    def parse_RESTO_IDENT(self):
        """Função para o não-terminal RESTO_IDENT."""
        self.funcao_atual = 'parse_RESTO_IDENT'
        print(f'\nIniciou a Função: {self.funcao_atual}')
        
        token_type, token_value = self.token_atual  # Captura o tipo e valor do token atual
        
        # Tratamento de atribuição (operador '='):
        if token_value == '=':
            self.match('=')  # Verifica o operador de atribuição
            expr_node = self.parse_EXP_IDENT()  # Captura a expressão após o '='
            print(f'Função: parse_RESTO_IDENT, finalizada.\n')
            return expr_node  # Retorna a expressão; o AssignmentNode será criado em parse_CMD()
        
        # Tratamento de chamada de função (parênteses '('):
        elif token_value == '(':
            self.match('(')  # Consome o parêntese de abertura
            
            # Captura a lista de argumentos
            arguments = self.parse_LISTA_ARG()
            
            # Verifica o parêntese de fechamento
            token_type, token_value = self.token_atual  # Atualiza o token atual
            if token_value == ')':
                self.match(')')
            else:
                self.error(f"Erro de sintaxe: esperado ')' mas encontrado '{token_value}' no token {self.contador_token}")
            
            # Retorna o nó de chamada de função com o nome correto
            function_call_node = FunctionCallNode(self.last_matched_id, arguments)
            print(f'Função: parse_RESTO_IDENT, finalizada.\n')
            return function_call_node
        
        else:
            self.error(f"Erro de sintaxe em RESTO_IDENT: \"{self.token_atual}\" não correspondido")
        
        print(f'Função: parse_RESTO_IDENT, finalizada.\n')


    def parse_LISTA_ARG(self):
        """Funcao para o nao-terminal LISTA_ARG."""
        self.funcao_atual = 'parse_LISTA_ARG'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        arguments = []
        
        if self.token_atual == 'id':
            arguments.append(self.parse_ARGUMENTOS())  # Adiciona os argumentos à lista
        elif self.token_atual == ')':  # Caminho nulo (λ)
            return arguments
        
        print(f'Funcao: parse_LISTA_ARG, finalizada.\n')
        return arguments


    def parse_ARGUMENTOS(self):
        """Funcao para o nao-terminal ARGUMENTOS."""
        self.funcao_atual = 'parse_ARGUMENTOS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        argument = VariableNode(self.match('id'))  # Captura o nome real do argumento
        self.parse_MAIS_IDENT()  # Processa argumentos adicionais
        
        print(f'Funcao: parse_ARGUMENTOS, finalizada.\n')
        return argument



    def parse_MAIS_IDENT(self):
        """Funcao para o nao-terminal MAIS_IDENT."""
        self.funcao_atual = 'parse_MAIS_IDENT'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        additional_arguments = []
        
        if self.token_atual == ',':
            self.match(',')
            additional_arguments.append(self.parse_ARGUMENTOS())  # Adiciona argumentos adicionais
        elif self.token_atual == ')':  # Caminho nulo (λ)
            return additional_arguments
        
        print(f'Funcao: parse_MAIS_IDENT, finalizada.\n')
        return additional_arguments


    def parse_EXP_IDENT(self):
        """Funcao para o nao-terminal EXP_IDENT."""
        self.funcao_atual = 'parse_EXP_IDENT'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')

        token_type, token_value = self.token_atual  # Captura o tipo e valor do token atual

        # Verifica se é um identificador, número ou expressão entre parênteses
        if token_type == 'id' or token_type == 'num' or token_value == '(':
            expr_node = self.parse_EXPRESSAO()  # Retorna o nó da expressão
            return expr_node

        # Verifica a chamada da função específica 'lerDouble()'
        elif token_value == 'lerDouble()':
            self.match('lerDouble()')
            return FunctionCallNode('lerDouble', [])  # Cria o nó de chamada da função 'lerDouble'

        # Tratamento de erro em caso de token não reconhecido
        else:
            self.error(f"Erro de sintaxe em EXP_IDENT: \"{token_value}\" não correspondido no token {self.contador_token}")
        
        print(f'Funcao: parse_EXP_IDENT, finalizada.\n')



    def parse_CONDICAO(self):
        """Funcao para o nao-terminal CONDICAO."""
        self.funcao_atual = 'parse_CONDICAO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        left_expr = self.parse_EXPRESSAO()  # Captura a expressão à esquerda
        operator = self.parse_RELACAO()  # Operador relacional
        right_expr = self.parse_EXPRESSAO()  # Captura a expressão à direita
        
        print(f'Funcao: parse_CONDICAO, finalizada.\n')
        return ConditionNode(left_expr, operator, right_expr)  # Cria o nó de condição



    def parse_RELACAO(self):
        """Funcao para o nao-terminal RELACAO."""
        self.funcao_atual = 'parse_RELACAO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        token_type, token_value = self.token_atual  # Captura o tipo e valor do token atual
        
        # Verifica se o valor do token é um operador relacional
        if token_value in ['==', '!=', '>=', '<=', '>', '<']:
            operator = token_value  # Captura o operador relacional
            self.match(token_value)  # Consome o operador usando o valor real do token
            print(f'Funcao: parse_RELACAO, finalizada.\n')
            return operator  # Retorna o operador relacional
        else:
            self.error(f"Erro de sintaxe em RELACAO: esperado um operador relacional, mas encontrado \"{self.token_atual}\"")

        print(f'Funcao: parse_RELACAO, finalizada.\n')




    def parse_EXPRESSAO(self):
        """Funcao para o nao-terminal EXPRESSAO."""
        self.funcao_atual = 'parse_EXPRESSAO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')

        termo_node = self.parse_TERMO()  # Obtenha o nó da expressão
        outros_termos_node = self.parse_OUTROS_TERMOS()  # Outros termos após o termo
        if outros_termos_node is not None:
            result_node = BinaryOperationNode(termo_node, outros_termos_node.operator, outros_termos_node.right)
        else:
            result_node = termo_node

        print(f'Funcao: parse_EXPRESSAO, finalizada.\n')
        return result_node  # Retorna o nó da expressão


    def parse_TERMO(self):
        """Funcao para o nao-terminal TERMO."""
        self.funcao_atual = 'parse_TERMO'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')

        op_un_node = self.parse_OP_UN()  # Operação unária se existir
        fator_node = self.parse_FATOR()  # Fator
        mais_fatores_node = self.parse_MAIS_FATORES()  # Possíveis fatores adicionais

        if op_un_node is not None:
            result_node = UnaryOperationNode(op_un_node, fator_node)
        else:
            result_node = fator_node

        if mais_fatores_node is not None:
            result_node = BinaryOperationNode(result_node, mais_fatores_node.operator, mais_fatores_node.right)

        print(f'Funcao: parse_TERMO, finalizada.\n')
        return result_node  # Retorna o nó do termo

    def parse_OP_UN(self):
        """Funcao para o nao-terminal OP_UN."""
        self.funcao_atual = 'parse_OP_UN'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')

        token_type, token_value = self.token_atual  # Captura o tipo e valor do token atual

        # Verifica se o operador unário é um sinal de menos '-'
        if token_value == '-':
            self.match('Operador')  # Consome o operador unário '-'
            print(f'Funcao: parse_OP_UN, finalizada.\n')
            return '-'  # Retorna o operador unário

        # Caso o token seja 'id', 'num', ou '(' (um token válido para continuar a expressão)
        elif token_type in ['id', 'num'] or token_value == '(':
            print(f'Funcao: parse_OP_UN, finalizada (Produção Nula).\n')
            return None  # Produção nula (λ)

        # Em caso de erro de sintaxe
        else:
            self.error(f"Erro de sintaxe em OP_UN: esperado '-' ou expressão válida, mas encontrado \"{self.token_atual}\"")

        print(f'Funcao: parse_OP_UN, finalizada.\n')




    def parse_FATOR(self):
        """Funcao para o nao-terminal FATOR."""
        self.funcao_atual = 'parse_FATOR'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')

        token_type, token_value = self.token_atual  # Captura o tipo e o valor real do token

        if token_type == 'id':
            var_name = self.match('id')  # Agora `match` retorna o valor real do identificador
            print(f'Funcao: parse_FATOR, finalizada.\n')
            return VariableNode(var_name)  # Cria nó de variável com o nome real
        elif token_type == 'num':
            num_value = self.match('num')  # Agora `match` retorna o valor real do número
            print(f'Funcao: parse_FATOR, finalizada.\n')
            return NumberNode(num_value)  # Cria nó de número com o valor real
        elif token_type == '(':
            self.match('(')
            expressao_node = self.parse_EXPRESSAO()  # Expressão dentro de parênteses
            self.match(')')
            print(f'Funcao: parse_FATOR, finalizada.\n')
            return expressao_node  # Retorna o nó da expressão
        else:
            self.error(f"Erro de sintaxe em FATOR: \"{token_value}\" nao correspondido")


    def parse_MAIS_FATORES(self):
        """Funcao para o nao-terminal MAIS_FATORES."""
        self.funcao_atual = 'parse_MAIS_FATORES'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')

        token_type, token_value = self.token_atual  # Captura o tipo e valor do token atual

        # Se encontrarmos '*' ou '/', processamos os fatores multiplicativos
        if token_value in ['*', '/']:
            operator = self.parse_OP_MUL()  # Operador multiplicativo
            fator_node = self.parse_FATOR()  # Fator adicional
            mais_fatores_node = self.parse_MAIS_FATORES()  # Outros fatores adicionais (recursão)
            print(f'Funcao: parse_MAIS_FATORES, finalizada.\n')
            return BinaryOperationNode(None, operator, fator_node)  # Cria nó de operação binária

        # Se encontrarmos tokens que indicam o fim de uma expressão, retornamos None
        elif token_value in [';', ')', ']', '==', '!=', '>=', '<=', '>', '<', '}', '+', '-']:
            print(f'Funcao: parse_MAIS_FATORES, finalizada com produção nula (null).\n')  # Substituído λ por "null"
            return None  # Produção nula

        # Caso contrário, temos um erro de sintaxe
        else:
            self.error(f"Erro de sintaxe em MAIS_FATORES: token inesperado \"{self.token_atual}\"")

        print(f'Funcao: parse_MAIS_FATORES, finalizada.\n')




    def parse_OUTROS_TERMOS(self):
        """Funcao para o nao-terminal OUTROS_TERMOS."""
        self.funcao_atual = 'parse_OUTROS_TERMOS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')

        token_type, token_value = self.token_atual  # Captura o tipo e valor do token atual

        if token_value in ['+', '-']:
            operator = self.parse_OP_AD()  # Operador aditivo
            termo_node = self.parse_TERMO()  # Termo adicional
            outros_termos_node = self.parse_OUTROS_TERMOS()  # Outros termos
            print(f'Funcao: parse_OUTROS_TERMOS, finalizada.\n')
            return BinaryOperationNode(None, operator, termo_node)  # Cria nó de operação binária

        # Verifica se o token atual é um delimitador válido (caminho nulo)
        elif token_value in [';', ')', ']', '==', '!=', '>=', '<=', '>', '<', '}']:
            print(f'Funcao: parse_OUTROS_TERMOS, finalizada (Produção Nula).\n')
            return None  # Produção nula (λ)

        # Em caso de erro de sintaxe
        else:
            self.error(f"Erro de sintaxe em OUTROS_TERMOS: esperado '+', '-', ou delimitador, mas encontrado \"{self.token_atual}\"")

        print(f'Funcao: parse_OUTROS_TERMOS, finalizada.\n')


    def parse_OP_AD(self):
        """Funcao para o nao-terminal OP_AD."""
        self.funcao_atual = 'parse_OP_AD'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')

        token_type, token_value = self.token_atual  # Captura o tipo e valor do token atual

        # Verifica se o valor do token é '+' ou '-'
        if token_value in ['+', '-']:
            operator = token_value  # Armazena o valor do operador ('+' ou '-')
            
            # A função match agora verifica diretamente o valor do token para operadores
            if token_type == 'Operador' or token_value in ['+', '-']:
                self.match(token_value)  # Usa o valor diretamente como parâmetro
            else:
                self.error(f"Erro de sintaxe na função: {self.funcao_atual}. Esperado operador '+' ou '-', mas encontrado \"{token_value}\" do tipo \"{token_type}\"")
            
            print(f'Funcao: parse_OP_AD, finalizada.\n')
            return operator  # Retorna o operador aditivo
        else:
            self.error(f"Erro de sintaxe em OP_AD: esperado '+' ou '-', mas encontrado \"{token_value}\" do tipo \"{token_type}\"")





    def parse_OP_MUL(self):
        """Funcao para o nao-terminal OP_MUL."""
        self.funcao_atual = 'parse_OP_MUL'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')

        if self.token_atual in ['*', '/']:
            operator = self.token_atual
            self.match(operator)
            print(f'Funcao: parse_OP_MUL, finalizada.\n')
            return operator  # Retorna o operador multiplicativo
        else:
            self.error(f"Erro de sintaxe em OP_MUL: \"{self.token_atual}\" nao correspondido")

