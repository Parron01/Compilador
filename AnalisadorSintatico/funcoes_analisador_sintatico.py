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
                # Códigos para impressão da arvore criada, basta descomentar
                # ast_dict = self.ast.to_dict()
                # ast_json = json.dumps(ast_dict, indent=4, ensure_ascii=False)
                # print("AST Gerada:")
                # print(ast_json)
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
        """Função para o não-terminal PROG."""
        self.funcao_atual = 'parse_PROG'
        print(f'\nIniciou a Função: {self.funcao_atual}')
        self.match('public')
        self.match('class')
        class_name = self.match('id')  # Captura o nome da classe
        self.match('{')
        self.match('public')
        self.match('static')
        self.match('void')
        method_name = self.match('main')  # Nome do método principal
        self.match('(')
        self.match('String')
        self.match('[')
        self.match(']')
        param_name = self.match('id')  # Nome do parâmetro do main
        self.match(')')
        self.match('{')
        
        # Analisar declarações de variáveis no main
        var_declarations = self.parse_DC()
        
        # Analisar comandos no main
        main_commands = self.parse_CMDS()
        self.match('}')
        
        # Criar o nó do método principal
        return_type = TypeNode('void')
        param_type = TypeNode('String[]')
        params = [ParamNode(param_type, param_name)]
        return_expression = None  # O main não possui expressão de retorno

        main_method_node = MethodNode(return_type, method_name, params, var_declarations, main_commands, return_expression)
        
        # Coletar outros métodos
        methods = []
        while self.token_atual[1] == 'public':
            method_node = self.parse_METODO()
            if method_node:
                methods.append(method_node)
        
        self.match('}')
        print(f'Função: parse_PROG, finalizada.\n')

        # Criar o nó raiz do programa
        self.ast = ProgramNode(main_method_node, methods)


    def parse_METODO(self):
        """Função para o não-terminal METODO."""
        self.funcao_atual = 'parse_METODO'
        print(f'\nIniciou a Função: {self.funcao_atual}')
        
        token_type, token_value = self.token_atual
        
        if token_value == 'public':
            self.match('public')
            self.match('static')
            return_type = self.parse_TIPO()
            method_name = self.match('id')
            self.match('(')
            params = self.parse_PARAMS()
            self.match(')')
            self.match('{')
            
            var_declarations = self.parse_DC()
            commands = self.parse_CMDS()
            self.match('return')
            return_expression = self.parse_EXPRESSAO()
            self.match(';')
            self.match('}')
            
            print(f'Função: parse_METODO, finalizada.\n')
            return MethodNode(return_type, method_name, params, var_declarations, commands, return_expression)
        elif token_value == '}':
            return None
        else:
            self.error(f"Erro de sintaxe em METODO: \"{token_value}\" não correspondido")



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
        token_type, token_value = self.token_atual  # Adicionado

        if token_value == ',':
            self.match(',')
            mais_params += self.parse_PARAMS()  # Adiciona os próximos parâmetros
        elif token_value == ')':  # Caminho nulo (λ)
            return mais_params  # Nenhum parâmetro adicional
        else:
            self.error(f"Erro de sintaxe em MAIS_PARAMS: \"{self.token_atual}\" nao correspondido")
        
        print(f'Funcao: parse_MAIS_PARAMS, finalizada.\n')
        return mais_params

    def parse_DC(self):
        """Funcao para o nao-terminal DC."""
        self.funcao_atual = 'parse_DC'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        declarations = []
        token_type, token_value = self.token_atual
        
        while token_value == 'double':
            var_decl_node = self.parse_VAR()
            declarations.append(var_decl_node)
            token_type, token_value = self.token_atual  # Atualiza o token atual
        
        print(f'Funcao: parse_DC, finalizada.\n')
        return declarations  # Retorna a lista de declarações (pode ser vazia)


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
        """Função para o não-terminal CMDS."""
        self.funcao_atual = 'parse_CMDS'
        print(f'\nIniciou a Função: {self.funcao_atual}')
        
        commands = []
        
        while True:
            token_type, token_value = self.token_atual
            
            if token_value == 'System.out.println' or token_type == 'id':
                cmd_node = self.parse_CMD()
                commands.append(cmd_node)
                if self.token_atual[1] == ';':
                    self.match(';')
                else:
                    self.error(f"Erro de sintaxe em CMDS: esperado ';', mas encontrado '{self.token_atual[1]}'")
            elif token_value in ['if', 'while']:
                cmd_cond_node = self.parse_CMD_COND()
                commands.append(cmd_cond_node)
            elif token_value == 'double':
                var_decl_node = self.parse_VAR()
                commands.append(var_decl_node)
            elif token_value in ['}', 'return']:
                break  # Fim dos comandos
            else:
                self.error(f"Erro de sintaxe em CMDS: comando não reconhecido '{token_value}'")
        
        print(f'Função: parse_CMDS, finalizada.\n')
        return commands
    
    def parse_CMD_COND(self):
        """Funcao para o nao-terminal CMD_COND."""
        self.funcao_atual = 'parse_CMD_COND'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        token_type, token_value = self.token_atual
        
        if token_value == 'if':
            self.match('if')
            self.match('(')
            condition = self.parse_CONDICAO()
            self.match(')')
            self.match('{')
            if_commands = self.parse_CMDS()
            self.match('}')
            else_commands = self.parse_PFALSA()
            print(f'Funcao: parse_CMD_COND, finalizada.\n')
            return IfNode(condition, if_commands, else_commands)
        elif token_value == 'while':
            self.match('while')
            self.match('(')
            condition = self.parse_CONDICAO()
            self.match(')')
            self.match('{')
            while_commands = self.parse_CMDS()
            self.match('}')
            print(f'Funcao: parse_CMD_COND, finalizada.\n')
            return WhileNode(condition, while_commands)
        else:
            self.error(f"Erro de sintaxe em CMD_COND: esperado 'if' ou 'while', mas encontrado '{token_value}'")


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
        token_type, token_value = self.token_atual
        
        if token_value == 'System.out.println':
            self.match('System.out.println')
            self.match('(')
            expression = self.parse_EXPRESSAO()
            self.match(')')
            print(f'Funcao: parse_CMD, finalizada.\n')
            return PrintNode(expression)
        elif token_type == 'id':
            var_name = self.match('id')
            rest_node = self.parse_RESTO_IDENT(var_name)
            print(f'Funcao: parse_CMD, finalizada.\n')
            return rest_node
        else:
            self.error(f"Erro de sintaxe em CMD: esperado 'System.out.println' ou 'id', mas encontrado '{token_value}'")

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


    def parse_RESTO_IDENT(self, var_name):
        """Função para o não-terminal RESTO_IDENT."""
        self.funcao_atual = 'parse_RESTO_IDENT'
        print(f'\nIniciou a Função: {self.funcao_atual}')
        
        token_type, token_value = self.token_atual
        
        if token_value == '=':
            self.match('=')
            expr_node = self.parse_EXP_IDENT()
            print(f'Função: parse_RESTO_IDENT, finalizada.\n')
            return AssignmentNode(var_name, expr_node)
        elif token_value == '(':
            self.match('(')
            arguments = self.parse_LISTA_ARG()
            self.match(')')
            print(f'Função: parse_RESTO_IDENT, finalizada.\n')
            return FunctionCallNode(var_name, arguments)
        else:
            self.error(f"Erro de sintaxe em RESTO_IDENT: esperado '=' ou '(', mas encontrado \"{token_value}\"")
        
        print(f'Função: parse_RESTO_IDENT, finalizada.\n')


    def parse_LISTA_ARG(self):
        """Funcao para o nao-terminal LISTA_ARG."""
        self.funcao_atual = 'parse_LISTA_ARG'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        arguments = []
        
        token_type, token_value = self.token_atual

        if token_type == 'id':
            arguments = self.parse_ARGUMENTOS()  # parse_ARGUMENTOS retorna uma lista de argumentos
        elif token_value == ')':  # Caminho nulo (λ)
            print(f'Funcao: parse_LISTA_ARG, finalizada (Produção Nula).\n')
            return arguments
        else:
            self.error(f"Erro de sintaxe em LISTA_ARG: esperado 'id' ou ')', mas encontrado '{token_value}'")
        
        print(f'Funcao: parse_LISTA_ARG, finalizada.\n')
        return arguments


    def parse_ARGUMENTOS(self):
        """Funcao para o nao-terminal ARGUMENTOS."""
        self.funcao_atual = 'parse_ARGUMENTOS'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        arguments = []
        argument = VariableNode(self.match('id'))  # Captura o nome real do argumento
        arguments.append(argument)
        additional_arguments = self.parse_MAIS_IDENT()  # Processa argumentos adicionais
        arguments.extend(additional_arguments)
        
        print(f'Funcao: parse_ARGUMENTOS, finalizada.\n')
        return arguments



    def parse_MAIS_IDENT(self):
        """Funcao para o nao-terminal MAIS_IDENT."""
        self.funcao_atual = 'parse_MAIS_IDENT'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')
        
        additional_arguments = []
        
        token_type, token_value = self.token_atual
        if token_value == ',':
            self.match(',')
            arguments = self.parse_ARGUMENTOS()  # parse_ARGUMENTOS retorna uma lista
            additional_arguments.extend(arguments)
        elif token_value == ')':  # Caminho nulo (λ)
            print(f'Funcao: parse_MAIS_IDENT, finalizada (Produção Nula).\n')
            return additional_arguments
        else:
            self.error(f"Erro de sintaxe em MAIS_IDENT: esperado ',' ou ')', mas encontrado '{token_value}'")
        
        print(f'Funcao: parse_MAIS_IDENT, finalizada.\n')
        return additional_arguments


    def parse_EXP_IDENT(self):
        """Funcao para o nao-terminal EXP_IDENT."""
        self.funcao_atual = 'parse_EXP_IDENT'
        print(f'\nIniciou a Funcao: {self.funcao_atual}')

        if self.token_atual[1] == 'lerDouble()':
            self.match('lerDouble()')  # Consome o token 'lerDouble()'
            print(f'Funcao: parse_EXP_IDENT, finalizada.\n')
            return FunctionCallNode('lerDouble', [])
        else:
            expr_node = self.parse_EXPRESSAO()
            print(f'Funcao: parse_EXP_IDENT, finalizada.\n')
            return expr_node




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
            self.match('-')  # Consome o operador unário '-'
            print(f'Funcao: parse_OP_UN, finalizada.\n')
            return '-'  # Retorna o operador unário

        # Caso o token seja 'id', 'num', ou '(' (um token válido para continuar a expressão)
        elif token_type in ['id', 'num'] or token_value == '(':
            print(f'Funcao: parse_OP_UN, finalizada (Produção Nula).\n')
            return None  # Produção nula (λ)

        # Em caso de erro de sintaxe
        else:
            self.error(f"Erro de sintaxe em OP_UN: esperado '-' ou expressão válida, mas encontrado \"{token_value}\"")

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

        token_type, token_value = self.token_atual  # Desempacota o token atual

        if token_value in ['*', '/']:
            operator = token_value  # Captura o valor do operador
            self.match(token_value)  # Consome o operador multiplicativo
            print(f'Funcao: parse_OP_MUL, finalizada.\n')
            return operator  # Retorna o operador multiplicativo
        else:
            self.error(f"Erro de sintaxe em OP_MUL: esperado '*' ou '/', mas encontrado \"{token_value}\" do tipo \"{token_type}\"")

