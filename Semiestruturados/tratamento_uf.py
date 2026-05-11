import pandas as pd
from unidecode import unidecode

arquivo = "indicadoressegurancapublicauf.xlsx"

# abas existentes no arquivo xlsx
# abas = pd.ExcelFile(arquivo)
# print("Abas disponíveis:", abas.sheet_names)
# print("Colunas Ocorrências: "
# print(ocorrencias.columns)
# print("\nPrimeiras Linhas Ocorrencias: ")
# print(ocorrencias.head())
# print("Colunas Vitimas: ")
# print(vitimas.columns)
# print("\nPrimeiras Linhas Vitimas: ")
# print(vitimas.head())

def carregar_dados(arquivo):
    ocorrencias = pd.read_excel(arquivo, sheet_name="Ocorrências")
    vitimas = pd.read_excel(arquivo, sheet_name="Vítimas")
    return ocorrencias, vitimas


def padronizar_colunas(ocorrencias, vitimas):
    ocorrencias.columns = ["uf", "tipo_crime", "ano", "mes", "quantidade_ocorrencias"]
    vitimas.columns = ["uf", "tipo_crime", "ano", "mes", "sexo_vitima", "quantidade_vitimas"]
    return ocorrencias, vitimas


def tratar_mes(ocorrencias, vitimas):
    mapa_meses = {
        "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
        "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
        "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
    }

    ocorrencias["mes"] = ocorrencias["mes"].map(mapa_meses)
    vitimas["mes"] = vitimas["mes"].map(mapa_meses)

    return ocorrencias, vitimas


def tratar_sexo(vitimas):
    vitimas["sexo_vitima"] = vitimas["sexo_vitima"].replace({
        "Sexo NI": "Nao informado"
    })
    return vitimas


def tratar_texto(ocorrencias, vitimas):
    ocorrencias["uf"] = ocorrencias["uf"].apply(unidecode)
    vitimas["uf"] = vitimas["uf"].apply(unidecode)

    ocorrencias["tipo_crime"] = ocorrencias["tipo_crime"].apply(unidecode)
    vitimas["tipo_crime"] = vitimas["tipo_crime"].apply(unidecode)

    vitimas["sexo_vitima"] = vitimas["sexo_vitima"].apply(unidecode)

    return ocorrencias, vitimas


def tratar_nulos(ocorrencias, vitimas):
    ocorrencias = ocorrencias.dropna(subset=["uf", "tipo_crime", "ano", "mes"])
    vitimas = vitimas.dropna(subset=["uf", "tipo_crime", "ano", "mes"])

    ocorrencias["quantidade_ocorrencias"] = ocorrencias["quantidade_ocorrencias"].fillna(0)
    vitimas["quantidade_vitimas"] = vitimas["quantidade_vitimas"].fillna(0)
    vitimas["sexo_vitima"] = vitimas["sexo_vitima"].fillna("Nao informado")

    return ocorrencias, vitimas


def salvar_dados(ocorrencias, vitimas):
    ocorrencias.to_csv("ocorrencias_tratado.csv", index=False)
    vitimas.to_csv("vitimas_tratado.csv", index=False)


def main():
    arquivo = "indicadoressegurancapublicauf.xlsx"

    ocorrencias, vitimas = carregar_dados(arquivo)
    ocorrencias, vitimas = padronizar_colunas(ocorrencias, vitimas)
    ocorrencias, vitimas = tratar_mes(ocorrencias, vitimas)
    vitimas = tratar_sexo(vitimas)
    ocorrencias, vitimas = tratar_nulos(ocorrencias, vitimas)
    ocorrencias, vitimas = tratar_texto(ocorrencias, vitimas)

    salvar_dados(ocorrencias, vitimas)

    print(ocorrencias.head())
    print(vitimas.head())

    print(ocorrencias.isnull().sum())
    print(vitimas.isnull().sum())


if __name__ == "__main__":
    main()
