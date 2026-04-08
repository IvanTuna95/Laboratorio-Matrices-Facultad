import streamlit as st
import numpy as np
import pandas as pd

# ==========================================
# LÓGICA DE PROGRAMACIÓN EXPERTA
# ==========================================

def sumar_matrices(A, B):
    if A.shape != B.shape:
        return "Error: Dimensiones incompatibles para sumar."
    filas, columnas = A.shape
    resultado = np.zeros((filas, columnas))
    for i in range(filas):
        for j in range(columnas):
            resultado[i][j] = A[i][j] + B[i][j]
    return resultado

def multiplicar_matrices(A, B):
    filas_A, cols_A = A.shape
    filas_B, cols_B = B.shape
    if cols_A != filas_B:
        return "Error: Columnas de A deben coincidir con Filas de B."
    resultado = np.zeros((filas_A, cols_B))
    for i in range(filas_A):
        for j in range(cols_B):
            for k in range(cols_A):
                resultado[i][j] += A[i][k] * B[k][j]
    return resultado

def inversa_gauss_jordan(M):
    """Cálculo de inversa para matrices de hasta 5x5 mediante Gauss-Jordan."""
    if M.shape[0] != M.shape[1]:
        return "Error: La matriz debe ser cuadrada."
    
    n = M.shape[0]
    # Creamos una copia para no modificar la original y la matriz identidad
    A = M.copy().astype(float)
    inv = np.identity(n)

    # Proceso de eliminación
    for i in range(n):
        # 1. Pivoteo: buscar el valor máximo en la columna para estabilidad
        pivote = A[i][i]
        if abs(pivote) < 1e-10:
            return "Error: La matriz es singular (no tiene inversa)."

        # 2. Hacer que el pivote sea 1 dividiendo toda la fila
        A[i] = A[i] / pivote
        inv[i] = inv[i] / pivote

        # 3. Eliminar los otros elementos de la columna
        for j in range(n):
            if i != j:
                factor = A[j][i]
                A[j] -= factor * A[i]
                inv[j] -= factor * inv[i]
                
    return inv

# ==========================================
# INTERFAZ DE USUARIO (STREAMLIT)
# ==========================================

st.set_page_config(page_title="Laboratorio de Matrices Pro", layout="wide")
st.title("🧪 Laboratorio de Matrices (Hasta 5x5)")

if 'matrices' not in st.session_state:
    st.session_state.matrices = {'A': None, 'B': None, 'C': None, 'D': None}

with st.sidebar:
    st.header("1. Entrada de Datos")
    metodo = st.radio("Método:", ["Manual", "Archivo .txt"])
    target = st.selectbox("Asignar a:", ['A', 'B', 'C', 'D'])

    if metodo == "Manual":
        f = st.number_input("Filas", 1, 5, 2)
        c = st.number_input("Columnas", 1, 5, 2)
        df_input = st.data_editor(pd.DataFrame(np.zeros((f, c))), key=f"ed_{target}")
        if st.button(f"Guardar en {target}"):
            st.session_state.matrices[target] = df_input.to_numpy()
            st.success("Guardado.")
    else:
        archivo = st.file_uploader("Sube TXT", type="txt")
        if archivo and st.button("Cargar"):
            try:
                st.session_state.matrices[target] = np.loadtxt(archivo)
                st.success("Cargado.")
            except:
                st.error("Archivo inválido.")

# --- OPERACIONES ---
st.header("2. Operaciones")
col1, col2 = st.columns([2, 1])

with col1:
    op = st.selectbox("Operación:", ["Suma", "Multiplicación", "Escalar", "Inversa (Gauss-Jordan)"])
    m1_name = st.selectbox("Matriz Principal:", ['A', 'B', 'C', 'D'], key="m1")
    
    m2_name = None
    factor = 1.0
    if op in ["Suma", "Multiplicación"]:
        m2_name = st.selectbox("Matriz Secundaria:", ['A', 'B', 'C', 'D'], key="m2")
    elif op == "Escalar":
        factor = st.number_input("Factor:", value=1.0)
    
    dest = st.selectbox("Destino:", ['A', 'B', 'C', 'D'], key="dest")

    if st.button("Calcular"):
        A = st.session_state.matrices[m1_name]
        if A is None:
            st.error("Matriz principal vacía.")
        else:
            if op == "Suma":
                B = st.session_state.matrices[m2_name]
                res = sumar_matrices(A, B) if B is not None else "Matriz B vacía."
            elif op == "Multiplicación":
                B = st.session_state.matrices[m2_name]
                res = multiplicar_matrices(A, B) if B is not None else "Matriz B vacía."
            elif op == "Escalar":
                res = A * factor
            elif op == "Inversa (Gauss-Jordan)":
                res = inversa_gauss_jordan(A)

            if isinstance(res, str):
                st.error(res)
            else:
                st.session_state.matrices[dest] = res
                st.success(f"Resultado en {dest}")

# --- VISUALIZACIÓN ---
st.divider()
cols = st.columns(4)
for i, L in enumerate(['A', 'B', 'C', 'D']):
    with cols[i]:
        st.subheader(f"Matriz {L}")
        if st.session_state.matrices[L] is not None:
            st.dataframe(st.session_state.matrices[L])
            csv = pd.DataFrame(st.session_state.matrices[L]).to_csv(index=False, header=False, sep='\t')
            st.download_button(f"Descargar {L}", csv, f"{L}.txt")
        else:
            st.caption("Vacía")
            
