# CORINTHIANS ARCHIVE STUDIES

Aplicação web desenvolvida com Flask para funcionar como um catálogo digital conceitual inspirado em archive fashion.

O projeto apresenta peças organizadas em famílias e coleções, páginas individuais para cada objeto do arquivo, uma área administrativa protegida para gerenciamento do catálogo e um sistema de recomendação de peças baseado em Machine Learning.

> Projeto independente e não oficial.

---

## Live

Acesse o projeto online:

https://corinthians-archive-studies-v2.onrender.com

> O projeto utiliza o plano gratuito do Render. Caso esteja inativo há algum tempo, o primeiro acesso pode levar alguns segundos para carregar.

---

## Sobre o projeto

O CORINTHIANS ARCHIVE STUDIES surgiu como uma evolução de uma aplicação simples de gerenciamento de produtos.

A proposta atual funciona como um arquivo digital experimental, combinando desenvolvimento web, organização de dados, direção visual inspirada em archive fashion e um sistema de recomendação baseado nas características das peças.

As peças cadastradas são apresentadas como objetos de arquivo e organizadas em diferentes famílias e estudos.

---

## Funcionalidades

- Catálogo público de peças
- Organização por famílias e coleções
- Página individual para cada peça
- Informações de coleção, temporada, categoria, tags, descrição e valor
- Área administrativa protegida por login
- Cadastro de novas peças
- Edição de peças existentes
- Exclusão de peças
- CRUD completo
- Interface responsiva
- Player de áudio integrado à experiência visual
- Recomendação automática de peças relacionadas
- Seleção de até 3 objetos semelhantes através de Machine Learning

---

## Machine Learning

O projeto possui um sistema de recomendação baseado em conteúdo.

Ao abrir uma peça, o sistema utiliza as informações de:

- coleção;
- categoria;
- tags.

Essas características são transformadas em uma representação numérica utilizando **TF-IDF**.

O modelo utiliza unigramas e bigramas:

```python
TfidfVectorizer(
    ngram_range=(1, 2)
)
```

Isso permite considerar tanto palavras individuais quanto expressões como:

```text
BLACK DENIM
LONG SLEEVE
SÃO PAULO
```

Depois, a **similaridade de cosseno** compara a peça atual com os outros objetos do catálogo.

O fluxo funciona assim:

```text
Peça atual
↓
Coleção + Categoria + Tags
↓
TF-IDF
↓
Vetores numéricos
↓
Similaridade de cosseno
↓
3 peças mais semelhantes
↓
RELATED ARCHIVE / MACHINE SELECTED
```

A lógica do recomendador fica separada em:

```text
ml/recommender.py
```

O modelo utiliza os dados reais armazenados no PostgreSQL e não depende de um conjunto de dados externo.

---

## Tecnologias utilizadas

- Python
- Flask
- PostgreSQL
- Supabase
- Psycopg2
- Scikit-learn
- HTML5
- CSS3
- JavaScript
- Jinja2
- Gunicorn
- Render
- Git
- GitHub

---

## Arquitetura

A aplicação segue uma arquitetura web cliente-servidor.

```text
Usuário
   ↓
Navegador
   ↓
Render
   ↓
Flask + Gunicorn
   ↓
PostgreSQL / Supabase
   ↓
Dados das peças
   ↓
Recomendador ML
   ↓
Template Jinja
```

O Flask é responsável pelas rotas, regras da aplicação, autenticação administrativa, comunicação com o banco e integração com o recomendador.

O PostgreSQL hospedado no Supabase armazena as informações das peças.

O Render executa a aplicação Flask e disponibiliza o sistema publicamente.

---

## Banco de dados

A tabela principal do projeto é `produtos`.

Estrutura atual:

```text
id
nome
preco
descricao
colecao
temporada
categoria
tags
imagem
```

O campo `id` é gerado automaticamente pelo PostgreSQL.

Os campos `colecao`, `categoria` e `tags` também são utilizados pelo sistema de recomendação.

---

## Organização do catálogo

As peças são agrupadas automaticamente em famílias a partir do campo `colecao`.

Exemplo:

```text
PAVILHÃO / SÃO PAULO
↓
família: PAVILHÃO
```

Famílias atuais:

- PAVILHÃO
- YOKOHAMA
- DEMOCRACIA
- 1910
- SCCP STUDIES

A aplicação utiliza uma ordem curatorial definida no backend para controlar como essas famílias aparecem no catálogo.

---

## Área administrativa

O projeto possui uma área administrativa protegida por autenticação.

Após o login, é possível:

- visualizar os objetos cadastrados;
- cadastrar novas peças;
- editar registros existentes;
- excluir registros.

As rotas administrativas são protegidas para impedir acesso direto sem autenticação.

Credenciais e informações sensíveis são carregadas através de variáveis de ambiente.

---

## Estrutura do projeto

```text
LOJA-CORINTHIANS/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── ml/
│   └── recommender.py
│
├── templates/
│   ├── index.html
│   ├── produto.html
│   ├── login.html
│   ├── admin.html
│   └── editar.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    ├── images/
    │
    └── audio/
```

O arquivo `.env` não é enviado ao GitHub.

---

## Fluxo do sistema

Fluxo público:

```text
Home
↓
Famílias / Coleções
↓
Peça individual
↓
Machine Learning
↓
Peças relacionadas
```

Fluxo administrativo:

```text
/login
↓
/admin
↓
Cadastrar / Editar / Excluir
↓
PostgreSQL
↓
Catálogo atualizado
```

---

## Flask e Jinja

O Flask funciona como o núcleo da aplicação.

Ele recebe as requisições do navegador, identifica a rota correspondente, executa a lógica necessária e consulta o banco de dados.

Na página individual de uma peça, o Flask também executa o recomendador e envia o resultado para o template:

```python
return render_template(
    'produto.html',
    produto=produto,
    relacionados=relacionados
)
```

O Jinja utiliza essas informações para gerar dinamicamente o HTML exibido pelo navegador.

---

## CRUD

O projeto possui CRUD completo:

```text
CREATE
→ cadastrar uma nova peça

READ
→ visualizar catálogo e peças

UPDATE
→ editar uma peça

DELETE
→ excluir uma peça
```

As operações são realizadas pelo Flask diretamente no PostgreSQL.

---

## Famílias e coleções

A função `extrair_familia()` identifica a família principal de uma coleção.

Exemplo:

```text
PAVILHÃO / STUDY 01
↓
PAVILHÃO
```

A função `organizar_familias()` agrupa os produtos e aplica a ordem curatorial utilizada na Home.

---

## Slugs

A função `gerar_slug()` transforma textos em identificadores simplificados.

Exemplo:

```text
SCCP STUDIES
↓
sccp-studies
```

A função remove acentos, converte o texto para letras minúsculas e substitui caracteres por hífens.

---

## Autenticação

O sistema possui uma área administrativa protegida por autenticação.

Após validar a senha:

```python
session['admin_authenticated'] = True
```

As rotas administrativas utilizam:

```python
@admin_required
```

Entre elas:

```text
/admin
/cadastrar
/editar/<id>
/deletar/<id>
```

---

## Variáveis de ambiente

Informações sensíveis não ficam diretamente no código.

Durante o desenvolvimento local, são armazenadas no `.env`:

```env
SECRET_KEY=
ADMIN_PASSWORD=

DB_HOST=
DB_PORT=5432
DB_NAME=postgres
DB_USER=
DB_PASSWORD=
```

O `.env` está incluído no `.gitignore` e não é enviado ao GitHub.

No Render, essas informações são configuradas como Environment Variables.

---

## Execução local

Crie um ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o `.env` e execute:

```bash
python app.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

---

## Deploy

A versão online utiliza:

- Render para hospedagem da aplicação Flask;
- Gunicorn como servidor de produção;
- Supabase para hospedagem do PostgreSQL.

O Render inicia a aplicação com:

```bash
gunicorn app:app
```

O deploy acompanha a versão estável utilizada pelo projeto.

---

## Segurança

O projeto utiliza práticas básicas de segurança:

- credenciais armazenadas em variáveis de ambiente;
- `.env` ignorado pelo Git;
- autenticação administrativa baseada em sessão;
- rotas administrativas protegidas;
- conexão PostgreSQL utilizando SSL;
- credenciais do banco fora do código-fonte.

---

## Sistema interativo, distribuído e adaptável

O CORINTHIANS ARCHIVE STUDIES possui características de diferentes tipos de sistemas.

### Interativo

O usuário interage diretamente com o catálogo, navega entre famílias, abre peças e utiliza os recursos da interface.

### Distribuído

Os componentes funcionam em ambientes diferentes e se comunicam pela rede:

```text
Navegador
↓
Render
↓
Flask
↓
Supabase
↓
PostgreSQL
```

### Recomendação / adaptação

O projeto passou a possuir uma camada automática de recomendação baseada nas características das peças.

O sistema analisa o conteúdo do catálogo e seleciona objetos semelhantes utilizando Machine Learning.

Atualmente essa recomendação é baseada nos próprios produtos, e não no histórico individual de cada usuário.

---

## Objetivo

O projeto funciona como ambiente de estudo e aplicação prática de conceitos de desenvolvimento de software.

Durante seu desenvolvimento foram aplicados conceitos como:

- Python
- Flask
- rotas HTTP
- arquitetura cliente-servidor
- templates Jinja2
- CRUD
- PostgreSQL
- banco de dados em nuvem
- autenticação e sessões
- variáveis de ambiente
- responsividade
- HTML
- CSS
- JavaScript
- Machine Learning
- TF-IDF
- similaridade de cosseno
- sistemas de recomendação
- deploy de aplicações web
- Git e GitHub
- Render
- Supabase

---

## Status do projeto

Concluído:

- catálogo público;
- organização por famílias e coleções;
- página individual das peças;
- autenticação administrativa;
- CRUD completo;
- PostgreSQL em nuvem;
- migração do antigo MySQL para PostgreSQL;
- hospedagem no Render;
- integração entre Flask, Render e Supabase;
- sistema de recomendação com Machine Learning;
- integração do recomendador com a página das peças;
- interface `RELATED ARCHIVE / MACHINE SELECTED`;
- aplicação publicada e validada online.

O projeto encontra-se em sua versão final planejada.

---

## Autor

Desenvolvido por **Kadu Almeida**.