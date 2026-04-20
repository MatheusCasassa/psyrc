# 🔴🟡🔵⚪ RASCS ⚪🔵🟡🔴
### **WCA Live Point System Rank Calculator**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://rascs.streamlit.app)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![WCA](https://img.shields.io/badge/WCA-Live_API-green.svg)

---

## 🌎 Overview / Visão Geral

**🇺🇸** RASCS is a Streamlit-based application designed to be a "scoring calculation system" for WCA competitions, using real-time data from **WCA Live**. It allows organizers and community members to score competitions dynamically as results are posted. 

**🇧🇷** O RASCS é uma aplicação desenvolvida em Streamlit com o objetivo de ser um sistema de cálculo de pontuação para competições da WCA, utilizando dados em tempo real do **WCA Live**. Ele permite que organizadores e a comunidade acompanhem a pontuação dinâmica conforme os resultados são publicados.

---

## 🧮 The Formula / A Fórmula

This project uses the calculation method created by **APS (Associação Portuguesa de Speedcubing)**.  
*Este projeto utiliza o método de cálculo criado pela **APS (Associação Portuguesa de Speedcubing)**.*

A pontuação de cada rodada é calculada da seguinte forma:

$$Pt = \frac{TC}{P + 1}$$

* **Pt**: Pontos obtidos / *Points earned*
* **TC**: Total de Competidores na rodada / *Total Competitors in the round*
* **P**: Posição do competidor / *Competitor's ranking*

---

## 🚀 Features / Funcionalidades

* **Real-time Fetching:** Integração direta com a API GraphQL do WCA Live.
* **Detailed Analytics:** Ranking geral, visão por rodada e panorama individual do competidor.
* **Export to Excel:** Gera planilhas formatadas com os totais e detalhes de cada round.
* **Searchable UI:** Busca rápida por competidores e filtros por eventos.

---

## 🛠️ Tech Stack / Tecnologias

* **Language:** Python
* **Frontend/Hosting:** Streamlit
* **Data Analysis:** Pandas
* **API:** GraphQL (Requests)
* **Export:** XlsxWriter

---

## 🤝 Collaboration & Credits / Colaboração e Créditos

This initiative is a project from **Cubing SP (Associação de Speedcubing São Paulo)**.
* **Concept:** APS (Associação Portuguesa de Speedcubing) - [Link Reference](https://www.instagram.com/p/DS-H9wJiAoi)
* **Developer:** [Matheus Casassa](https://github.com/MatheusCasassa)

---

## 📝 How to use / Como usar

1.  Acesse o link da competição no [WCA Live](https://live.worldcubeassociation.org/).
2.  Copie o URL e cole no campo de entrada do RASCS.
3.  Clique em **Analisar Competição**.
4.  Navegue pelas abas para ver os resultados e exporte para Excel se necessário.
