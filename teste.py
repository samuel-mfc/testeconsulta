import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Vitalis - Registro de Consulta", layout="wide")

# -----------------------------
# Helpers / Estado
# -----------------------------
def init_state():
    if "registros" not in st.session_state:
        st.session_state.registros = []
    if "problemas" not in st.session_state:
        st.session_state.problemas = []  # lista de dicts: {"cid": "...", "descricao": "...", "data": "..."}
    if "paciente" not in st.session_state:
        st.session_state.paciente = {
            "nome": "João da Silva",
            "nascimento": "01/01/1980",
            "telefone": "(11) 99999-0000",
            "endereco": "Rua Floresta, 123, SP",
            "idade": "45",  # opcional
        }

def agora_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def salvar_registro(tipo: str, payload: dict):
    registro = {
        "data_hora": agora_str(),
        "tipo": tipo,
        "paciente": st.session_state.paciente,
        "conteudo": payload,
    }
    st.session_state.registros.append(registro)

def exportar_json():
    return json.dumps(st.session_state.registros, ensure_ascii=False, indent=2).encode("utf-8")

init_state()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("VITALIS")
menu = st.sidebar.radio("Menu", ["Registro de Consulta", "Pacientes", "Agenda"], index=0)

st.sidebar.markdown("---")
st.sidebar.subheader("Paciente")
p = st.session_state.paciente
st.sidebar.write(f"**{p['nome']}**")
st.sidebar.caption(
    f"Nasc.: {p['nascimento']}  |  Tel.: {p['telefone']}\n\nEnd.: {p['endereco']}"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Lista de Problemas")
if st.session_state.problemas:
    for i, prob in enumerate(st.session_state.problemas, start=1):
        st.sidebar.write(f"{i}. **{prob['cid']}** — {prob.get('descricao','')}")
        st.sidebar.caption(prob.get("data_hora", ""))
else:
    st.sidebar.caption("Nenhum problema registrado ainda.")

col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    if st.button("Limpar problemas"):
        st.session_state.problemas = []
with col_sb2:
    if st.button("Limpar registros"):
        st.session_state.registros = []

st.sidebar.markdown("---")
st.sidebar.download_button(
    "Baixar registros (JSON)",
    data=exportar_json(),
    file_name="registros_consulta.json",
    mime="application/json",
)

# -----------------------------
# Tela principal
# -----------------------------
st.title("Registro de Consulta Médica")

if menu != "Registro de Consulta":
    st.info("Esta versão simples foca no **Registro de Consulta**. Podemos evoluir Pacientes/Agenda depois.")
    st.stop()

# Cabeçalho estilo “cartão do paciente”
with st.container(border=True):
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.markdown(f"### {p['nome']}")
        st.caption(f"Data de nascimento: {p['nascimento']} • Endereço: {p['endereco']}")
    with c2:
        st.markdown("### ")
        st.caption(f"Telefone: {p['telefone']}")
    with c3:
        st.markdown("### IDADE")
        st.metric(label="", value=p.get("idade", "-"))

st.markdown("")

tab1, tab2, tab3 = st.tabs(["📝 Registro livre", "📋 Anamnese tradicional", "🧾 SOAP"])

# -----------------------------
# Aba 1 - Registro livre
# -----------------------------
with tab1:
    st.subheader("Registro livre")
    texto_livre = st.text_area(
        "Escreva o registro da consulta",
        height=260,
        placeholder="Digite aqui...",
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Salvar (Livre)", type="primary", use_container_width=True):
            if texto_livre.strip():
                salvar_registro("registro_livre", {"texto": texto_livre.strip()})
                st.success("Registro livre salvo!")
            else:
                st.warning("Escreva algo antes de salvar.")
    with col2:
        st.caption("Dica: você pode baixar tudo em JSON pela barra lateral.")

# -----------------------------
# Aba 2 - Anamnese tradicional (igual ao layout da imagem)
# -----------------------------
with tab2:
    st.subheader("Anamnese tradicional")

    with st.expander("QUEIXA PRINCIPAL", expanded=True):
        qp = st.text_area(" ", key="qp", height=140, placeholder="Descreva a queixa principal...")

    with st.expander("HDA", expanded=False):
        hda = st.text_area(" ", key="hda", height=120, placeholder="História da Doença Atual...")

    with st.expander("HPP", expanded=False):
        hpp = st.text_area(" ", key="hpp", height=120, placeholder="História Patológica Pregressa...")

    col_hf, col_hs = st.columns(2)
    with col_hf:
        with st.expander("HF", expanded=False):
            hf = st.text_area(" ", key="hf", height=110, placeholder="História Familiar...")
    with col_hs:
        with st.expander("HS", expanded=False):
            hs = st.text_area(" ", key="hs", height=110, placeholder="História Social...")

    with st.expander("MED", expanded=False):
        med = st.text_area(" ", key="med", height=110, placeholder="Medicações em uso...")

    with st.expander("ALERGIA", expanded=False):
        alergia = st.text_area(" ", key="alergia", height=110, placeholder="Alergias...")

    with st.expander("HD:", expanded=False):
        hd = st.text_area(" ", key="hd", height=110, placeholder="Hipótese Diagnóstica...")

    with st.expander("CD:", expanded=False):
        cd = st.text_area(" ", key="cd", height=110, placeholder="Conduta...")

    if st.button("Salvar (Anamnese)", type="primary"):
        payload = {
            "queixa_principal": st.session_state.get("qp", "").strip(),
            "hda": st.session_state.get("hda", "").strip(),
            "hpp": st.session_state.get("hpp", "").strip(),
            "hf": st.session_state.get("hf", "").strip(),
            "hs": st.session_state.get("hs", "").strip(),
            "med": st.session_state.get("med", "").strip(),
            "alergia": st.session_state.get("alergia", "").strip(),
            "hd": st.session_state.get("hd", "").strip(),
            "cd": st.session_state.get("cd", "").strip(),
        }
        # exige ao menos queixa principal para salvar
        if payload["queixa_principal"]:
            salvar_registro("anamnese_tradicional", payload)
            st.success("Anamnese salva!")
        else:
            st.warning("Preencha ao menos a **Queixa Principal** para salvar.")

# -----------------------------
# Aba 3 - SOAP
# -----------------------------
with tab3:
    st.subheader("SOAP")

    s = st.text_area("Subjetivo (S)", height=140, placeholder="Queixas, percepções do paciente, sintomas...")
    o = st.text_area("Objetivo (O)", height=140, placeholder="Exame físico, sinais, medidas, exames...")
    a = st.text_area("Avaliação (A)", height=140, placeholder="Raciocínio clínico, hipóteses, diagnóstico...")

    st.markdown("#### CID na Avaliação")
    # Lista simples (pode ser trocada por base completa depois)
    cids = [
        ("Z00.0", "Exame geral de rotina"),
        ("I10", "Hipertensão essencial (primária)"),
        ("E11", "Diabetes mellitus tipo 2"),
        ("J06.9", "Infecção aguda das vias aéreas superiores, não especificada"),
        ("M54.5", "Dor lombar baixa"),
        ("F41.1", "Transtorno de ansiedade generalizada"),
    ]
    cid_opcoes = [f"{cod} — {desc}" for cod, desc in cids]
    cid_escolhido = st.selectbox("Selecione um CID", options=cid_opcoes, index=0)
    inserir_problema = st.checkbox("Inserir na lista de problemas", value=False)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Salvar (SOAP)", type="primary", use_container_width=True):
            payload = {
                "subjetivo": s.strip(),
                "objetivo": o.strip(),
                "avaliacao": a.strip(),
                "cid": cid_escolhido.split(" — ")[0],
                "cid_descricao": cid_escolhido.split(" — ", 1)[1],
                "inserir_na_lista_problemas": inserir_problema,
            }

            if payload["subjetivo"] or payload["objetivo"] or payload["avaliacao"]:
                salvar_registro("soap", payload)

                if inserir_problema:
                    st.session_state.problemas.append({
                        "cid": payload["cid"],
                        "descricao": payload["cid_descricao"],
                        "data_hora": agora_str(),
                    })

                st.success("SOAP salvo!")
            else:
                st.warning("Preencha ao menos um campo (S, O ou A) para salvar.")
    with col2:
        st.caption("O CID selecionado e o flag de problema ficam registrados no JSON.")

# -----------------------------
# Preview rápido dos últimos registros
# -----------------------------
st.markdown("---")
with st.expander("Ver últimos registros salvos", expanded=False):
    if st.session_state.registros:
        st.json(st.session_state.registros[-3:])  # mostra os 3 últimos
    else:
        st.caption("Nenhum registro salvo ainda.")
