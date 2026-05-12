import psycopg2

def conecao():
    return psycopg2.connect(
        host = "localhost",
        port = 5433,
        database = "segurança_publica_db",
        user = "postgres",
        password = "1234"
    )

def listar_unidade_federativa():
    con = conecao()
    cur = con.cursor()
    cur.execute("SELECT * FROM unidade_federativa")
    resultados = cur.fetchall()

    for row in resultados:
        print(row)
        cur.close()
        con.close()

def listar_crimes():
    con = conecao()
    cur = con.cursor()
    cur.execute("SELECT * FROM crime")
    resultados = cur.fetchall()

    for row in resultados:
        print(row)
        cur.close()
        con.close()

def listar_ocorrencias():
    con = conecao()
    cur = con.cursor()
    cur.execute("""
                SELECT uf.nome_uf, c.nome_crime, t.ano, t.mes, o.numero_ocorrencias
                FROM ocorrencia o
                JOIN unidade_federativa uf ON o.id_uf = uf.id_uf
                JOIN crime c ON o.id_crime = c.id_crime
                JOIN tempo t ON o.id_tempo = t.id_tempo
                ORDER BY uf.nome_uf, t.ano, t.mes
                LIMIT 10
            """)
    resultados = cur.fetchall()

    for row in resultados:
        print(row)
        cur.close()
        con.close()

def atualizar_ocorrencias(id_ocorrencia, valor_novo):
    con = conecao()
    cur = con.cursor()
    cur.execute("UPDATE ocorrencia SET numero_ocorrencias = %s WHERE id_ocorrencia = %s", 
                (valor_novo, id_ocorrencia))
    con.commit()
    print("Registro {} atualizado".format(id_ocorrencia))
    cur.close()
    con.close()

def deletar_ocorrencia(id_ocorrencia):
    con = conecao()
    cur = con.cursor()
    cur.execute("DELETE FROM ocorrencia WHERE id_ocorrencia = %s", (id_ocorrencia,))
    con.commit()
    print("Registro {} deletado".format(id_ocorrencia))
    con.commit()
    cur.close()
    con.close()

def menu():
    while True:
        print("Digite 1 para Listar os estados")
        print("Digite 2 para Listar crimes")
        print("Digite 3 para Listar ocorrencias")
        print("Digite 4 para Atualizar ocorrencias")
        print("Digite 5 para Deletar uma ocorrencia")
        print("Digite 0 para sair")

        escolha = input("Escolha uma das opções: ")

        if escolha == "1":
            listar_unidade_federativa()
        elif escolha == "2":
            listar_crimes()
        elif escolha == "3":
            listar_ocorrencias()
        elif escolha == "4":
            id_ocorrencia = input("ID da ocorrencia: ")
            valor_novo = input("Digite o novo valor da ocorrencia: ")
            atualizar_ocorrencias(int(id_ocorrencia), int(valor_novo))
        elif escolha == "5":
            id_ocorrencia = input("ID da ocorrencia: ")
            deletar_ocorrencia(int(id_ocorrencia))
        elif escolha == "0":
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    menu()
