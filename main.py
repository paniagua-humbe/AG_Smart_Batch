import tkinter as tk
from tkinter import messagebox
import numpy as np
from ag_core import ejecutar_algoritmo_genetico
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from tkinter import filedialog
import random

def parse_matrix(text):
    try:
        lines = [line for line in text.strip().split('\n') if line.strip()]
        matrix = [list(map(float, line.strip().split())) for line in lines]
        arr = np.array(matrix)
        n, m = arr.shape
        if n != m:
            raise ValueError
        return arr
    except:
        raise ValueError('Formato de matriz inválido. Debe ser una matriz cuadrada con números decimales separados por espacios.')

def iniciar_ag():
    try:
        elevacion = parse_matrix(text_elevacion.get("1.0", tk.END))
        n = elevacion.shape[0]
        num_verdes = int(entry_verdes.get())
        num_drenajes = int(entry_drenajes.get())
        num_tanques = int(entry_tanques.get())
        
        # Inicialmente generamos posiciones aleatorias para tanques
        disponibles = [(i, j) for i in range(n) for j in range(n)]
        random.shuffle(disponibles)
        posiciones_tanques = disponibles[:num_tanques]
        
        # Para drenajes, generamos posiciones temporales
        posiciones_drenajes_temp = disponibles[num_tanques:num_tanques+num_drenajes]
        
        resultado = ejecutar_algoritmo_genetico(
            n,
            num_verdes,
            posiciones_drenajes_temp,
            posiciones_tanques,
            elevacion  # Ahora pasamos la matriz de elevación
        )
        
        fig, ax = plt.subplots(figsize=(max(8, n*0.8), max(8, n*0.8)))
        colores = {
            1: '#b3e0ff', # lote habitacional
            2: '#1e88e5', # tanque de agua
            3: '#388e3c', # área verde
            4: '#bdbdbd', # calle
            5: '#e53935'  # drenaje
        }
        
        for i in range(n):
            for j in range(n):
                valor = resultado[i][j]
                if valor == 4:  # Calle
                    rect = plt.Rectangle([j, i], 1, 1, facecolor='#bdbdbd', edgecolor='black', linewidth=0.7)
                    ax.add_patch(rect)
                    
                    es_horizontal = False
                    es_vertical = False
                    
                    # Verificar si hay calle a la izquierda o derecha
                    if j > 0 and resultado[i][j-1] == 4 or j < n-1 and resultado[i][j+1] == 4:
                        es_horizontal = True
                    
                    # Verificar si hay calle arriba o abajo
                    if i > 0 and resultado[i-1][j] == 4 or i < n-1 and resultado[i+1][j] == 4:
                        es_vertical = True
                    
                    # Dibujar líneas según la orientación
                    if es_horizontal:
                        ax.plot([j+0.1, j+0.9], [i+0.5, i+0.5], color='white', linestyle=(0, (5, 5)), linewidth=2, zorder=10)
                    if es_vertical:
                        ax.plot([j+0.5, j+0.5], [i+0.1, i+0.9], color='white', linestyle=(0, (5, 5)), linewidth=2, zorder=10)
                else:
                    color = colores.get(valor, 'white')
                    rect = plt.Rectangle([j, i], 1, 1, facecolor=color, edgecolor='black', linewidth=0.7)
                    ax.add_patch(rect)
        
        ax.set_xlim(0, n)
        ax.set_ylim(0, n)
        ax.set_xticks(np.arange(0, n+1, 1))
        ax.set_yticks(np.arange(0, n+1, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        ax.grid(True, which='both', color='black', linewidth=0.7)
        
        legend_elements = [
            Patch(facecolor='#b3e0ff', edgecolor='k', label='Lote habitacional'),
            Patch(facecolor='#388e3c', edgecolor='k', label='Área verde'),
            Patch(facecolor='#bdbdbd', edgecolor='k', label='Calle'),
            Patch(facecolor='#e53935', edgecolor='k', label='Registro de drenaje'),
            Patch(facecolor='#1e88e5', edgecolor='k', label='Tanque de agua')
        ]
        
        ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=10)
        plt.title('Plano Urbanístico Generado')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror('Error', str(e))

root = tk.Tk()
root.title("SmartBatch - Algoritmo Genético")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_elevacion = tk.Label(frame, text="Matriz de elevación (n x n):")
label_elevacion.grid(row=1, column=0, sticky="ne")
text_elevacion = tk.Text(frame, width=30, height=10)
text_elevacion.grid(row=1, column=1)

label_verdes = tk.Label(frame, text="Número de áreas verdes:")
label_verdes.grid(row=2, column=0, sticky="e")
entry_verdes = tk.Entry(frame)
entry_verdes.grid(row=2, column=1)
entry_verdes.insert(0, "2")

label_drenajes = tk.Label(frame, text="Número de registros de drenaje:")
label_drenajes.grid(row=3, column=0, sticky="e")
entry_drenajes = tk.Entry(frame)
entry_drenajes.grid(row=3, column=1)
entry_drenajes.insert(0, "2")

label_tanques = tk.Label(frame, text="Número de tanques de agua:")
label_tanques.grid(row=4, column=0, sticky="e")
entry_tanques = tk.Entry(frame)
entry_tanques.grid(row=4, column=1)
entry_tanques.insert(0, "2")

def cargar_archivo_elevacion():
    archivo = filedialog.askopenfilename(filetypes=[('Archivos de texto', '*.txt *.csv')])
    if archivo:
        try:
            with open(archivo, 'r') as f:
                contenido = f.read()
            text_elevacion.delete('1.0', tk.END)
            text_elevacion.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo leer el archivo: {e}')

btn_cargar_archivo = tk.Button(frame, text="Cargar archivo de elevación", command=cargar_archivo_elevacion)
btn_cargar_archivo.grid(row=0, column=0, columnspan=2, pady=5)
btn_iniciar = tk.Button(frame, text="Iniciar Algoritmo Genético", command=iniciar_ag)
btn_iniciar.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
import matplotlib.pyplot as plt
import numpy as np

def mostrar_plano(matriz):
    fig, ax = plt.subplots(figsize=(8,8))
    cmap = plt.get_cmap('tab20c')
    ax.imshow(matriz, cmap=cmap)
    ax.set_xticks(np.arange(-0.5, matriz.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, matriz.shape[0], 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=3)  # Línea más gruesa
    ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    plt.show()
