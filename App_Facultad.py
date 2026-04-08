import streamlit as st
import numpy as np
import pandas as pd

# ==========================================
# LÓGICA DE PROGRAMACIÓN (ÁLGEBRA LINEAL)
# ==========================================

def sumar_matrices(A, B):
    """Suma A + B recorriendo posición por posición."""
    if A.shape != B.shape:
        return "Error: Las dimensiones deben ser iguales para sumar."
    
    filas, columnas = A.shape
    resultado = np.zeros((filas, columnas))
    
    # Recorrido con ciclos anidados (i = filas, j = columnas)
    for i in range(filas):
        for j in range(columnas):
            resultado[i][j] = A[i][j] + B[i][j]
    return resultado

def multiplicar_matrices(A, B):
    """Multiplicación matricial usando triple ciclo (i, j, k)."""
    filas_A, cols_A = A.shape
    filas_B, cols_B = B.shape
    
    if cols_A != filas_B:
        return f"Error: No se puede multiplicar. Columnas de A ({cols_A}) != Filas de B ({filas_B})."
    
    # La matriz resultante es de (filas A x columnas B)
    resultado = np.zeros((filas_A, cols_B))
    
    # Lógica de 3 ciclos
    for i in range(filas_A):          # Recorre filas de A
        for j in range(cols_B):      # Recorre columnas de B
            suma_acumulada = 0
            for k in range(cols_A):  # k es el índice común
                suma_acumulada += A[i][k] * B[k][j]
            resultado[i][j] = suma_acumulada
    return resultado

def multiplicar_por_escalar(A, factor):
    """Multiplica cada elemento de la matriz por un número real."""
    filas, columnas = A.shape
    resultado = np.zeros((filas, columnas))
    
    for i in range(filas):
        for j in range(columnas):
            resultado[i][j] = A[i][j] * factor
    return resultado

def inversa_2x2(M):
    """Cálculo manual de la inversa para matrices de 2x2."""
    if M.shape != (2, 2):
        return "Error: Esta lógica simplificada solo aplica a matrices 2x2."
    
    # Extraer valores individuales
    a, b = M[0][0], M[0][1]
    c, d = M[1][0], M[1][1]
    
    # Calcular determinante
    determinante = (a * d) - (b * c)
    
    if determinante == 0:
        return "Error: El determinante es 0. La matriz no tiene inversa."
    
    # Aplicar fórmula de la adjunta para 2x2
    resultado = np.zeros((2, 2))
    resultado[0][0] = d / determinante
    resultado[0][1] = -b / determinante
    resultado[1][0] = -c / determinante
    resultado[1][1] = a / determinante
    return resultado

# ==========================================
# INTERFAZ DE USUARIO (STREAMLIT)
# ==========================================

st.set_page_config(page_title="Laboratorio de Matrices", layout="wide")
st.title("🧪 Laboratorio de Matrices Profecional")

# Inicializar el espacio de las 4 matrices
if 'matrices' not in st.session_state:
    st.session_state.matrices = {'A': None, 'B': None, 'C': None, 'D': None}

# --- PANEL LATERAL (CARGA Y CAPTURA) ---
with st.sidebar:
    st.header("1. Entrada de Datos")
    metodo = st.radio("Método de entrada:", ["Manual (Editor)", "Subir Archivo (.txt)"])
    target = st.selectbox("Asignar a:", ['A', 'B', 'C', 'D'])

    if metodo == "Manual (Editor)":
        f = st.number_input("Filas", 1, 10, 2)
        c = st.number_input("Columnas", 1, 10, 2)
        df_input = st.data_editor(pd.DataFrame(np.zeros((f, c))), key=f"editor_{target}")
        if st.button("Guardar en " + target):
            st.session_state.matrices[target] = df_input.to_numpy()
            st.success(f"Matriz {target} lista.")
    else:
        archivo = st.file_uploader("Sube tu archivo TXT", type="txt")
        if archivo and st.button("Procesar Archivo"):
            try:
                matriz_cargada = np.loadtxt(archivo)
                st.session_state.matrices[target] = matriz_cargada
                st.success(f"Matriz {target} cargada desde archivo.")
            except:
                st.error("Formato de archivo inválido. Usa espacios o tabs entre números.")

# --- PANEL CENTRAL (OPERACIONES) ---
st.header("2. Operaciones con Matrices")
col1, col2 = st.columns([2, 1])

with col1:
    operacion = st.selectbox("Elegir Operación:", 
                            ["Suma", "Multiplicación Matricial", "Escalar (Factor)", "Inversa (2x2)"])
    
    m_origen1 = st.selectbox("Matriz Principal:", ['A', 'B', 'C', 'D'], key="mo1")
    
    # Mostrar opciones adicionales según la operación
    m_origen2 = None
    factor = 1.0
    if operacion in ["Suma", "Multiplicación Matricial"]:
        m_origen2 = st.selectbox("Matriz Secundaria:", ['A', 'B', 'C', 'D'], key="mo2")
    elif operacion == "Escalar (Factor)":
        factor = st.number_input("Introduce el factor real:", value=1.0)
    
    m_destino = st.selectbox("Guardar resultado en:", ['A', 'B', 'C', 'D'], key="mdest")

    if st.button("🔥 Ejecutar Cálculo"):
        A = st.session_state.matrices[m_origen1]
        
        if A is None:
            st.error(f"La matriz {m_origen1} está vacía.")
        else:
            res = None
            if operacion == "Suma":
                B = st.session_state.matrices[m_origen2]
                res = sumar_matrices(A, B) if B is not None else "Error: Segunda matriz vacía."
            
            elif operacion == "Multiplicación Matricial":
                B = st.session_state.matrices[m_origen2]
                res = multiplicar_matrices(A, B) if B is not None else "Error: Segunda matriz vacía."
            
            elif operacion == "Escalar (Factor)":
                res = multiplicar_por_escalar(A, factor)
            
            elif operacion == "Inversa (2x2)":
                res = inversa_2x2(A)

            # Validar si el resultado es un mensaje de error o una matriz
            if isinstance(res, str):
                st.error(res)
            else:
                st.session_state.matrices[m_destino] = res
                st.success(f"Operación terminada. Resultado guardado en {m_destino}")

# --- PANEL INFERIOR (ESTADO ACTUAL) ---
st.divider()
st.header("3. Espacio de Trabajo (Matrices Activas)")
vista_cols = st.columns(4)

for i, letra in enumerate(['A', 'B', 'C', 'D']):
    with vista_cols[i]:
        st.subheader(f"Matriz {letra}")
        m = st.session_state.matrices[letra]
        if m is not None:
            st.dataframe(m)
            # Opción para exportar/guardar en archivo
            txt_data = pd.DataFrame(m).to_csv(index=False, header=False, sep='\t')
            st.download_button(f"📥 Bajar {letra}.txt", txt_data, f"Matriz_{letra}.txt")
        else:
            st.caption("Sin datos cargados.")
