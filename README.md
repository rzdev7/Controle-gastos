# Expense Tracker

Projeto simples em Python para registrar e acompanhar gastos utilizando MongoDB como banco de dados.

## Recursos
- Registrar gastos com descrição, valor, categoria e data.
- Listar os registros mais recentes.
- Resumo por categoria com quantidade de lançamentos e total gasto.
- Resumo mensal para um ano específico.
- Remoção de lançamentos pelo identificador.

## Pré-requisitos
- Python 3.10+
- MongoDB em execução (local ou remoto)

## Configuração
1. Crie e ative um ambiente virtual (opcional, mas recomendado).
2. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```
3. Defina as variáveis de ambiente para apontar para o seu banco:
   ```powershell
   $env:MONGODB_URI="mongodb://localhost:27017"
   $env:EXPENSE_DB_NAME="expense_tracker"
   $env:EXPENSE_COLLECTION_NAME="expenses"
   ```
   > Ajuste os valores conforme necessário. Caso não informe, os valores acima são usados como padrão.

## Uso
Execute o programa para abrir o menu interativo:
```powershell
python main.py
```

### Operações disponíveis
1. **Adicionar gasto** – Insere um novo registro. A data aceita o formato `YYYY-MM-DD`; deixe em branco para usar a data atual.
2. **Listar gastos recentes** – Solicita a quantidade de itens e exibe do mais recente para o mais antigo.
3. **Resumo por categoria** – Mostra total gasto e quantidade de lançamentos por categoria.
4. **Resumo mensal por ano** – Informe o ano (ex.: `2025`) para ver totais agrupados por mês.
5. **Remover gasto** – Remove um registro informando o ID exibido nas listagens.

## Estrutura
```
.
├── expense_tracker
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── db.py
│   └── services.py
├── main.py
├── requirements.txt
└── README.md
```

## Próximos passos
- Criar testes automatizados para validar as funções de serviço.
- Adicionar camadas de validação (ex.: valores negativos).
- Integrar com uma interface web ou API REST, se desejar expandir o projeto.
