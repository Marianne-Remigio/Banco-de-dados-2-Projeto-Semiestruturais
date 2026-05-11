import pandas as pd
from unidecode import unidecode


def carregar_dados(arquivo):
    abas = pd.ExcelFile(arquivo).sheet_names
    lista = []

    for aba in abas:
        dados = pd.read_excel(arquivo, sheet_name=aba)
        lista.append(dados)

    municipios = pd.concat(lista, ignore_index=True)
    return municipios


def padronizar_colunas(municipios):
    municipios.columns = ["cod_ibge", "municipio", "uf", "regiao", "data", "vitimas"]
    return municipios


def tratar_dados(municipios):
    municipios = municipios.dropna(subset=["cod_ibge", "municipio", "uf", "regiao", "data"])
    municipios["vitimas"] = municipios["vitimas"].fillna(0)

    municipios["municipio"] = municipios["municipio"].apply(unidecode)
    municipios["regiao"] = municipios["regiao"].apply(unidecode)
    municipios["uf"] = municipios["uf"].apply(unidecode)

    municipios["ano"] = pd.to_datetime(municipios["data"]).dt.year
    municipios["mes"] = pd.to_datetime(municipios["data"]).dt.month

    return municipios


def selecionar_menor_por_regiao(municipios):
    totais = municipios.groupby(
        ["regiao", "uf", "municipio"],
        as_index=False
    )["vitimas"].sum()

    totais = totais[totais["vitimas"] > 0]

    menores = totais.loc[
        totais.groupby("regiao")["vitimas"].idxmin()
    ]

    return menores


def filtrar_dados_dos_menores(municipios, menores):
    resultado = municipios.merge(
        menores[["regiao", "uf", "municipio"]],
        on=["regiao", "uf", "municipio"],
        how="inner"
    )

    return resultado


def salvar_dados(municipios_tratado, menores, dados_menores):
    municipios_tratado.to_csv("municipios_tratado.csv", index=False)
    menores.to_csv("menores_municipios_por_regiao.csv", index=False)
    dados_menores.to_csv("dados_menores_municipios.csv", index=False)


def main():
    arquivo = "indicadoressegurancapublicamunic.xlsx"

    municipios = carregar_dados(arquivo)
    municipios = padronizar_colunas(municipios)
    municipios = tratar_dados(municipios)

    menores = selecionar_menor_por_regiao(municipios)
    dados_menores = filtrar_dados_dos_menores(municipios, menores)

    salvar_dados(municipios, menores, dados_menores)

    print("Menor municipio por regiao:")
    print(menores)

    print("\nDados filtrados:")
    print(dados_menores.head())

    print("\nValores nulos:")
    print(dados_menores.isnull().sum())


if __name__ == "__main__":
    main()