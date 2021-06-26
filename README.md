# Resolução do exercício


### Documentação

[Documentação das Rotas da API via OpenAPI3](http://localhost/docs)

Foi implementado autenticação JWT nos endpoints da API

| Username | Password |
| -------- | -------- |
| admin  | admin  |

##### Build e execução dos containeres
```sh
docker-compose up --build -d
```

##### Execução dos testes iniciais(dentro do container)
```sh
cd /home/src/
pytest
```

##### Estrutura do .env no diretório /backend 

```sh
DEBUG=True
PROJECT_NAME=API Luiz
SECRET_KEY=l1d2b99ae9f502cd9bbb3c345337c0ca4e708b1c9e9fe1dbbcf30156c3630565a

MARIADB_USER=user
MARIADB_PASS=123456
MARIADB_HOST=db
MARIADB_DB=db

```

----
# Exercicio Proposto    

## Backend
Desenvolver uma API JSON REST na *linguagem a sua escolha*, que utilize os métodos (​GET​, ​POST​, ​PUT​,
DELETE​).

## Frontend
UI/UX fica a critério do desenvolvedor porém deverá ser SPA (single-page
application) e atender o consumo de todos endpoints da API 

## Especificação
Monte uma base de desenvolvedores com a seguinte estrutura:

```
nome: varchar
sexo: char
idade: integer
hobby: varchar
datanascimento: date
```

Utilize o ​banco de dados​ de sua preferência para armazenar os dados que a API irá
consumir.

## API endpoints

```
GET /developers
Codes 200
```
Retorna todos os desenvolvedores

```
GET /developers?
Codes 200 / 404
```
Retorna os desenvolvedores de acordo com o termo passado via querystring e
paginação

```
GET /developers/{id}
Codes 200 / 404
```
Retorna os dados de um desenvolvedor

```
POST /developers
Codes 201 / 400
```
Adiciona um novo desenvolvedor

```
PUT /developers/{id}
Codes 200 / 400
```
Atualiza os dados de um desenvolvedor

```
DELETE /developers/{id}
Codes 204 / 400
```
Apaga o registro de um desenvolvedor


## Entrega
A aplicação deve rodar em docker, possuir um script para geração das tabelas no banco de dados e TESTES UNITÁRIOS.

Após finalizado o link do projeto, por e-mail, no github com explicação no README
