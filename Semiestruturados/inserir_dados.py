import psycopg2
import pandas as pd

con = psycopg2.connect(
    host = "localhost",
    port = 5433,
    database = "segurança_publica_db",
    user = "postgres",
    password = "1234"
)

cur = con.cursor()

ocorrencias_df = pd.read_csv(r"C:\temp\ws-eclipse\BancodeDado-Semiestruturais\Banco-de-dados-2-Projeto-Semiestruturais-main\Banco-de-dados-2-Projeto-Semiestruturais-main\Semiestruturados\ocorrencias_tratado.csv")
vitimas_df = pd.read_csv(r"C:\temp\ws-eclipse\BancodeDado-Semiestruturais\Banco-de-dados-2-Projeto-Semiestruturais-main\Banco-de-dados-2-Projeto-Semiestruturais-main\Semiestruturados\vitimas_tratado.csv")

print(f"Ocorrências: {len(ocorrencias_df)} linhas")
print(f"Vítimas: {len(vitimas_df)} linhas")
print(f"Colunas ocorrências: {list(ocorrencias_df.columns)}")
print(f"Colunas vítimas: {list(vitimas_df.columns)}")

# Extrair UFs únicas e inserir
ufs_unicas = ocorrencias_df['uf'].unique()
print(f"UFs encontradas: {ufs_unicas}")

for uf in ufs_unicas:
    cur.execute(
        "INSERT INTO unidade_federativa (nome_uf) VALUES (%s) ON CONFLICT (nome_uf) DO NOTHING",
        (uf,)
    )

con.commit()
cur.execute("SELECT id_uf, nome_uf FROM unidade_federativa")
dict_uf = {row[1]: row[0] for row in cur.fetchall()}
#cur.execute("SELECT * FROM unidade_federativa")
#print("UFs inseridas:", cur.fetchall())

# Extrair crimes únicos (junta os dois CSVs para pegar todos)
crimes_ocorrencias = ocorrencias_df['tipo_crime'].unique()
crimes_vitimas = vitimas_df['tipo_crime'].unique()
crimes_unicos = set(crimes_ocorrencias) | set(crimes_vitimas)
print(f"Crimes encontrados: {len(crimes_unicos)}")

for crime in crimes_unicos:
    cur.execute(
        "INSERT INTO crime (nome_crime) VALUES (%s) ON CONFLICT (nome_crime) DO NOTHING",
        (str(crime),)
    )

con.commit()
cur.execute("SELECT COUNT(*) FROM crime")
print("Total de crimes inseridos:", cur.fetchone()[0])

# Extrair pares únicos de ano/mês (junta os dois CSVs)
tempos_ocorrencias = ocorrencias_df[['ano', 'mes']].drop_duplicates()
tempos_vitimas = vitimas_df[['ano', 'mes']].drop_duplicates()
tempos_unicos = pd.concat([tempos_ocorrencias, tempos_vitimas]).drop_duplicates()
print(f"Pares ano/mês encontrados: {len(tempos_unicos)}")

for _, row in tempos_unicos.iterrows():
    cur.execute(
        "INSERT INTO tempo (ano, mes) VALUES (%s, %s) ON CONFLICT (ano, mes) DO NOTHING",
        (int(row['ano']), int(row['mes']))
    )

con.commit()
cur.execute("SELECT COUNT(*) FROM tempo")
print("Total de tempos inseridos:", cur.fetchone()[0])

# Extrair sexos únicos (só da tabela de vítimas)
sexos_unicos = vitimas_df['sexo_vitima'].unique()
print(f"Sexos encontrados: {sexos_unicos}")

for sexo in sexos_unicos:
    cur.execute(
        "INSERT INTO sexo (sexo) VALUES (%s) ON CONFLICT (sexo) DO NOTHING",
        (str(sexo),)
    )

con.commit()
cur.execute("SELECT * FROM sexo")
print("Sexos inseridos:", cur.fetchall())

# Conferir tudo
for tabela in ['unidade_federativa', 'crime', 'tempo', 'sexo']:
    cur.execute(f"SELECT COUNT(*) FROM {tabela}")
    print(f"Tabela {tabela}: {cur.fetchone()[0]} registros")

# Montar dicionários
cur.execute("SELECT id_uf, nome_uf FROM unidade_federativa")
dict_uf = {row[1]: row[0] for row in cur.fetchall()}

cur.execute("SELECT id_crime, nome_crime FROM crime")
dict_crime = {row[1]: row[0] for row in cur.fetchall()}

cur.execute("SELECT id_tempo, ano, mes FROM tempo")
dict_tempo = {(row[1], row[2]): row[0] for row in cur.fetchall()}

cur.execute("SELECT id_sexo, sexo FROM sexo")
dict_sexo = {row[1]: row[0] for row in cur.fetchall()}

print("Dicionários montados!")
print(f"dict_uf: {len(dict_uf)} itens")
print(f"dict_crime: {len(dict_crime)} itens")
print(f"dict_tempo: {len(dict_tempo)} itens")
print(f"dict_sexo: {len(dict_sexo)} itens")

# Inserir ocorrências
print("Inserindo ocorrências...")
inseridos = 0
erros = 0

for _, row in ocorrencias_df.iterrows():
    try:
        id_uf = dict_uf[row['uf']]
        id_crime = dict_crime[row['tipo_crime']]
        id_tempo = dict_tempo[(int(row['ano']), int(row['mes']))]
        quantidade = int(row['quantidade_ocorrencias'])

        cur.execute(
            "INSERT INTO ocorrencia (id_uf, id_crime, id_tempo, numero_ocorrencias) VALUES (%s, %s, %s, %s)",
            (id_uf, id_crime, id_tempo, quantidade)
        )
        inseridos += 1
        
        if inseridos % 5000 == 0:
            con.commit()
            print(f"  {inseridos} ocorrências inseridas...")
            
    except Exception as e:
        erros += 1
        if erros <= 5:
            print(f"Erro na linha: uf={row['uf']}, crime={row['tipo_crime']}, ano={row['ano']}, mes={row['mes']}")
            print(f"  {e}")

con.commit()
print(f"Ocorrências: {inseridos} inseridas, {erros} erros")

# Inserir vítimas
print("Inserindo vítimas...")
inseridos = 0
erros = 0

for _, row in vitimas_df.iterrows():
    try:
        id_uf = dict_uf[row['uf']]
        id_crime = dict_crime[row['tipo_crime']]
        id_tempo = dict_tempo[(int(row['ano']), int(row['mes']))]
        id_sexo = dict_sexo[row['sexo_vitima']]
        quantidade = int(row['quantidade_vitimas'])

        cur.execute(
            "INSERT INTO vitima (id_uf, id_crime, id_tempo, id_sexo, numero_vitimas) VALUES (%s, %s, %s, %s, %s)",
            (id_uf, id_crime, id_tempo, id_sexo, quantidade)
        )
        inseridos += 1
        
        if inseridos % 5000 == 0:
            con.commit()
            print(f"  {inseridos} vítimas inseridas...")
            
    except Exception as e:
        erros += 1
        if erros <= 5:
            print(f"Erro na linha: uf={row['uf']}, crime={row['tipo_crime']}, ano={row['ano']}, mes={row['mes']}, sexo={row['sexo_vitima']}")
            print(f"  {e}")

con.commit()
print(f"Vítimas: {inseridos} inseridas, {erros} erros")

# Verificar totais finais
for tabela in ['unidade_federativa', 'crime', 'tempo', 'sexo', 'ocorrencia', 'vitima']:
    cur.execute(f"SELECT COUNT(*) FROM {tabela}")
    print(f"Tabela {tabela}: {cur.fetchone()[0]} registros")

cur.close()
con.close()
print("Dados inseridos")
