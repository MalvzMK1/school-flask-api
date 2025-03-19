# DOCUMENTAÇÃO API

## GET /students

### Descrição: 

Recupera todos os alunos.

```
{
  "students": [
    {
      "id": 1,
      "name": "John Doe",
      "created_at": "2025-03-18T12:34:56"
    },
    ...
  ]
}
```
# Obter um aluno específico pelo ID

## Método: GET 

### Descrição: Retorna os detalhes de um aluno com base no id 

``` {
  "id": 1,
  "name": "John Doe",
  "created_at": "2021-05-01T12:00:00"
}
```

# Criar um novo aluno

## Método: POST

### Descrição: Cria um novo aluno, a partir do corpo da requisição que deve incluir name e birthdate.
```
Corpo da requisição:
json

{
  "name": "John Doe",
  "birthdate": "2000-01-01"
}

```
```
{
  "id": 1,
  "message": "Student created successfully"
}
```
