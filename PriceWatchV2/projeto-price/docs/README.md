# PriceWatch

Aplicação Flask para exibir produtos e histórico de preços usando apenas o banco local `data/precos.db`.

## Fluxo atual

1. Os produtos ficam guardados no banco de dados.
2. A home exibe somente produtos ativados pelo cadastro da aplicação.
3. Ao cadastrar um produto, o sistema não busca preço em sites externos.
4. O preço atual, maior preço, menor preço e gráfico são calculados a partir da tabela `historico`.
5. O banco possui produtos do Mercado Livre e da Amazon disponíveis para cadastro.

## Banco de dados

- 20 produtos do Mercado Livre.
- 19 produtos válidos da Amazon.

Observação: no arquivo enviado da Amazon, o Produto 15 veio sem nome, link e preços. Por isso, ele não foi inserido para evitar uma opção vazia na tela de cadastro. O produto P10 da Amazon veio sem preço de fevereiro, então esse mês foi ignorado apenas nesse item.

## Como rodar

```bash
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000` no navegador.

## Escolher a porta

```bash
python app.py --port 8080
```

Ou:

```bash
python app.py -p 8080
```

Também é possível usar variável de ambiente:

```bash
PORT=8080 python app.py
```
