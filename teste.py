import streamlit as st

st.set_page_config(
    page_title="Ficha de Registro de Consulta Médica",
    layout="wide"
)

st.title("Ficha de Registro de Consulta Médica")

# =========================
# SUBJETIVO
# =========================
with st.expander("Subjetivo", expanded=True):

    st.subheader("Queixa principal")
    queixa_principal = st.text_area(
        "Queixa principal",
        placeholder="Motivo principal da consulta...",
        height=120,
        label_visibility="collapsed",
    )

    st.subheader("HDA – História da Doença Atual")
    hda = st.text_area(
        "HDA",
        placeholder="Descrição detalhada da queixa abordada na consulta...",
        height=200,
        label_visibility="collapsed",
    )

# =========================
# OBJETIVO
# =========================
with st.expander("Objetivo", expanded=True):

    st.subheader("Exame físico")
    exame_fisico = st.text_area(
        "Exame físico",
        placeholder="Descreva os achados do exame físico...",
        height=200,
        label_visibility="collapsed",
    )

    st.subheader("Resultados de exames complementares")
    exames_texto = st.text_area(
        "Resultados dos exames",
        placeholder="Resultados de exames laboratoriais, imagem etc...",
        height=160,
        label_visibility="collapsed",
    )

    uploaded_files = st.file_uploader(
        "Upload de exames (PDF ou imagens)",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.write(f"{len(uploaded_files)} arquivo(s) enviado(s).")

# =========================
# AVALIAÇÃO
# =========================
with st.expander("Avaliação", expanded=True):

    st.subheader("Hipótese diagnóstica")
    hipotese_diagnostica = st.text_area(
        "Hipótese diagnóstica",
        placeholder="Hipótese(s) diagnóstica(s) da consulta...",
        height=160,
        label_visibility="collapsed",
    )

    st.subheader("Lista de problemas")

    lista_problemas_ativos = [
        "Hipertensão arterial (CID I10)",
        "Diabetes mellitus tipo 2 (CID E11)",
        "Dor lombar (CIAP L03)",
        "Ansiedade (CIAP P01)",
    ]

    problemas_selecionados = st.multiselect(
        "Problemas abordados nesta consulta",
        lista_problemas_ativos
    )

    adicionar_lista = st.checkbox(
        "Adicionar problemas selecionados à lista ativa do paciente"
    )

# =========================
# PLANO
# =========================
with st.expander("Plano", expanded=True):

    st.subheader("Conduta")
    conduta = st.text_area(
        "Conduta",
        placeholder="Plano terapêutico, prescrições, exames solicitados etc...",
        height=200,
        label_visibility="collapsed",
    )

    st.subheader("Pendências / Lembretes")
    pendencias = st.text_area(
        "Pendências",
        placeholder="O que precisa ser avaliado em próxima consulta ou ficou pendente...",
        height=160,
        label_visibility="collapsed",
    )

# =========================
# AÇÕES
# =========================
st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("Salvar consulta", type="primary"):
        st.success("Consulta registrada (simulação).")

with col2:
    if st.button("Limpar formulário"):
        st.rerun()
