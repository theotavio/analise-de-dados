# A Guerra dos Consoles e o Choque Cultural

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.66-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interativo-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Dados-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

Aplicação web analítica e interativa desenvolvida para explorar quatro décadas de vendas globais de jogos eletrônicos (1980 a 2016), padrões de consumo regional e eficiência comercial de publicadoras.

---

## Links do Projeto

* **Dashboard Online (Streamlit Cloud):** [https://guerradeconsoles.streamlit.app/](https://guerradeconsoles.streamlit.app/)
* **Base de Dados Original (Kaggle):** [Video Games Sales Dataset (vgsales)](https://www.kaggle.com/datasets/gregorut/videogamesales)

---

## Visualizações Desenvolvidas

1. **Corrida das Plataformas no Tempo:** Animação temporal com controle interativo de reprodução (Play/Pause) que demonstra a evolução acumulada e a dança de liderança entre os 10 maiores consoles da história.
2. **Fluxo de Mercado (Fabricantes para Gêneros):** Diagrama de fluxo Alluvial/Sankey que mapeia visualmente as conexões de faturamento dos ecossistemas de hardware diretamente para os gêneros de jogos.
3. **Hierarquia Radial Concéntrica (Sunburst):** Visualização em anéis concêntricos que decompõe o faturamento em camadas navegáveis por clique (*Fabricante ➔ Plataforma ➔ Gênero*).
4. **Disparidade Cultural Regional (Dumbbell):** Modelo de halteres comparativos que isola o market share percentual de cada gênero, evidenciando o abismo entre o mercado norte-americano (Shooters e Ação) e o japonês (JRPGs).
5. **Matriz de Concentração de Vendas:** Heatmap com valores numéricos explícitos indicando o volume de vendas globais no cruzamento entre plataformas e gêneros.

---

## Estrutura de Arquivos

```text
analise-de-dados/
├── .streamlit/
│   └── config.toml         # Configuração nativa forçando o modo claro
├── data/
│   ├── vgsales.csv         # Dataset original bruto extraído do VGChartz
│   └── vgsales_cleaned.csv # Dataset tratado e enriquecido com fabricantes e gerações
├── src/
│   └── prepare_data.py     # Script de limpeza e enriquecimento dos dados
├── .gitignore              # Ignora cache e temporários
├── app.py                  # Aplicação web principal do Streamlit
└── README.md               # Documentação completa do projeto
```

---

## Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/theotavio/analise-de-dados.git
cd analise-de-dados
```

### 2. Instalar as dependências
```bash
pip install streamlit plotly pandas
```

### 3. Iniciar o dashboard
```bash
streamlit run app.py
```
O navegador abrirá automaticamente em `http://localhost:8501`.
