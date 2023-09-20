import sqlite3

TIPO_PESSOA = {
    'M': 1,  # Masculino
    'F': 2,  # Feminino
}

TIPO_DOCUMENTO = {
    11: 1,  # CPF
    14: 2,  # CNPJ
}

class Pessoas:
    def __init__(self, nome: str, sobrenome: str, idade: int, genero: str):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade
        self.genero = genero
    
    def getDados(self):
        dados = {
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "nome_completo": f"{self.nome} {self.sobrenome}",
            "idade": self.idade,
            "genero": self.genero}
        return dados

class PessoaPJ(Pessoas):
    def __init__(self, nome: str, sobrenome: str, idade: int, genero: str, cnpj: str):
        super().__init__(nome, sobrenome, idade, genero)
        self.cnpj = cnpj

    def getDados(self):
        dados = super().getDados()
        dados["cnpj"] = self.cnpj
        return dados

    def salvar_db(self, conn):
        tipo_pessoa = TIPO_PESSOA.get(self.genero, None)
        tipo_documento = TIPO_DOCUMENTO.get(len(self.cnpj), None)
        
        if tipo_pessoa is not None and tipo_documento is not None:
            sql = "INSERT INTO pessoas (nome, sobrenome, genero, idade, documento, tipo) VALUES (?, ?, ?, ?, ?, ?)"
            values = (self.nome, self.sobrenome, tipo_pessoa, self.idade, self.cnpj, tipo_documento)
            inserir_dados(conn, sql, values)
        else:
            print("Gênero ou documento inválido!")

class PessoaPF(Pessoas):
    def __init__(self, nome: str, sobrenome: str, idade: int, genero: str, cpf: str):
        super().__init__(nome, sobrenome, idade, genero)
        self.cpf = cpf

    def getDados(self):
        dados = super().getDados()
        dados["cpf"] = self.cpf
        return dados

    def salvar_db(self, conn):
        tipo_pessoa = TIPO_PESSOA.get(self.genero, None)
        tipo_documento = TIPO_DOCUMENTO.get(len(self.cpf), None)
        
        if tipo_pessoa is not None and tipo_documento is not None:
            sql = "INSERT INTO pessoas (nome, sobrenome, genero, idade, documento, tipo) VALUES (?, ?, ?, ?, ?, ?)"
            values = (self.nome, self.sobrenome, tipo_pessoa, self.idade, self.cpf, tipo_documento)
            inserir_dados(conn, sql, values)
        else:
            print("Gênero ou documento inválido!")

class Endereco:
    def __init__(self, documento: str, pais: str, estado: str, cidade: str, bairro: str, rua: str, numero_casa: int, observacao: str):
        self.documento = documento
        self.pais = pais
        self.estado = estado
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero_casa = numero_casa
        self.observacao = observacao

    def salvar_db(self, conn):
        sql = "INSERT INTO endereco (documento, pais, estado, cidade, bairro, rua, numero_casa, observacao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        values = (self.documento, self.pais, self.estado, self.cidade, self.bairro, self.rua, self.numero_casa, self.observacao)
        inserir_dados(conn, sql, values)

class SQLQueryExecutor:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def execute_queries_from_file(self, query_file):
        try:
            conn = sqlite3.connect(self.db_filename)
            cursor = conn.cursor()
            with open(query_file, 'r') as file:
                queries = file.read().split(';')
            results = []
            for query in queries:
                query = query.strip()
                if query:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    results.append(result)
            conn.commit()
            return results
        except sqlite3.Error as e:
            return None
        finally:
            if conn:
                conn.close()

def criar_conexao():
    try:
        conn = sqlite3.connect('poo/base.db')
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def fechar_conexao(conn):
    if conn:
        conn.close()

def inserir_dados(conn, sql, values):
    try:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        print("Dados inseridos com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")

def main():
    conn = criar_conexao()
    if not conn:
        return

    while True:
        print("""
        0 - Sair
        1 - Cadastrar Pessoa
        2 - Cadastrar Endereço
        3 - Executar Consultas SQL a partir de um arquivo
        """)
        escolha = int(input('Escolha uma opção: '))
        if escolha == 0:
            print('Saindo...')
            break
        elif escolha == 1:
            vnome = str(input('Informe o nome: '))
            vsobrenome = str(input('Informe o sobrenome: '))
            vidade = int(input('Informe a idade: '))
            vgenero = str(input('Informe o genero: '))
            vdoc = str(input('Informe o CPF ou CNPJ: '))

            if len(vdoc) == 11:
                pessoa = PessoaPF(vnome, vsobrenome, vidade, vgenero, vdoc)
                pessoa.salvar_db(conn)
            elif len(vdoc) == 14:
                pessoa = PessoaPJ(vnome, vsobrenome, vidade, vgenero, vdoc)
                pessoa.salvar_db(conn)
            else:
                print("CPF ou CNPJ inválido!")
        elif escolha == 2:
            vdoc = str(input('Informe o CPF ou CNPJ: '))
            vpais = str(input('Informe o país: '))
            vestado = str(input('Informe o estado: '))
            vcidade = str(input('Informe a cidade: '))
            vbairro = str(input('Informe o bairro: '))
            vrua = str(input('Informe a rua: '))
            vnumero_casa = int(input('Informe o número da casa: '))
            vobservacao = str(input('Informe a observação: '))

            endereco = Endereco(vdoc, vpais, vestado, vcidade, vbairro, vrua, vnumero_casa, vobservacao)
            endereco.salvar_db(conn)
        elif escolha == 3:
            query_executor = SQLQueryExecutor('poo/base.db')
            results = query_executor.execute_queries_from_file('poo/query.txt')
            if results is not None:
                for result in results:
                    for row in result:
                        print(row)
        else:
            print('Essa opção não existe')

    fechar_conexao(conn)

if __name__ == "__main__":
    main()
