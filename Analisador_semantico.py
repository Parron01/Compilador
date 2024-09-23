from ArvoreSintaticaAbstrata import ProgramNode

class AnalisadorSemantico:
    def __init__(self):
        self.escopo_variaveis = {}  # Armazena as variáveis declaradas globalmente
        self.escopo_atual = {}  # Escopo local para cada método
        self.funcoes_declaradas = {
            'lerDouble': {'params': [], 'return_type': 'double'}  # 'lerDouble' retorna 'double'
        }
        self.erros_semanticos = []  # Lista para armazenar mensagens de erro

    def visitar(self, node):
        if isinstance(node, list):
            for subnode in node:
                self.visitar(subnode)
            return
        method_name = f'visitar_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.visitar_no_nao_definido)
        return visitor(node)

    def visitar_no_nao_definido(self, node):
        """Método chamado quando não há um método específico para o nó."""
        print(f"Semântica não definida para o nó: {node.__class__.__name__}")

    def visitar_ProgramNode(self, node):
        print("Analisando Programa...")
        # Registra as funções declaradas primeiro
        for metodo in node.methods:
            self.funcoes_declaradas[metodo.method_name] = {
                'params': metodo.params,
                'return_type': metodo.return_type.type_name
            }
        # Analisa o bloco principal (main_class)
        self.escopo_atual = {}
        self.visitar(node.main_class)
        # Analisa os métodos
        for metodo in node.methods:
            self.visitar(metodo)


    def visitar_MethodNode(self, node):
        print(f"Analisando Método: {node.method_name}")
        # Inicializa o escopo do método
        self.escopo_atual = {}  # Reseta o escopo para o método
        for param in node.params:
            self.visitar(param)
        # Analisa as declarações de variáveis
        for var_decl in node.var_declarations:
            self.visitar(var_decl)
        # Analisa os comandos no método
        for comando in node.commands:
            self.visitar(comando)
        # Analisa a expressão de retorno
        self.visitar(node.return_expression)

    def visitar_VarDeclarationNode(self, node):
        # Registra as variáveis no escopo atual (local ou global)
        var_type = self.visitar(node.var_type)
        print(f"Variáveis declaradas: {node.var_names} do tipo {var_type}")
        for var_name in node.var_names:
            if isinstance(node, ProgramNode):
                self.escopo_variaveis[var_name] = var_type  # Variável global
            else:
                self.escopo_atual[var_name] = var_type  # Variável local no método

    def visitar_TypeNode(self, node):
        # Retorna o nome do tipo
        return node.type_name

    def visitar_AssignmentNode(self, node):
        print(f"Atribuindo valor à variável: {node.var_name}")
        # Verifica se a variável está declarada no escopo local ou global
        if node.var_name in self.escopo_atual:
            var_type = self.escopo_atual[node.var_name]
        elif node.var_name in self.escopo_variaveis:
            var_type = self.escopo_variaveis[node.var_name]
        else:
            mensagem_erro = f"Erro semântico: Variável '{node.var_name}' não declarada."
            print(mensagem_erro)
            self.erros_semanticos.append(mensagem_erro)
            return
        # Analisa a expressão atribuída
        expr_type = self.visitar(node.expression)
        # Verifica se os tipos são compatíveis
        if var_type != expr_type and expr_type is not None:
            mensagem_erro = f"Erro semântico: Tipos incompatíveis. Variável '{node.var_name}' é do tipo '{var_type}', mas expressão é do tipo '{expr_type}'."
            print(mensagem_erro)
            self.erros_semanticos.append(mensagem_erro)


    def visitar_NumberNode(self, node):
        print(f"Verificando número: {node.value}")

    def visitar_VariableNode(self, node):
        if node.var_name not in self.escopo_atual and node.var_name not in self.escopo_variaveis:
            mensagem_erro = f"Erro semântico: Variável '{node.var_name}' não foi declarada."
            print(mensagem_erro)
            self.erros_semanticos.append(mensagem_erro)
            return None
        else:
            print(f"Verificando variável: {node.var_name}")
            return self.escopo_atual.get(node.var_name, self.escopo_variaveis.get(node.var_name))

    def visitar_BinaryOperationNode(self, node):
        print(f"Operação binária: {node.operator}")
        left_type = self.visitar(node.left)
        right_type = self.visitar(node.right)
        if left_type != right_type and left_type is not None and right_type is not None:
            mensagem_erro = f"Erro semântico: Operandos de tipos incompatíveis '{left_type}' e '{right_type}' na operação '{node.operator}'."
            print(mensagem_erro)
            self.erros_semanticos.append(mensagem_erro)
        return left_type  # Assume que o tipo resultante é o mesmo


    def visitar_ConditionNode(self, node):
        print(f"Condição: {node.operator}")
        self.visitar(node.left)
        self.visitar(node.right)

    def visitar_WhileNode(self, node):
        print("Analisando laço While")
        self.visitar(node.condition)
        for comando in node.commands:
            self.visitar(comando)

    def visitar_IfNode(self, node):
        print("Analisando condicional If")
        self.visitar(node.condition)
        # Analisa os comandos dentro do if
        for cmd in node.if_commands:
            self.visitar(cmd)
        # Analisa o else, se houver
        if node.else_commands:
            for cmd in node.else_commands:
                self.visitar(cmd)

    def visitar_FunctionCallNode(self, node):
        print(f"Chamada de função: {node.function_name}")
        if node.function_name in self.funcoes_declaradas:
            func_info = self.funcoes_declaradas[node.function_name]
            expected_params = func_info['params']
            # Verifica se o número de argumentos corresponde
            if len(node.arguments) != len(expected_params):
                mensagem_erro = f"Erro semântico: Função '{node.function_name}' esperava {len(expected_params)} argumentos, mas recebeu {len(node.arguments)}."
                print(mensagem_erro)
                self.erros_semanticos.append(mensagem_erro)
            else:
                # Opcional: Verificar tipos dos argumentos
                pass
            func_return_type = func_info['return_type']
            # Visitar os argumentos
            for arg in node.arguments:
                self.visitar(arg)
            return func_return_type
        else:
            mensagem_erro = f"Erro semântico: Função '{node.function_name}' não foi declarada."
            print(mensagem_erro)
            self.erros_semanticos.append(mensagem_erro)
            return None

    def visitar_UnaryOperationNode(self, node):
        print(f"Operação unária: {node.operator}")
        self.visitar(node.operand)

    def visitar_PrintNode(self, node):
        print("Verificando comando de impressão")
        self.visitar(node.expression)
