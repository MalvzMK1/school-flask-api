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

# Atualizar informações de um aluno

## Método: PUT 

### Descrição: Atualizar o nome e a data de nascimento de um aluno com base no id 

```

{
  "name": "John Doe Updated",
  "birthdate": "2000-01-02"
}

```
# Excluir Aluno

## Metodo: Delete 

### Excluir o aluno com base no id

```
{
  "message": "Student deleted successfully"
}

```
# Obter turma de Alunos

## Metodo: get 

### Vai rertorna as turmas que estão associdas ao aluno

```

[
  {
    "id": 1,
    "course_name": "Mathematics",
    "teacher": "Mr. Smith"
  },
  ...
]

```
