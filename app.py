import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ===================== CONFIGURAÇÃO GERAL =====================
st.set_page_config(
    page_title="Dashboard AGT - Usabilidade dos Sistemas",
    layout="wide",
    page_icon="📊"
)

st.markdown("""
    <style>
        .big-font { font-size:24px !important; font-weight:700; }
        .small-font { font-size:16px !important; color:gray; }
        .stPlotlyChart { background-color: #f9f9f9; border-radius: 10px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# ===================== DADOS =====================
data = {
    'Participante': ['P1', 'P2', 'P3'],
    'Função na AGT': ['Atendimento ao Público', 'Atendimento ao Público', 'Contencioso e Execuções Fiscais'],
    'Tempo de Serviço': ['1 a 5 anos', '1 a 5 anos', '1 a 5 anos'],
    'Nível de Escolaridade': ['Ensino Superior (Graduação)', 'Ensino Superior (Graduação)', 'Ensino Médio'],
    'Sexo': ['Masculino', 'Masculino', 'Masculino'],
    'Idade': ['26-35 anos', '26-35 anos', '26-35 anos'],
    'Sistemas Utilizados': [['SIGT', 'Portal Administração AGT'],
                            ['SIGT', 'Portal Administração AGT', 'APEX', 'Portal SAFT'],
                            ['SIGT', 'Portal Administração AGT', 'APEX']],
    'Frequência Utilização': ['Diariamente', 'Diariamente', 'Diariamente'],
    'Tarefas': [['Consulta de informações', 'Lançamento de impostos', 'Emissão de documentos'],
                ['Consulta de informações', 'Cadastro de contribuintes', 'Lançamento de impostos', 'Emissão de documentos'],
                ['Consulta de informações', 'Lançamento de impostos', 'Emissão de documentos', 'Reporte de Informações']],
    'Recebeu Treinamento': ['Sim', 'Sim', 'Sim'],
    'Opinião Treinamento': ['Bom', 'Bom', 'Regular'],
    'Q_Facil_Usar': [4, 4, 4],
    'Q_Facil_Info': [4, 4, 4],
    'Q_Instrucoes_Claras': [4, 4, 4],
    'Q_Sistemas_Rapidos': [4, 4, 4],
    'Q_Raramente_Erros': [4, 4, 4],
    'Q_Facil_Corrigir_Erros': [4, 5, 4],
    'Q_Sistemas_Confiaveis': [4, 4, 4],
    'Q_Funcionalidades_Atendem': [5, 4, 4],
    'Q_Satisfeito_Experiencia': [4, 4, 4],
    'Q_Sistemas_Eficiencia': [4, 4, 4],
    'Q_Sistemas_Acessiveis': [4, 4, 4],
    'Q_Interface_Agradavel': [4, 5, 4],
    'Positivos': [
        'Fácil manuseamento, dinamização do trabalho, facilidade na execução de tarefas.',
        'Acesso às informações sem recorrer a arquivos físicos. Uniformização dos dados.',
        'Acesso aos sistemas sem muitos esforços e facilidade de controlo.'
    ],
    'Negativos': [
        'Não parametrização do sistema à legislação fiscal.',
        'Muitas plataformas de trabalho dificultam integração de dados.',
        'Muitas plataformas de trabalho dificultam integração de dados.'
    ],
    'Melhorias': [
        'Parametrização com a legislação angolana.',
        'Fusão das plataformas e melhoria do servidor central.',
        'Integração das plataformas para uso eficiente.'
    ],
    'Sugestoes': [
        'O sistema deve enquadrar-se com a realidade das empresas nacionais.',
        'Nada, apenas devem melhorar.',
        'No momento não! Apenas melhorar os sistemas.'
    ]
}

df = pd.DataFrame(data)

# ===================== SIDEBAR =====================
st.sidebar.header("⚙️ Filtros")

funcoes = st.sidebar.multiselect(
    "Função na AGT", df["Função na AGT"].unique(), default=df["Função na AGT"].unique()
)
sexos = st.sidebar.multiselect(
    "Sexo", df["Sexo"].unique(), default=df["Sexo"].unique()
)
tempos = st.sidebar.multiselect(
    "Tempo de Serviço", df["Tempo de Serviço"].unique(), default=df["Tempo de Serviço"].unique()
)

df_filtered = df[
    (df["Função na AGT"].isin(funcoes)) &
    (df["Sexo"].isin(sexos)) &
    (df["Tempo de Serviço"].isin(tempos))
]

# ===================== TÍTULO =====================
st.title("📊 Dashboard de Usabilidade dos Sistemas Informáticos da AGT (Luau)")
st.markdown("### Avaliação da experiência dos colaboradores com os sistemas institucionais")

# ===================== INDICADORES =====================
col1, col2, col3 = st.columns(3)
col1.metric("👥 Participantes", len(df_filtered))
col2.metric("🧑‍💼 Funções distintas", df_filtered["Função na AGT"].nunique())
col3.metric("📈 Média Geral de Satisfação", f"{df_filtered['Q_Satisfeito_Experiencia'].mean():.1f}/5")

# ===================== SEÇÃO 1: DEMOGRÁFICA =====================
with st.expander("I. Informações Demográficas", expanded=True):
    col1, col2 = st.columns(2)
    fig1 = px.bar(df_filtered, x='Função na AGT', color='Função na AGT',
                  title='Distribuição por Função', color_discrete_sequence=px.colors.qualitative.Safe)
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(df_filtered, names='Nível de Escolaridade', title='Nível de Escolaridade',
                  color_discrete_sequence=px.colors.sequential.Viridis)
    col2.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    fig3 = px.bar(df_filtered, x='Tempo de Serviço', color='Tempo de Serviço', title='Tempo de Serviço')
    col3.plotly_chart(fig3, use_container_width=True)

    fig4 = px.bar(df_filtered, x='Idade', color='Idade', title='Faixa Etária')
    col4.plotly_chart(fig4, use_container_width=True)

# ===================== SEÇÃO 2: UTILIZAÇÃO =====================
with st.expander("II. Utilização dos Sistemas", expanded=True):
    sistemas_flat = [item for sublist in df_filtered['Sistemas Utilizados'] for item in sublist]
    df_sistemas = pd.DataFrame(sistemas_flat, columns=['Sistema'])
    fig_sys = px.bar(df_sistemas, x='Sistema', color='Sistema',
                     title='Sistemas Informáticos Utilizados',
                     color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig_sys, use_container_width=True)

    col1, col2 = st.columns(2)
    fig_freq = px.bar(df_filtered, x='Frequência Utilização', color='Frequência Utilização',
                      title='Frequência de Utilização')
    col1.plotly_chart(fig_freq, use_container_width=True)

    fig_train = px.pie(df_filtered, names='Recebeu Treinamento',
                       title='Treinamento Recebido', color_discrete_sequence=['#00cc96', '#ff6361'])
    col2.plotly_chart(fig_train, use_container_width=True)

    fig_op = px.bar(df_filtered, x='Opinião Treinamento', color='Opinião Treinamento',
                    title='Opinião sobre o Treinamento')
    st.plotly_chart(fig_op, use_container_width=True)

# ===================== SEÇÃO 3: AVALIAÇÃO =====================
with st.expander("III. Avaliação da Usabilidade e Experiência", expanded=True):
    questions_df = df_filtered[[col for col in df.columns if col.startswith('Q_')]]
    mean_scores = questions_df.mean().reset_index()
    mean_scores.columns = ['Questão', 'Média']

    mapping = {
        'Q_Facil_Usar': 'Facilidade de uso',
        'Q_Facil_Info': 'Facilidade de encontrar informações',
        'Q_Instrucoes_Claras': 'Instruções claras',
        'Q_Sistemas_Rapidos': 'Rapidez dos sistemas',
        'Q_Raramente_Erros': 'Poucos erros',
        'Q_Facil_Corrigir_Erros': 'Facilidade em corrigir erros',
        'Q_Sistemas_Confiaveis': 'Confiabilidade',
        'Q_Funcionalidades_Atendem': 'Funcionalidades adequadas',
        'Q_Satisfeito_Experiencia': 'Satisfação geral',
        'Q_Sistemas_Eficiencia': 'Eficiência no trabalho',
        'Q_Sistemas_Acessiveis': 'Acessibilidade',
        'Q_Interface_Agradavel': 'Interface agradável'
    }
    mean_scores["Questão"] = mean_scores["Questão"].map(mapping)

    fig_eval = px.bar(mean_scores, x='Média', y='Questão', orientation='h',
                      color='Média', color_continuous_scale='viridis',
                      title='Avaliação Média das Questões (1 a 5)', range_x=[1,5])
    st.plotly_chart(fig_eval, use_container_width=True)

# ===================== SEÇÃO 4: COMENTÁRIOS =====================
with st.expander("IV. Comentários e Sugestões", expanded=False):
    st.subheader("💚 Pontos Positivos")
    for i, p in enumerate(df_filtered['Positivos']):
        st.markdown(f"**{df_filtered['Participante'][i]}:** {p}")

    st.subheader("🔴 Pontos Negativos")
    for i, n in enumerate(df_filtered['Negativos']):
        st.markdown(f"**{df_filtered['Participante'][i]}:** {n}")

    st.subheader("🔧 Melhorias Sugeridas")
    for i, m in enumerate(df_filtered['Melhorias']):
        st.markdown(f"**{df_filtered['Participante'][i]}:** {m}")

    st.subheader("💬 Outras Sugestões")
    for i, s in enumerate(df_filtered['Sugestoes']):
        st.markdown(f"**{df_filtered['Participante'][i]}:** {s}")

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>© 2025 AGT - Dashboard de Usabilidade</p>", unsafe_allow_html=True)
