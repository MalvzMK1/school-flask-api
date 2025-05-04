# API Escola

Uma API em Flask que gerencia `professores`, `turmas` e `alunos`.

## Objetivo

Este projeto foi feito para a matéria de Desenvolvimento de APIs da faculdade. O objetivo é desenvolver aos poucos um sistema bem estruturado em Python usando Flask. Esta é a primeira versão do projeto, a mais simples.

## Como Começar

Para rodar o projeto, é necessário seguir o passo a passo:

### Inicialização padrão

1. **Crie a pasta venv**

```bash
python -m venv venv
# ou
python3 -m venv venv
```

2. **Ative o ambiente**

```bash
./venv/Scripts/activate
# ou se estiver em um terminal bash...
source ./venv/Scripts/activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Rode o projeto**

```bash
flask run
```

### Inicialização com Docker

1. Tenha o Docker instalado em sua máquina

```sh
$ docker -v
  Docker version 27.5.0, build a187fa5

$ docker compose version
  Docker Compose version v2.32.4
```

2. Rode com o Docker Compose

Exemplo:

```sh
docker compose up --build
```

## Testes E2E

Com a API rodando é possível executar os testes com o seguinte comando:

```bash
python -m unittest teste.py
```

## Relacionamento entre Entidades

1. **Professor**

   - Tem N turmas

2. **Turma**

   - Tem N alunos
   - Tem 1 professor

3. **Aluno**
   - Tem N turmas
