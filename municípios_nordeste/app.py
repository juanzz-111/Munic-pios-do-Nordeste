from flask import Flask, render_template, request, jsonify, make_response
import json

app = Flask(__name__)


# ==========================================
# DICIONÁRIO DE MUNICÍPIOS DO NORDESTE
# ==========================================


municipios_nordeste_dataset = {
    "metadados": {
        "regiao": "Nordeste",
        "pais": "Brasil",
        "total_municipios": 30,
        "fonte_dados_populacao": "IBGE - Censo 2022"
    },

    "municipios": {
        # CEARÁ
        "Fortaleza": {
            "id_ibge": 2304400,
            "estado": "Ceará",
            "sigla_uf": "CE",
            "capital": True,
            "populacao_estimada": 2582360
        },
        "Caucaia": {
            "id_ibge": 2303709,
            "estado": "Ceará",
            "sigla_uf": "CE",
            "capital": False,
            "populacao_estimada": 355679
        },
        "Juazeiro do Norte": {
            "id_ibge": 2307304,
            "estado": "Ceará",
            "sigla_uf": "CE",
            "capital": False,
            "populacao_estimada": 286120
        },
        "Maracanaú": {
            "id_ibge": 2307650,
            "estado": "Ceará",
            "sigla_uf": "CE",
            "capital": False,
            "populacao_estimada": 234509
        },

        # BAHIA
        "Salvador": {
            "id_ibge": 2927408,
            "estado": "Bahia",
            "sigla_uf": "BA",
            "capital": True,
            "populacao_estimada": 2559945
        },
        "Feira de Santana": {
            "id_ibge": 2910800,
            "estado": "Bahia",
            "sigla_uf": "BA",
            "capital": False,
            "populacao_estimada": 616279
        },
        "Vitória da Conquista": {
            "id_ibge": 2933307,
            "estado": "Bahia",
            "sigla_uf": "BA",
            "capital": False,
            "populacao_estimada": 370868
        },
        "Camaçari": {
            "id_ibge": 2905701,
            "estado": "Bahia",
            "sigla_uf": "BA",
            "capital": False,
            "populacao_estimada": 300372
        },

        # ALAGOAS
        "Maceió": {
            "id_ibge": 2704302,
            "estado": "Alagoas",
            "sigla_uf": "AL",
            "capital": True,
            "populacao_estimada": 957916
        },
        "Arapiraca": {
            "id_ibge": 2700300,
            "estado": "Alagoas",
            "sigla_uf": "AL",
            "capital": False,
            "populacao_estimada": 234696
        },
        "Rio Largo": {
            "id_ibge": 2707701,
            "estado": "Alagoas",
            "sigla_uf": "AL",
            "capital": False,
            "populacao_estimada": 93927
        },

        # MARANHÃO
        "São Luís": {
            "id_ibge": 2111300,
            "estado": "Maranhão",
            "sigla_uf": "MA",
            "capital": True,
            "populacao_estimada": 1037775
        },
        "Imperatriz": {
            "id_ibge": 2105302,
            "estado": "Maranhão",
            "sigla_uf": "MA",
            "capital": False,
            "populacao_estimada": 273110
        },
        "Timon": {
            "id_ibge": 2112209,
            "estado": "Maranhão",
            "sigla_uf": "MA",
            "capital": False,
            "populacao_estimada": 174465
        },

        # PARAÍBA
        "João Pessoa": {
            "id_ibge": 2507507,
            "estado": "Paraíba",
            "sigla_uf": "PB",
            "capital": True,
            "populacao_estimada": 833932
        },
        "Campina Grande": {
            "id_ibge": 2504009,
            "estado": "Paraíba",
            "sigla_uf": "PB",
            "capital": False,
            "populacao_estimada": 419379
        },
        "Santa Rita": {
            "id_ibge": 2513703,
            "estado": "Paraíba",
            "sigla_uf": "PB",
            "capital": False,
            "populacao_estimada": 149910
        },

        # PERNAMBUCO
        "Recife": {
            "id_ibge": 2611606,
            "estado": "Pernambuco",
            "sigla_uf": "PE",
            "capital": True,
            "populacao_estimada": 1488920
        },
        "Jaboatão dos Guararapes": {
            "id_ibge": 2607901,
            "estado": "Pernambuco",
            "sigla_uf": "PE",
            "capital": False,
            "populacao_estimada": 643759
        },
        "Caruaru": {
            "id_ibge": 2604106,
            "estado": "Pernambuco",
            "sigla_uf": "PE",
            "capital": False,
            "populacao_estimada": 378052
        },

        # PIAUÍ
        "Teresina": {
            "id_ibge": 2211001,
            "estado": "Piauí",
            "sigla_uf": "PI",
            "capital": True,
            "populacao_estimada": 866300
        },
        "Parnaíba": {
            "id_ibge": 2207702,
            "estado": "Piauí",
            "sigla_uf": "PI",
            "capital": False,
            "populacao_estimada": 162159
        },
        "Picos": {
            "id_ibge": 2208007,
            "estado": "Piauí",
            "sigla_uf": "PI",
            "capital": False,
            "populacao_estimada": 83090
        },

        # RIO GRANDE DO NORTE
        "Natal": {
            "id_ibge": 2408102,
            "estado": "Rio Grande do Norte",
            "sigla_uf": "RN",
            "capital": True,
            "populacao_estimada": 751300
        },
        "Mossoró": {
            "id_ibge": 2408003,
            "estado": "Rio Grande do Norte",
            "sigla_uf": "RN",
            "capital": False,
            "populacao_estimada": 264577
        },
        "Parnamirim": {
            "id_ibge": 2403251,
            "estado": "Rio Grande do Norte",
            "sigla_uf": "RN",
            "capital": False,
            "populacao_estimada": 252716
        },

        # SERGIPE
        "Aracaju": {
            "id_ibge": 2800308,
            "estado": "Sergipe",
            "sigla_uf": "SE",
            "capital": True,
            "populacao_estimada": 602757
        },
        "Nossa Senhora do Socorro": {
            "id_ibge": 2804805,
            "estado": "Sergipe",
            "sigla_uf": "SE",
            "capital": False,
            "populacao_estimada": 192330
        },
        "Lagarto": {
            "id_ibge": 2803502,
            "estado": "Sergipe",
            "sigla_uf": "SE",
            "capital": False,
            "populacao_estimada": 101579
        },
        "Itabaiana": {
            "id_ibge": 2802906,
            "estado": "Sergipe",
            "sigla_uf": "SE",
            "capital": False,
            "populacao_estimada": 103439
        }
    }
}


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def atualizar_total_municipios():
    municipios = municipios_nordeste_dataset["municipios"]

    municipios_nordeste_dataset["metadados"]["total_municipios"] = len(municipios)


def validar_municipio(dados, cadastro_completo=False):

    if not isinstance(dados, dict):
        return "Os dados devem ser enviados em formato JSON."

    campos_permitidos = [
        "nome",
        "id_ibge",
        "estado",
        "sigla_uf",
        "capital",
        "populacao_estimada"
    ]

    for campo in dados:
        if campo not in campos_permitidos:
            return f"Campo não permitido: {campo}"

    campos_obrigatorios = [
        "id_ibge",
        "estado",
        "sigla_uf",
        "capital",
        "populacao_estimada"
    ]

    if cadastro_completo:
        for campo in campos_obrigatorios:
            if campo not in dados:
                return f"O campo {campo} é obrigatório."

    if "id_ibge" in dados:
        if type(dados["id_ibge"]) is not int or dados["id_ibge"] <= 0:
            return "O ID IBGE deve ser um número inteiro positivo."

    if "estado" in dados:
        if not isinstance(dados["estado"], str) or not dados["estado"].strip():
            return "O estado informado é inválido."

    if "sigla_uf" in dados:
        if (
            not isinstance(dados["sigla_uf"], str)
            or len(dados["sigla_uf"].strip()) != 2
            or not dados["sigla_uf"].strip().isalpha()
        ):
            return "A sigla UF deve conter duas letras."

    if "capital" in dados:
        if type(dados["capital"]) is not bool:
            return "O campo capital deve ser verdadeiro ou falso."

    if "populacao_estimada" in dados:
        if (
            type(dados["populacao_estimada"]) is not int
            or dados["populacao_estimada"] < 0
        ):
            return "A população deve ser um número inteiro não negativo."

    return None


# ==========================================
# ROTA PRINCIPAL
# ==========================================

@app.route("/")
def inicio():
    return render_template("index.html")


# ==========================================
# GET - LISTAR TODOS OU FILTRAR POR UF
# ==========================================

@app.route("/municipios", methods=["GET"])
def listar_municipios():

    municipios = municipios_nordeste_dataset["municipios"]

    uf = request.args.get("uf")

    if uf:
        filtrados = {}

        for nome, dados in municipios.items():
            if dados["sigla_uf"] == uf.strip().upper():
                filtrados[nome] = dados

        return jsonify(filtrados), 200

    return jsonify(municipios), 200


# ==========================================
# GET - CONSULTAR MUNICÍPIO PELO NOME
# ==========================================

@app.route("/municipios/<nome>", methods=["GET"])
def consultar_municipio(nome):

    municipios = municipios_nordeste_dataset["municipios"]

    if nome not in municipios:
        return jsonify({
            "erro": "Município não encontrado."
        }), 404

    return jsonify(municipios[nome]), 200


# ==========================================
# POST - CADASTRAR NOVO MUNICÍPIO
# ==========================================

@app.route("/municipios", methods=["POST"])
def cadastrar_municipio():

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie os dados em formato JSON."
        }), 400

    nome = dados.get("nome")

    if not isinstance(nome, str) or not nome.strip():
        return jsonify({
            "erro": "Nome do município obrigatório."
        }), 400

    nome = nome.strip()

    erro = validar_municipio(dados, cadastro_completo=True)

    if erro:
        return jsonify({"erro": erro}), 400

    municipios = municipios_nordeste_dataset["municipios"]

    if nome in municipios:
        return jsonify({
            "erro": "Município já cadastrado."
        }), 409

    novo_municipio = {
        "id_ibge": dados["id_ibge"],
        "estado": dados["estado"].strip(),
        "sigla_uf": dados["sigla_uf"].strip().upper(),
        "capital": dados["capital"],
        "populacao_estimada": dados["populacao_estimada"]
    }

    municipios[nome] = novo_municipio

    atualizar_total_municipios()

    return jsonify({
        "mensagem": "Município cadastrado com sucesso!",
        "municipio": municipios[nome]
    }), 201


# ==========================================
# PATCH - ATUALIZAR PARTE DOS DADOS
# ==========================================

@app.route("/municipios/<nome>", methods=["PATCH"])
def atualizar_municipio(nome):

    municipios = municipios_nordeste_dataset["municipios"]

    if nome not in municipios:
        return jsonify({
            "erro": "Município não encontrado."
        }), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie os dados em formato JSON."
        }), 400

    dados.pop("nome", None)

    if not dados:
        return jsonify({
            "erro": "Nenhum dado enviado para atualização."
        }), 400

    erro = validar_municipio(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    dados_atualizados = dados.copy()

    if "estado" in dados_atualizados:
        dados_atualizados["estado"] = dados_atualizados["estado"].strip()

    if "sigla_uf" in dados_atualizados:
        dados_atualizados["sigla_uf"] = dados_atualizados["sigla_uf"].strip().upper()

    municipios[nome].update(dados_atualizados)

    return jsonify({
        "mensagem": "Município atualizado com sucesso!",
        "municipio": municipios[nome]
    }), 200


# ==========================================
# DELETE - EXCLUIR MUNICÍPIO
# ==========================================

@app.route("/municipios/<nome>", methods=["DELETE"])
def excluir_municipio(nome):

    municipios = municipios_nordeste_dataset["municipios"]

    if nome not in municipios:
        return jsonify({
            "erro": "Município não encontrado."
        }), 404

    municipio_removido = municipios.pop(nome)

    atualizar_total_municipios()

    return jsonify({
        "mensagem": "Município removido com sucesso!",
        "municipio": municipio_removido
    }), 200


# ==========================================
# GET - BAIXAR ARQUIVO JSON
# ==========================================

@app.route("/municipios/download", methods=["GET"])
def baixar_municipios():

    atualizar_total_municipios()

    arquivo_json = json.dumps(
        municipios_nordeste_dataset,
        ensure_ascii=False,
        indent=4
    )

    resposta = make_response(arquivo_json)

    resposta.headers["Content-Type"] = "application/json; charset=utf-8"

    resposta.headers["Content-Disposition"] = (
        "attachment; filename=municipios_nordeste.json"
    )

    return resposta


# ==========================================
# EXECUTAR A APLICAÇÃO
# ==========================================

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000, debug=True)
