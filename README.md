# Controle do Motorista - Sistema Web

Sistema web para controle de ganhos e despesas de motoristas de aplicativo.

## 🚀 Funcionalidades

- Sistema de login e cadastro de usuários
- Registro de abastecimentos
- Registro de trocas de óleo
- Registro de ganhos (Uber/iFood)
- Registro de despesas
- Visualização de registros
- Relatórios mensais
- Exportação de relatórios em PDF
- Dashboard com gráficos e estatísticas
- Interface responsiva e moderna

## 🛠️ Tecnologias Utilizadas

- Python 3.8+
- Flask (Framework Web)
- SQLAlchemy (ORM)
- SQLite (Banco de Dados)
- Bootstrap 5 (Framework CSS)
- Chart.js (Gráficos)
- Font Awesome (Ícones)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Navegador web moderno

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/web-controle-motorista.git
cd web-controle-motorista
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```
Edite o arquivo `.env` com suas configurações

6. Inicialize o banco de dados:
```bash
flask db upgrade
```

7. Execute o servidor de desenvolvimento:
```bash
flask run
```

O sistema estará disponível em `http://localhost:5000`

## 📦 Estrutura do Projeto

```
web-controle-motorista/
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   └── routes.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── cadastro.html
│   └── dashboard.html
├── config/
│   └── config.py
├── requirements.txt
└── README.md
```

## 🖥️ Uso

1. Acesse o sistema através do navegador
2. Faça login ou crie uma nova conta
3. No dashboard, você terá acesso a todas as funcionalidades
4. Registre seus ganhos e despesas
5. Visualize relatórios e estatísticas

## 📊 Funcionalidades do Dashboard

- Resumo financeiro
- Gráficos de ganhos e despesas
- Média de consumo de combustível
- Próxima troca de óleo
- Últimos registros
- Ações rápidas

## 🔒 Segurança

- Senhas criptografadas
- Proteção contra SQL Injection
- Autenticação de usuários
- Sessões seguras
- CSRF Protection

## 📱 Responsividade

O sistema é totalmente responsivo e pode ser acessado em:
- Computadores
- Tablets
- Smartphones

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit de suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✨ Autor

Desenvolvido por BRSinformatica - Bruno Saraiva

## 📞 Suporte

Para suporte, envie um email para suporte@brsinformatica.com.br 