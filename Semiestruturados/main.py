import psycopg2

con = psycopg2.connect(
    host = "localhost",
    port = 5433,
    database = "segurança_publica_db",
    user = "postgres",
    password = "1234"
)

cur = con.cursor()
cur.execute("SELECT * FROM unidade_federativa")
resultados = cur.fetchall()
print(resultados)

cur.close()
con.close()
