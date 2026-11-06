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
        "total_municipios": 2,
        "fonte_dados_populacao": "IBGE"
    },

    "municipios": {
        "Fortaleza": {
            "id_ibge": 2304400,
            "estado": "Ceará",
            "sigla_uf": "CE",
            "capital": True,
            "populacao_estimada": 2582360
        },

        "Salvador": {
            "id_ibge": 2927408,
            "estado": "Bahia",
            "sigla_uf": "BA",
            "capital": True,
            "populacao_estimada": 2559945
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
