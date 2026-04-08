import streamlit as st
import numpy as np
import pandas as pd

# 1. Configurar el "Espacio" para las 4 matrices
if 'matrices' not in st.session_state:
    st.session_state.matrices = {'A': None, 'B': None, 'C': None, 'D': None}

st.set_page_config(page_title="Laboratorio de Matrices", layout="wide")
st.title("🧪 Laboratorio de Matrices - Facultad")

# --- BARRA LATERAL: CAPTURA Y CARGA ---
with st.sidebar:
    st.header("Entrada de Datos")
    opcion_entrada = st.radio("Método:", ["Manual", "Subir Archivo .txt"])
    target = st.selectbox("Seleccionar Matriz Destino:", ['A', 'B', 'C', 'D'])

    if opcion_entrada == "Manual":
        f = st.number_input("Filas", 1, 10, 2)
        c = st.number_input("Columnas", 1, 10, 2)
        # Editor tipo Excel
        df_editor = st.data_editor(pd.DataFrame(np.zeros((f, c))), key=f"ed_{target}")
        if st.button("Guardar Manual"):
            st.session_state.matrices[target] = df_editor.to_numpy()
            st.success(f"Matriz {target} guardada.")

    else:
        archivo = st.file_uploader("Subir TXT", type="txt")
        if archivo and st.button("Cargar Archivo"):
            try:
                data = np.loadtxt(archivo)
                st.session_state.matrices[target] = data
                st.success(f"Matriz {target} cargada.")
            except:
                st.error("Formato de archivo inválido.")

# --- CUERPO PRINCIPAL: OPERACIONES ---
st.header("Operaciones")
col_op, col_res = st.columns([2, 1])

with col_op:
    tipo = st.selectbox("Función:", ["Sumar", "Multiplicar Matrices", "Factor Escalar", "Inversa"])

    m1 = st.selectbox("Matriz 1 (o base):", ['A', 'B', 'C', 'D'], key="m1")
    m2 = st.selectbox("Matriz 2:", ['A', 'B', 'C', 'D'], key="m2") if tipo in ["Sumar",
                                                                               "Multiplicar Matrices"] else None
    escalar = st.number_input("Factor:", value=1.0) if tipo == "Factor Escalar" else None
    destino = st.selectbox("Guardar Resultado en:", ['A', 'B', 'C', 'D'], key="dest")

    if st.button("Ejecutar Operación"):
        mat1 = st.session_state.matrices[m1]
        try:
            if tipo == "Sumar":
                mat2 = st.session_state.matrices[m2]
                st.session_state.matrices[destino] = mat1 + mat2
            elif tipo == "Multiplicar Matrices":
                mat2 = st.session_state.matrices[m2]
                st.session_state.matrices[destino] = np.matmul(mat1, mat2)
            elif tipo == "Factor Escalar":
                st.session_state.matrices[destino] = mat1 * escalar
            elif tipo == "Inversa":
                st.session_state.matrices[destino] = np.linalg.inv(mat1)
            st.balloons()  # Animación de éxito
        except Exception as e:
            st.error(f"Error: {e}")

# --- VISUALIZACIÓN DE LAS 4 MATRICES ---
st.divider()
st.header("Visualización del Espacio")
cols = st.columns(4)
for i, letra in enumerate(['A', 'B', 'C', 'D']):
    with cols[i]:
        st.subheader(f"Matriz {letra}")
        m = st.session_state.matrices[letra]
        if m is not None:
            st.write(m)
            # Botón para descargar/guardar
            txt = pd.DataFrame(m).to_csv(index=False, header=False, sep='\t')
            st.download_button(f"Descargar {letra}", txt, f"Matriz_{letra}.txt")
        else:
            st.info("Vacía")