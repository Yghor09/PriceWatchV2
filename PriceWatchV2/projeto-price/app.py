import argparse
import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for

from database import (
    ativar_produto,
    buscar_historico_produto,
    buscar_produto,
    desativar_produto,
    listar_produtos,
    listar_produtos_disponiveis,
)

app = Flask(__name__)

MESES = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez",
}


def _converter_data(data_original):
    for formato in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(data_original, formato)
        except ValueError:
            continue

    return None


def montar_historico(produto_id):
    registros = buscar_historico_produto(produto_id)
    historico = []
    total = len(registros)

    for indice, registro in enumerate(registros):
        data_obj = _converter_data(registro["data"])

        if data_obj:
            label = MESES.get(data_obj.month, data_obj.strftime("%m"))
            data_completa = data_obj.strftime("%d/%m/%Y")
        else:
            label = registro["data"]
            data_completa = registro["data"]

        if indice == total - 1:
            label = "Atual"

        historico.append(
            {
                "label": label,
                "data_completa": data_completa,
                "preco": float(registro["preco"]),
            }
        )

    return historico


def montar_card_produto(produto):
    historico = montar_historico(produto["id"])

    if historico:
        preco_atual = historico[-1]["preco"]
        menor_preco = min(historico, key=lambda item: item["preco"])
        maior_preco = max(historico, key=lambda item: item["preco"])
    else:
        preco_atual = None
        menor_preco = None
        maior_preco = None

    return {
        "id": produto["id"],
        "nome": produto["nome"],
        "url": produto["url"],
        "site": produto["site"],
        "preco_atual": preco_atual,
        "menor_preco": menor_preco,
        "maior_preco": maior_preco,
        "historico": historico,
        "labels": [item["label"] for item in historico],
        "precos": [item["preco"] for item in historico],
    }


@app.route("/")
def home():
    produtos_ativos = listar_produtos()
    produtos_cards = [montar_card_produto(produto) for produto in produtos_ativos]

    return render_template(
        "index.html",
        produtos=produtos_cards,
        produto_count=len(produtos_cards),
    )


@app.route("/novo-produto")
def novo_produto():
    produtos_disponiveis = listar_produtos_disponiveis()

    return render_template(
        "cadastrar.html",
        produtos_disponiveis=produtos_disponiveis,
    )


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    produto_id = request.form.get("produto_id", type=int)

    if produto_id:
        produto = buscar_produto(produto_id)

        if produto:
            ativar_produto(produto_id)

    return redirect(url_for("home"))


@app.route("/historico/<int:id>")
def historico(id):
    produto = buscar_produto(id)

    if produto is None:
        return redirect(url_for("home"))

    produto_card = montar_card_produto(produto)

    return render_template("historico.html", produto=produto_card)


@app.route("/remover/<int:id>")
def remover(id):
    desativar_produto(id)
    return redirect(url_for("home"))


@app.route("/excluir/<int:id>")
def excluir(id):
    return remover(id)


def obter_porta_padrao():
    porta = os.getenv("PORT", "5005")

    try:
        porta = int(porta)
    except ValueError as erro:
        raise ValueError("A variável PORT precisa ser um número. Exemplo: PORT=8080") from erro

    if porta < 1 or porta > 65535:
        raise ValueError("A porta precisa estar entre 1 e 65535.")

    return porta


def criar_argumentos_linha_comando():
    parser = argparse.ArgumentParser(description="Executar o PriceWatch localmente.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=obter_porta_padrao(),
        help="Porta em que o projeto vai rodar. Exemplo: python app.py --port 8080",
    )
    return parser.parse_args()


if __name__ == "__main__":
    argumentos = criar_argumentos_linha_comando()

    if argumentos.port < 1 or argumentos.port > 65535:
        raise ValueError("A porta precisa estar entre 1 e 65535.")

    app.run(debug=True, port=argumentos.port)
