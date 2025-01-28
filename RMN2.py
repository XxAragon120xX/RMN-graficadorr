import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class GraficadorRMN:
    
    def __init__(self):
        # Crear carpeta para guardar los resultados
        self.carpeta_resultados = Path('resultados_rmn')
        self.carpeta_resultados.mkdir(exist_ok=True)
        
        # Configuración visual del gráfico
        self.configurar_estilo()
    
    def configurar_estilo(self):
        plt.style.use('default')
        plt.rcParams.update({
            'figure.figsize': (12, 6),    # Tamaño adecuado para ver detalles
            'font.size': 10,              # Tamaño de letra legible
            'lines.linewidth': 1.0,       # Grosor de línea balanceado
            'font.family': 'sans-serif'   # Tipo de letra moderna
        })
    
    def generar_pico(self, posiciones_x, posicion_pico, intensidad):
        
        anchura_pico = 10000.0  # Factor que determina qué tan agudo es el pico
        return intensidad * np.exp(-anchura_pico * (posiciones_x - posicion_pico) ** 2)
    
    def crear_espectro(self):
        
        try:
            # Cargar datos experimentales
            datos = pd.read_csv("ethyl acetate_NMR.csv")
            
            # Preparar el gráfico
            figura, grafico = plt.subplots()
            
            # Generar puntos para el eje x (escala de ppm)
            escala_ppm = np.linspace(0, 12, num=3000)
            intensidad_total = np.zeros_like(escala_ppm)
            
            # Crear el espectro sumando todos los picos
            for _, pico in datos.iterrows():
                intensidad_total += self.generar_pico(
                    escala_ppm,
                    pico['ppm'],
                    pico['Int.']
                )
            
            # Dibujar el espectro
            grafico.plot(escala_ppm, intensidad_total, color='navy', label='Señal RMN')
            
            # Configurar aspecto del gráfico
            grafico.set_xlabel('Desplazamiento Químico (ppm)')
            grafico.set_ylabel('Intensidad Relativa')
            grafico.invert_xaxis()  # Convención en RMN: ppm decrece de izquierda a derecha
            grafico.grid(True, linestyle='--', alpha=0.7)
            
            # Añadir título con información de la muestra
            plt.title('Espectro RMN-H¹: Acetato de Etilo\n'
                     'Muestra en CDCl₃, 400 MHz', pad=20)
            
            # Guardar el espectro como imagen
            nombre_archivo = self.carpeta_resultados / 'espectro_acetato_etilo.png'
            plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
            print(f"Espectro guardado como: {nombre_archivo}")
            
            # Mostrar el espectro
            plt.show()
            
        except FileNotFoundError:
            print("Error: No se encontró el archivo de datos.")
            print("Asegúrate de tener el archivo 'ethyl acetate_NMR.csv' en la carpeta actual.")
        except Exception as error:
            print(f"Error al generar el espectro: {str(error)}")

if __name__ == "__main__":
    # Crear y usar el graficador
    graficador = GraficadorRMN()
    graficador.crear_espectro()