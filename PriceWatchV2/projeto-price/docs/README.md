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

## Observação sobre a forma de funcionamento do projeto:

A ideia inicial do PriceWatch era desenvolver um sistema comparativo de preços funcionando de forma automática, buscando informações como preço atual, menor preço, maior preço e histórico de preços em sites como Amazon, Mercado Livre e outras plataformas de e-commerce.

Durante o desenvolvimento, a proposta inicial era utilizar APIs de integração para obter essas informações diretamente das plataformas. Porém, nos testes realizados, encontramos limitações de acesso, autenticação, regras de uso e disponibilidade de dados, o que dificultou o funcionamento automático da aplicação de forma confiável.

Também foi testada a possibilidade de coletar os preços diretamente do HTML das páginas dos produtos. No entanto, essa abordagem apresentou problemas de confiabilidade, pois muitos sites carregam os preços dinamicamente via JavaScript, utilizam estruturas diferentes de página e podem alterar o formato dos dados com frequência. Além disso, plataformas como o Mercado Livre podem apresentar diferentes formatos de links e páginas para um mesmo tipo de produto, o que dificultaria a padronização da coleta automática.

Diante dessas limitações, adotamos uma solução mais estável para fins acadêmicos: a utilização de um banco de dados local com SQLite.

Nesse modelo, os produtos são previamente cadastrados no banco de dados, contendo nome, link, site de origem, preço atual, menor preço, maior preço e histórico de preços dos últimos meses. A aplicação passa a trabalhar com esses dados locais, sem depender de consultas externas em tempo real.

O funcionamento ficou da seguinte forma:

Os produtos ficam armazenados no banco de dados local.
O usuário acessa a aplicação e escolhe um produto já cadastrado no banco.
Ao ativar o produto no sistema, ele passa a ser exibido na página inicial.
A home mostra as principais informações do produto, como preço atual, menor preço, maior preço e gráfico com o histórico de preços.
O histórico permite visualizar a variação de preços entre janeiro e junho, ajudando o usuário a identificar o melhor momento para realizar uma compra.

Com essa solução, o sistema mantém a proposta principal do projeto, que é permitir a análise e comparação de preços, mas de uma forma mais controlada, confiável e adequada para a apresentação acadêmica.