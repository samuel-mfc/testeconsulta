import streamlit as st

st.set_page_config(
    page_title="Ficha de Registro de Consulta Médica",
    layout="wide"
)

st.title("🩺 Ficha de Registro de Consulta Médica")

# =========================
# SUBJETIVO
# =========================
st.header("📌 Subjetivo")

queixa_principal = st.text_area(
    "Queixa principal",
    placeholder="Motivo principal da consulta..."
)

ciap_queixa = st.text_input(
    "Código CIAP (opcional)",
    placeholder="Ex: A01, D12..."
)

hda = st.text_area(
    "HDA – História da Doença Atual",
    placeholder="Descrição detalhada da queixa abordada na consulta..."
)

# =========================
# OBJETIVO
# =========================
st.header("🔍 Objetivo")

exame_fisico = st.text_area(
    "Exame físico",
    placeholder="Descreva os achados do exame físico..."
)

st.subheader("Resultados de exames complementares")

exames_texto = st.text_area(
    "Descrição dos exames",
    placeholder="Resultados de exames laboratoriais, imagem etc..."
)

uploaded_files = st.file_uploader(
    "Upload de exames (PDF, imagens)",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} arquivo(s) enviado(s)")

# =========================
# AVALIAÇÃO
# =========================
st.header("🧠 Avaliação")

hipotese_diagnostica = st.text_area(
    "Hipótese diagnóstica",
    placeholder="Hipótese(s) diagnóstica(s) da consulta..."
)

st.subheader("Lista de problemas")

# Mock de lista CID/CIAP ativos
lista_problemas_ativos = [
    "Hipertensão arterial (CID I10)",
    "Diabetes mellitus tipo 2 (CID E11)",
    "Dor lombar (CIAP L03)",
    "Ansiedade (CIAP P01)"
]

problemas_selecionados = st.multiselect(
    "Selecione os problemas abordados nesta consulta",
    lista_problemas_ativos
)

adicionar_lista = st.checkbox(
    "Adicionar novos problemas à lista ativa do paciente"
)

# =========================
# PLANO
# =========================
st.header("📝 Plano")

conduta = st.text_area(
    "Conduta",
    placeholder="Descrever plano terapêutico, prescrições, exames solicitados..."
)

pendencias = st.text_area(
    "Pendências / Lembretes",
    placeholder="O que precisa ser avaliado em próxima consulta ou ficou pendente..."
)

# =========================
# AÇÕES
# =========================
st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Salvar consulta"):
        st.success("Consulta registrada (simulação).")

with col2:
    if st.button("🧹 Limpar formulário"):
        st.experimental_rerun()
