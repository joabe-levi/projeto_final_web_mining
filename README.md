# Projeto Web Mining Analítico

Sistema de extração, transformação e carregamento (ETL) para análise de dados financeiros, desenvolvido em Python com pipeline modular e persistência em DuckDB. Inclui web scraping do InfoMoney e integração com API YFinance para dados de criptomoedas.

## 📋 Índice

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pipeline ETL](#pipeline-etl)
- [Exemplos de Uso](#exemplos-de-uso)
- [Contribuição](#contribuição)

## 🚀 Funcionalidades

### Pipeline de Scraping (InfoMoney)
- **Extração Automática**: Web scraping inteligente do InfoMoney com Selenium
- **Carregamento Dinâmico**: Scroll automático para carregar mais notícias
- **Validação de Dados**: Filtragem automática de notícias incompletas
- **Análise Temporal**: Conversão de datas relativas para absolutas
- **Persistência**: Armazenamento em banco DuckDB com pandas

### Pipeline de API (YFinance)
- **Extração de Dados Financeiros**: Integração com API YFinance para criptomoedas
- **Análise Técnica**: Cálculo de médias móveis (7d e 30d) e variação percentual
- **Enriquecimento de Dados**: Adição de indicadores técnicos automáticos
- **Persistência Dupla**: Armazenamento em tabelas `instruments` e `prices`

### Funcionalidades Gerais
- **Pipeline Modular**: Arquitetura ETL flexível e extensível
- **Interface CLI**: Execução via linha de comando com parâmetros
- **Logging Avançado**: Sistema de logs estruturado com diferentes níveis
- **Configuração Flexível**: Suporte a variáveis de ambiente

## 🛠 Tecnologias

### Core
- **Python 3.8+**
- **DuckDB**: Banco de dados analítico
- **Pandas**: Manipulação de dados
- **NumPy**: Computação numérica

### Web Scraping
- **Selenium**: Web scraping e automação
- **BeautifulSoup**: Parsing de HTML
- **WebDriver Manager**: Gerenciamento automático de drivers

### APIs e Dados Financeiros
- **YFinance**: API para dados financeiros
- **Requests**: Cliente HTTP

### Utilitários
- **Argparse**: Interface de linha de comando
- **Python-dotenv**: Gerenciamento de variáveis de ambiente
- **LXML**: Parser XML/HTML rápido

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd projeto_web_mining_analitico
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Instale o ChromeDriver (se necessário)

O projeto usa o `webdriver-manager` que baixa automaticamente o ChromeDriver, mas você pode instalar manualmente:

```bash
# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# macOS
brew install chromedriver

# Windows
# Baixe do site oficial do Chrome
```

### 5. Instale dependências adicionais (opcional)

Para desenvolvimento e testes:

```bash
pip install pytest black flake8
```

## ⚙️ Configuração

### Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
# Caminho do banco de dados
db_path=data/dck.db
```

## 🎯 Como Executar

### Execução Básica

```bash
python main.py
```

### Parâmetros Disponíveis

#### `--scrapping`
Executa apenas o pipeline de scraping:

```bash
python main.py --scrapping
```

#### `--api`
Executa apenas o pipeline da API (YFinance):

```bash
python main.py --api
```

#### Execução sem parâmetros
Executa todos os pipelines disponíveis:

```bash
python main.py
```

### Exemplos de Uso

```bash
# Executar apenas scraping
python main.py --scrapping

# Executar todos os pipelines
python main.py

# Ver ajuda
python main.py --help
```

## 📁 Estrutura do Projeto

```
projeto_web_mining_analitico/
├── main.py                          # Ponto de entrada principal
├── requirements.txt                  # Dependências do projeto
├── README.md                        # Este arquivo
├── bases/                          # Interfaces e classes base
│   ├── interfaces/
│   │   ├── extractor.py            # Interface para extração
│   │   ├── transformers.py         # Interface para transformação
│   │   ├── loader.py               # Interface para carregamento
│   │   └── pipeline.py              # Interface para pipelines
│   └── crawlers/
│       └── base_crawler.py         # Classe base para crawlers
├── src/                            # Código fonte principal
│   ├── config/                     # Configurações
│   │   ├── settings.py             # Configurações do projeto
│   │   └── logging.py              # Configuração de logs
│   ├── scrapping/                  # Pipeline de scraping (InfoMoney)
│   │   ├── pipeline.py             # Pipeline principal
│   │   ├── crawlers/
│   │   │   └── infomoney.py        # Crawler do InfoMoney
│   │   └── tasks/
│   │       ├── extractor.py        # Extrator de dados
│   │       ├── transformer.py      # Transformador/validador
│   │       └── loader.py           # Carregador no banco
│   └── api/                        # Pipeline da API (YFinance)
│       ├── pipeline.py             # Pipeline YFinance
│       └── tasks/
│           ├── extractor.py        # Extrator YFinance
│           ├── transformers.py     # Transformador YFinance
│           └── loader.py           # Carregador YFinance
├── data/                          # Diretório de dados
│   └── dck.db                     # Banco DuckDB
└── logs/                          # Diretório de logs
    └── app.log                    # Arquivo de log
```

## 🔄 Pipeline ETL

### Pipeline de Scraping (InfoMoney)

#### 1. **Extração (Extract)**
- Navegação automática no InfoMoney com Selenium
- Carregamento dinâmico de notícias (scroll automático)
- Parsing de HTML com BeautifulSoup
- Conversão de datas relativas para absolutas
- Extração de: tipo, título, URL e data da notícia

#### 2. **Transformação (Transform)**
- Validação de campos obrigatórios (tipo, título, URL, data)
- Filtragem de notícias incompletas
- Limpeza e padronização de dados
- Geração de metadados de processamento

#### 3. **Carregamento (Load)**
- Persistência em DuckDB (tabela `news`)
- Inserção em lote com pandas
- Geração automática de IDs sequenciais
- Métodos de consulta: recentes, por tipo, totais

### Pipeline de API (YFinance)

#### 1. **Extração (Extract)**
- Integração com API YFinance
- Download de dados históricos (6 meses)
- Suporte a diferentes símbolos e intervalos
- Tratamento de erros de API

#### 2. **Transformação (Transform)**
- Cálculo de variação percentual (pct_change)
- Médias móveis de 7 e 30 dias
- Limpeza de dados nulos
- Remoção de duplicatas por data

#### 3. **Carregamento (Load)**
- Persistência em duas tabelas: `instruments` e `prices`
- Relacionamento entre instrumentos e preços
- Suporte a múltiplos ativos
- Estrutura normalizada para análise

## 📊 Exemplos de Uso

### Executar Pipeline Completo

```bash
python main.py
```

**Saída esperada:**
```
Executando todos os pipelines...
🚀 Iniciando pipeline de Scraping...
📡 Iniciando extração de dados com InfoMoneyCrawler...
Loaded 150 items.
Extraídas 120 notícias com dados completos.
✅ Extração concluída com sucesso (120 registros).
⚙️ Iniciando transformação de dados...
✅ Transformação concluída. 115 registros processados.
💾 Iniciando carga dos dados...
✅ 115 notícias inseridas no banco com sucesso!
🏁 Pipeline de Scraping finalizado em 45.23s

🚀 Iniciando pipeline de ETL para YFinance...
📡 Iniciando extração de dados da API YFinance...
✅ Extração concluída com sucesso (180 registros).
⚙️ Iniciando transformação dos dados extraídos...
✅ Transformação concluída. 180 registros processados.
💾 Iniciando carga dos dados no banco DuckDB...
✅ 180 registros inseridos na tabela 'prices' com sucesso.
🏁 Pipeline YFinance finalizado em 12.45s
```

### Executar Apenas Scraping

```bash
python main.py --scrapping
```

### Consultar Dados no Banco

#### Notícias (Pipeline de Scraping)
```python
import duckdb

# Conectar ao banco
conn = duckdb.connect('data/dck.db')

# Consultar notícias recentes
result = conn.execute("""
    SELECT tipo, titulo, data_noticia 
    FROM news 
    ORDER BY data_importacao DESC 
    LIMIT 10
""").fetchall()

for row in result:
    print(f"[{row[0]}] {row[1]} - {row[2]}")
```

#### Dados Financeiros (Pipeline de API)
```python
import duckdb

# Conectar ao banco
conn = duckdb.connect('data/dck.db')

# Consultar preços recentes do Bitcoin
result = conn.execute("""
    SELECT date, close, pct_change, ma_7d, ma_30d
    FROM prices 
    WHERE symbol = 'BTC-USD'
    ORDER BY date DESC 
    LIMIT 10
""").fetchall()

for row in result:
    print(f"{row[0]}: R$ {row[1]:.2f} ({row[2]:.2%}) - MA7: {row[3]:.2f} - MA30: {row[4]:.2f}")
```

## 🗄️ Estrutura do Banco de Dados

### Tabela `news` (Pipeline de Scraping)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | ID único (auto-incremento) |
| `data_importacao` | TIMESTAMP | Data/hora da importação |
| `tipo` | VARCHAR | Categoria da notícia |
| `titulo` | VARCHAR | Título da notícia |
| `url` | VARCHAR | URL da notícia |
| `data_noticia` | TIMESTAMP | Data da notícia |

### Tabela `instruments` (Pipeline de API)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | ID único (auto-incremento) |
| `symbol` | VARCHAR | Símbolo do ativo (ex: BTC-USD) |
| `name` | VARCHAR | Nome do ativo |
| `sector` | VARCHAR | Setor (ex: Crypto) |
| `created_at` | TIMESTAMP | Data de criação do registro |

### Tabela `prices` (Pipeline de API)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | ID único (auto-incremento) |
| `symbol` | VARCHAR | Símbolo do ativo |
| `date` | DATE | Data do preço |
| `open` | DOUBLE | Preço de abertura |
| `high` | DOUBLE | Preço máximo |
| `low` | DOUBLE | Preço mínimo |
| `close` | DOUBLE | Preço de fechamento |
| `adj_close` | DOUBLE | Preço ajustado |
| `volume` | BIGINT | Volume negociado |
| `pct_change` | DOUBLE | Variação percentual |
| `ma_7d` | DOUBLE | Média móvel 7 dias |
| `ma_30d` | DOUBLE | Média móvel 30 dias |

## 🔧 Desenvolvimento

### Adicionando Novos Crawlers

1. Crie uma nova classe herdando de `BaseCrawler`
2. Implemente os métodos `run()` e `_parser()`
3. Adicione ao pipeline de extração

### Adicionando Novos Transformers

1. Implemente a interface `TransformInterface`
2. Adicione lógica de validação no método `is_valid()`
3. Configure no pipeline

### Adicionando Novos Loaders

1. Implemente a interface `LoadInterface`
2. Configure persistência no método `do_load()`
3. Adicione ao pipeline

## 🐛 Solução de Problemas

### Erro de ChromeDriver

```bash
# Instalar ChromeDriver manualmente
pip install webdriver-manager
```

### Erro de Dependências

```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### Erro de Permissão no Banco

```bash
# Verificar permissões do diretório data/
chmod 755 data/
```

## 📈 Próximos Passos

- [x] Implementar pipeline da API (YFinance)
- [ ] Adicionar mais fontes de dados (Alpha Vantage, Yahoo Finance)
- [ ] Interface web para visualização
- [ ] Análise de sentimentos das notícias
- [ ] Dashboard em tempo real
- [ ] Notificações automáticas
- [ ] Análise de correlação entre notícias e preços
- [ ] Machine Learning para previsão de preços

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Joabe Levi** - *Desenvolvimento inicial* - [GitHub](https://github.com/joabe-levi)

## 📞 Contato

Para dúvidas ou sugestões, entre em contato através dos issues do GitHub ou por email.

---

**Desenvolvido com ❤️ para análise de dados financeiros**
