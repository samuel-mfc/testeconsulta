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
    if "paciente" not in st.session_state:
        st.session_state.paciente = {
            "identificacao": {
                "nome": "João da Silva",
                "nascimento": "01/01/1980",
                "idade": "45",
                "sexo": "M",
                "telefone": "(11) 99999-0000",
                "endereco": "Rua Floresta, 123, SP",
                "convenio": "Particular",
                "prontuario": "PR-000123",
            },
            "diagnosticos_ativos": [
                {"cid": "I10", "descricao": "Hipertensão essencial (primária)", "desde": "2021"},
                {"cid": "E11", "descricao": "Diabetes mellitus tipo 2", "desde": "2019"},
            ],
            "medicacoes_em_uso": [
                {"nome": "Losartana", "dose": "50 mg", "posologia": "1 cp 2x/dia"},
                {"nome": "Metformina", "dose": "850 mg", "posologia": "1 cp 2x/dia"},
            ],
            "alergias": [
                {"substancia": "Dipirona", "reacao": "Urticária"},
            ],
            "medidas_recentes": {
                "pressao_arterial": "138/86 mmHg",
                "frequencia_cardiaca": "78 bpm",
                "peso": "86 kg",
                "altura": "1,72 m",
                "imc": "29,1",
                "glicemia_capilar": "142 mg/dL",
                "ultima_atualizacao": "Há 12 dias",
            },
            "habitos_risco": {
                "tabagismo": "Não",
                "etilismo": "Social",
                "atividade_fisica": "2x/semana",
                "sono": "6-7h/noite",
            },
            "historico_relevante": [
                "Internação por pneumonia (2017)",
                "Cirurgia: apendicectomia (2005)",
            ],
            "problemas": [
                # lista “ativa” fictícia — diferente dos registros
                {"cid": "M54.5", "descricao": "Dor lombar baixa", "status": "Intermitente"},
            ],
        }

def agora_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def salvar_registro(tipo: str, payload: dict):
    registro = {
        "data_hora": agora_str(),
        "tipo": tipo,
        "paciente": st.session_state.paciente["identificacao"],
        "conteudo": payload,
    }
    st.session_state.registros.append(registro)

def exportar_json():
    return json.dumps(st.session_state.registros, ensure_ascii=False, indent=2).encode("utf-8")

init_state()
pac = st.session_state.paciente
idp = pac["identificacao"]

# -----------------------------
# Sidebar — Folha de rosto / Resumo clínico
# -----------------------------
st.sidebar.markdown("## 🩺 Folha de rosto")
st.sidebar.markdown(f"### {idp['nome']}")
st.sidebar.caption(
    f"Prontuário: **{idp['prontuario']}**  •  Convênio: **{idp['convenio']}**\n\n"
    f"{idp['sexo']}, {idp['idade']} anos  •  Nasc.: {idp['nascimento']}\n\n"
    f"Tel.: {idp['telefone']}\n\n"
    f"End.: {idp['endereco']}"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Diagnósticos ativos")
for d in pac["diagnosticos_ativos"]:
    st.sidebar.write(f"• **{d['cid']}** — {d['descricao']} _(desde {d['desde']})_")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💊 Medicações em uso")
for m in pac["medicacoes_em_uso"]:
    st.sidebar.write(f"• **{m['nome']} {m['dose']}** — {m['posologia']}")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚠️ Alergias")
if pac["alergias"]:
    for a in pac["alergias"]:
        st.sidebar.write(f"• **{a['substancia']}** — {a['reacao']}")
else:
    st.sidebar.caption("Nenhuma alergia conhecida.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🩸 Medidas recentes")
mr = pac["medidas_recentes"]
st.sidebar.write(f"• **PA:** {mr['pressao_arterial']}")
st.sidebar.write(f"• **FC:** {mr['frequencia_cardiaca']}")
st.sidebar.write(f"• **Peso/Altura:** {mr['peso']} / {mr['altura']}")
st.sidebar.write(f"• **IMC:** {mr['imc']}")
st.sidebar.write(f"• **Glicemia:** {mr['glicemia_capilar']}")
st.sidebar.caption(f"Atualização: {mr['ultima_atualizacao']}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧩 Hábitos / risco")
hr = pac["habitos_risco"]
st.sidebar.write(f"• Tabagismo: **{hr['tabagismo']}**")
st.sidebar.write(f"• Etilismo: **{hr['etilismo']}**")
st.sidebar.write(f"• Atividade física: **{hr['atividade_fisica']}**")
st.sidebar.write(f"• Sono: **{hr['sono']}**")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Histórico relevante")
for item in pac["historico_relevante"]:
    st.sidebar.write(f"• {item}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 Problemas (lista ativa)")
for pr in pac["problemas"]:
    st.sidebar.write(f"• **{pr['cid']}** — {pr['descricao']} _({pr['status']})_")

st.sidebar.markdown("---")
st.sidebar.download_button(
    "Baixar registros (JSON)",
    data=exportar_json(),
    file_name="registros_consulta.json",
    mime="application/json",
)

col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    if st.button("Limpar registros"):
        st.session_state.registros = []
with col_sb2:
    if st.button("Reset paciente"):
        # volta ao fictício padrão
        for k in list(st.session_state.keys()):
            if k in ("paciente",):
                del st.session_state[k]
        init_state()
        st.rerun()

# -----------------------------
# Tela principal
# -----------------------------
st.title("Registro de Consulta Médica")

# Cabeçalho do paciente (cartão)
with st.container(border=True):
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.markdown(f"### {idp['nome']}")
        st.caption(f"Nasc.: {idp['nascimento']} • Endereço: {idp['endereco']}")
    with c2:
        st.markdown("### ")
        st.caption(f"Telefone: {idp['telefone']} • Convênio: {idp['convenio']}")
    with c3:
        st.markdown("### IDADE")
        st.metric(label="", value=idp.get("idade", "-"))

st.markdown("")

tab1, tab2, tab3 = st.tabs(["📝 Registro livre", "📋 Anamnese tradicional", "🧾 SOAP"])

# -----------------------------
# Aba 1 - Registro livre
# -----------------------------
with tab1:
    st.subheader("Registro livre")
    texto_livre = st.text_area(
        "Escreva o registro da consulta",
        height=280,
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
        st.caption("Os registros ficam na sessão e podem ser baixados em JSON pela barra lateral.")

# -----------------------------
# Aba 2 - Anamnese tradicional (SEM expander)
# -----------------------------
with tab2:
    st.subheader("Anamnese tradicional")

    # Bloco principal (similar ao layout: campos empilhados)
    with st.container(border=True):
        st.markdown("#### QUEIXA PRINCIPAL")
        qp = st.text_area(" ", key="qp", height=140, placeholder="Descreva a queixa principal...")

        st.markdown("#### HDA")
        hda = st.text_area("  ", key="hda", height=120, placeholder="História da Doença Atual...")

        st.markdown("#### HPP")
        hpp = st.text_area("   ", key="hpp", height=120, placeholder="História Patológica Pregressa...")

        col_hf, col_hs = st.columns(2)
        with col_hf:
            st.markdown("#### HF")
            hf = st.text_area("    ", key="hf", height=110, placeholder="História Familiar...")
        with col_hs:
            st.markdown("#### HS")
            hs = st.text_area("     ", key="hs", height=110, placeholder="História Social...")

        st.markdown("#### MED")
        med = st.text_area("      ", key="med", height=110, placeholder="Medicações em uso...")

        st.markdown("#### ALERGIA")
        alergia = st.text_area("       ", key="alergia", height=110, placeholder="Alergias...")

        st.markdown("#### HD")
        hd = st.text_area("        ", key="hd", height=110, placeholder="Hipótese Diagnóstica...")

        st.markdown("#### CD")
        cd = st.text_area("         ", key="cd", height=110, placeholder="Conduta...")

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
        if payload["queixa_principal"]:
            salvar_registro("anamnese_tradicional", payload)
            st.success("Anamnese salva!")
        else:
            st.warning("Preencha ao menos a **Queixa Principal** para salvar.")

# -----------------------------
# Aba 3 - SOAP
# -----------------------------
with tab3:
    st.markdown("#### Subjetivo (S)")
    s = st.text_area(" ", height=140, placeholder="Queixas, percepções do paciente, sintomas...")
    st.markdown("#### Objetivo (O)")
    o = st.text_area(" ", height=140, placeholder="Exame físico, sinais, medidas, exames...")
    st.markdown("#### Avaliação (A)")
    a = st.text_area(" ", height=140, placeholder="Raciocínio clínico, hipóteses, diagnóstico...")

    cids = [
        ("Z00.0", "Exame geral de rotina"),
        ("I10", "Hipertensão essencial (primária)"),
        ("E11", "Diabetes mellitus tipo 2"),
        ("J06.9", "IVAS aguda, não especificada"),
        ("M54.5", "Dor lombar baixa"),
        ("F41.1", "Transtorno de ansiedade generalizada"),
    ]
    cid_opcoes = [f"{cod} — {desc}" for cod, desc in cids]
    cid_escolhido = st.selectbox("Selecione um CID", options=cid_opcoes, index=0)

    inserir_problema = st.checkbox("Inserir na lista de problemas ativos?", value=False)

    st.markdown("#### Plano (P)")
    p = st.text_area(" ", height=140, placeholder="Conduta, orientações, pendências...")

    if st.button("Salvar (SOAP)", type="primary"):
        payload = {
            "subjetivo": s.strip(),
            "objetivo": o.strip(),
            "avaliacao": a.strip(),
            "plano": p.strip(),
            "cid": cid_escolhido.split(" — ")[0],
            "cid_descricao": cid_escolhido.split(" — ", 1)[1],
            "inserir_na_lista_problemas": inserir_problema,
        }

        if payload["subjetivo"] or payload["objetivo"] or payload["avaliacao"] or payload["plano"]:
            salvar_registro("soap", payload)

            if inserir_problema:
                pac["problemas"].append({
                    "cid": payload["cid"],
                    "descricao": payload["cid_descricao"],
                    "status": "Ativo",
                })

            st.success("SOAP salvo!")
        else:
            st.warning("Preencha ao menos um campo (S, O ou A) para salvar.")
