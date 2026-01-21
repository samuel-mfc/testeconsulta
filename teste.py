import streamlit as st

st.set_page_config(page_title="Ficha de Registro de Consulta Médica", layout="wide")

st.title("Ficha de Registro de Consulta Médica")

# =========================
# SUBJETIVO
# =========================
st.header("Subjetivo")

with st.expander("Queixa principal", expanded=True):
    queixa_principal = st.text_area(
        "Texto",
        placeholder="Motivo principal da consulta...",
        key="queixa_principal",
        height=140,
        label_visibility="collapsed",
    )
    ciap_queixa = st.text_input(
        "Código CIAP (opcional)",
        placeholder="Ex: A01, D12...",
        key="ciap_queixa",
    )

with st.expander("HDA – História da Doença Atual", expanded=False):
    hda = st.text_area(
        "Texto",
        placeholder="Descrição detalhada da queixa abordada na consulta...",
        key="hda",
        height=220,
        label_visibility="collapsed",
    )

# =========================
# OBJETIVO
# =========================
st.header("Objetivo")

with st.expander("Exame físico", expanded=True):
    exame_fisico = st.text_area(
        "Texto",
        placeholder="Descreva os achados do exame físico...",
        key="exame_fisico",
        height=220,
        label_visibility="collapsed",
    )

with st.expander("Resultados de exames complementares", expanded=False):
    exames_texto = st.text_area(
        "Descrição dos exames",
        placeholder="Resultados de exames laboratoriais, imagem etc...",
        key="exames_texto",
        height=180,
    )

    uploaded_files = st.file_uploader(
        "Upload de exames (PDF, imagens)",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="uploaded_files",
    )

    if uploaded_files:
        st.write(f"{len(uploaded_files)} arquivo(s) enviado(s).")

# =========================
# AVALIAÇÃO
# =========================
st.header("Avaliação")

with st.expander("Hipótese diagnóstica", expanded=True):
    hipotese_diagnostica = st.text_area(
        "Texto",
        placeholder="Hipótese(s) diagnóstica(s) da consulta...",
        key="hipotese_diagnostica",
        height=180,
        label_visibility="collapsed",
    )

with st.expander("Lista de problemas", expanded=False):
    # Mock de lista CID/CIAP ativos
    lista_problemas_ativos = [
        "Hipertensão arterial (CID I10)",
        "Diabetes mellitus tipo 2 (CID E11)",
        "Dor lombar (CIAP L03)",
        "Ansiedade (CIAP P01)",
    ]

    problemas_selecionados = st.multiselect(
        "Selecione os problemas abordados nesta consulta",
        lista_problemas_ativos,
        key="problemas_selecionados",
    )

    st.caption(
        "Aqui entra o CID/CIAP automático e a possibilidade de adicionar ou não à lista ativa do paciente."
    )

    adicionar_lista = st.checkbox(
        "Adicionar novos problemas à lista ativa do paciente",
        key="adicionar_lista",
    )

# =========================
# PLANO
# =========================
st.header("Plano")

with st.expander("Conduta", expanded=True):
    conduta = st.text_area(
        "Texto",
        placeholder="Plano terapêutico, prescrições, exames solicitados etc...",
        key="conduta",
        height=220,
        label_visibility="collapsed",
    )
    st.caption("Sugestão: depois podemos estruturar prescrição e solicitações de exames em formulários.")

with st.expander("Pendências / Lembretes", expanded=False):
    pendencias = st.text_area(
        "Texto",
        placeholder="O que precisa ser avaliado em próxima consulta; demandas não abordadas/esgotadas etc...",
        key="pendencias",
        height=180,
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
        st.experimental_rerun()
