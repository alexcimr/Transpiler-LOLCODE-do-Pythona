import streamlit as st
from streamlit_ace import st_ace
import io
from contextlib import redirect_stdout

from lexer import lexer
from parser import parser

st.set_page_config(page_title="Transpiler LOLCODE", layout="wide")
st.title("Transpiler LOLCODE do Pythona")

default_code = """HAI
I HAS A KOTY ITZ 5
I HAS A PSY ITZ 3
I HAS A RAZEM ITZ SUM OF KOTY AN PSY
VISIBLE "Zwierzeta lacznie:"
VISIBLE RAZEM
KTHXBYE"""

col1, col2 = st.columns(2)

with col1:
    st.subheader("Wejście (LOLCODE)")
    lol_code = st_ace(
        value=default_code, 
        language="text", 
        theme="tomorrow_night",
        height=300,
        show_gutter=True
    )
    transpile_btn = st.button("1. Transpiluj", type="primary")

if "python_code" not in st.session_state:
    st.session_state.python_code = ""
if "errors" not in st.session_state:
    st.session_state.errors = ""

if transpile_btn and lol_code:
    lexer.lineno = 1
    stdout_capture = io.StringIO()
    
    with redirect_stdout(stdout_capture):
        result = parser.parse(lol_code, lexer=lexer)
        
    st.session_state.errors = stdout_capture.getvalue()
    
    if result:
        st.session_state.python_code = result
    else:
        st.session_state.python_code = "# BŁĄD SKŁADNIOWY/LEKSYKALNY"

with col2:
    st.subheader("Wyjście (Python)")
    st.code(st.session_state.python_code, language="python", line_numbers=True)
    
    if st.session_state.errors:
        st.warning(f"Logi parsera:\n{st.session_state.errors}")

st.divider()
st.subheader("Terminal")
run_btn = st.button("2. Uruchom przetłumaczony kod")

if run_btn:
    if st.session_state.python_code and not st.session_state.python_code.startswith("#"):
        stdout_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture):
            try:
                exec(st.session_state.python_code, {})
            except Exception as e:
                print(f"Błąd wykonania (Runtime): {e}")
                
        output = stdout_capture.getvalue()
        
        if output:
            st.text(output)
        else:
            st.info("Kod wykonał się poprawnie, ale nic nie wypisał na ekran.")
    else:
        st.error("Brak poprawnego kodu Pythona do uruchomienia.")
