import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# --- 1. CONFIGURAÇÃO E MEMÓRIA ---
st.set_page_config(page_title="Rascs", page_icon="https://cdn-icons-png.flaticon.com/512/9942/9942242.png", layout="wide")

if 'dados_prontos' not in st.session_state:
    st.session_state.dados_prontos = False
    st.session_state.df = None
    st.session_state.nome_comp = ""
    st.session_state.id_comp = ""

# --- 2. FUNÇÃO DE BUSCA ---
def buscar_dados_wca(competition_id):
    url_api = "https://live.worldcubeassociation.org/api/graphql"
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    query = """
    query GetCompetitionResults($id: ID!) {
      competition(id: $id) {
        name
        competitionEvents {
          event { name }
          rounds {
            id
            number
            results {
              ranking
              person { name }
            }
          }
        }
      }
    }
    """
    try:
        response = requests.post(url_api, json={'query': query, 'variables': {"id": competition_id}}, headers=headers)
        return response.json()['data']['competition']
    except:
        return None

# --- 3. CABEÇALHO ---
st.markdown("<h1 style='text-align: center;'>🔴🟡🔵⚪RASCS⚪🔵🟡🔴</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'><b>WCA Live Ranking Score System</b></h3>", unsafe_allow_html=True)
st.divider()

# --- 4. ÁREA DE INPUT / BOTÕES (ESTABILIZADA) ---
# Se não tem dados, mostra o campo de busca
if not st.session_state.dados_prontos:
    url_comp = st.text_input("Insira o link da competição (WCA Live):", placeholder="https://live.worldcubeassociation.org/competitions/1")
    if st.button("Analisar Competição", use_container_width=True):
        if url_comp:
            comp_id = url_comp.split('/')[-1]
            with st.spinner('Extraindo dados...'):
                dados = buscar_dados_wca(comp_id)
                if dados:
                    lista = []
                    for event in dados['competitionEvents']:
                        for rd in event['rounds']:
                            tc = len(rd['results'])
                            for res in rd['results']:
                                if res['ranking']:
                                    lista.append({
                                        "Evento": event['event']['name'],
                                        "Round": f"{event['event']['name']} - R{rd['number']}",
                                        "Nome": res['person']['name'],
                                        "Posicao": res['ranking'],
                                        "Total de Competidores": tc,
                                        "Pontos": round(tc / (res['ranking'] + 1), 2)
                                    })
                    st.session_state.df = pd.DataFrame(lista)
                    st.session_state.nome_comp = dados['name']
                    st.session_state.id_comp = comp_id
                    st.session_state.dados_prontos = True
                    st.rerun() # Força o app a redesenhar já com os dados salvos
                else:
                    st.error("Competição não encontrada.")
        else:
            st.warning("Insira um link.")

# Se já tem dados, mostra o botão de "Consultar Outra"
else:
    st.info(f"📍 Exibindo resultados de: **{st.session_state.nome_comp}**")
    if st.button("Consultar Outra Competição", type="secondary"):
        st.session_state.dados_prontos = False
        st.session_state.df = None
        st.rerun()

# --- 5. EXIBIÇÃO EM ABAS (SÓ APARECE SE DADOS_PRONTOS FOR TRUE) ---
if st.session_state.dados_prontos:
    df = st.session_state.df
    
    # Preparação dos dados
    ranking_geral = df.groupby('Nome')['Pontos'].sum().sort_values(ascending=False).reset_index()
    ranking_geral.columns = ['Nome', 'Pontos Totais']
    ranking_geral['Pontos Totais'] = ranking_geral['Pontos Totais'].round(2)
    
    tab_geral, tab_rodadas, tab_panorama, tab_export = st.tabs([
        "📊 Ranking Geral", "📂 Por Rodada", "👤 Panorama Individual", "📥 Exportar Dados"
    ])

    with tab_geral:
        rank_vis = ranking_geral.copy()
        rank_vis.insert(0, 'Rank', range(1, len(rank_vis) + 1))
        st.dataframe(rank_vis, use_container_width=True, hide_index=True)

    with tab_rodadas:
        rds = sorted(df['Round'].unique())
        sel_rd = st.selectbox("Selecione a Rodada:", rds, key="sel_rd_estavel")
        df_rd = df[df['Round'] == sel_rd][['Posicao', 'Nome', 'Pontos']].sort_values('Posicao')
        st.dataframe(df_rd, use_container_width=True, hide_index=True)

    with tab_panorama:
        nomes_f = sorted(df['Nome'].unique())
        sel_nome = st.selectbox("Buscar competidor:", nomes_f, key="sel_nome_estavel")
        
        detalhe = df[df['Nome'] == sel_nome][['Round', 'Posicao', 'Total de Competidores', 'Pontos']]
        # Visual limpo sem o index lateral
        st.dataframe(detalhe, use_container_width=True, hide_index=True)
        
        total_p = ranking_geral[ranking_geral['Nome'] == sel_nome]['Pontos Totais'].values[0]
        st.metric("Total de Pontos PSYRC", f"{total_p:.2f}")

    with tab_export:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            ranking_geral.to_excel(writer, sheet_name='Totais', index=False)
            df.to_excel(writer, sheet_name='Detalhes', index=False)
        st.download_button("📥 Baixar Planilha Completa", output.getvalue(), 
                          file_name=f"PSYRC_{st.session_state.id_comp}.xlsx",
                          key="download_final")