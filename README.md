# Painel Flask

Este é um projeto de aplicação web desenvolvido com Flask, que serve como um painel de controle. O projeto é estruturado para facilitar a manutenção e a escalabilidade.

## Estrutura do Projeto

```
painel_flask
├── app.py                # Ponto de entrada da aplicação Flask
├── config.py             # Configurações da aplicação
├── static                # Arquivos estáticos (CSS, JS, imagens)
│   ├── css               # Folhas de estilo CSS
│   ├── js                # Scripts JavaScript
│   └── images            # Imagens utilizadas na aplicação
├── templates             # Templates HTML
│   ├── base.html         # Template base
│   ├── login.html        # Página de login
│   ├── dashboard.html     # Página do dashboard
│   └── partials          # Templates parciais
│       ├── navbar.html    # Barra de navegação
│       └── footer.html    # Rodapé
├── auth                  # Módulo de autenticação
│   ├── __init__.py       # Inicialização do módulo
│   ├── routes.py         # Rotas de autenticação
│   └── utils.py          # Funções utilitárias de autenticação
├── tools                 # Ferramentas auxiliares
│   └── helpers.py        # Funções auxiliares
└── README.md             # Documentação do projeto
```

## Instalação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   ```
2. Navegue até o diretório do projeto:
   ```
   cd painel_flask
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para iniciar a aplicação, execute o seguinte comando:
```
python app.py
```

A aplicação estará disponível em `http://127.0.0.1:5000`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.