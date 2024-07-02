import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import os
import base64
from io import BytesIO

class EDA_REPORT:
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        matplotlib.use('Agg')  # Usar un backend que no requiera una GUI
    
    def resumen_general(self):
        resumen = f"""
        <h2>Resumen General del Curso</h2>
        <p>Número total de asistentes: {self.df.shape[0]}</p>
        <p>Promedio de edad: {self.df['edad'].mean():.2f}</p>
        <p>Distribución de género:</p>
        <pre>{self.df['genero'].value_counts().to_string()}</pre>
        <p>Nacionalidades:</p>
        <pre>{self.df['nacionalidad'].value_counts().to_string()}</pre>
        <p>Comunas:</p>
        <pre>{self.df['comuna'].value_counts().to_string()}</pre>
        <p>Barrios:</p>
        <pre>{self.df['barrio'].value_counts().to_string()}</pre>
        """
        return resumen

    def resumen_asistencia(self):
        resumen = f"""
        <h2>Resumen de Asistencia</h2>
        <p>Porcentaje de asistencia:</p>
        <pre>{self.df['clases_asistidas'].value_counts(normalize=True) * 100}</pre>
        <p>Asistencia promedio: {self.df['asistencia_promedio'].mean():.2f}</p>
        """
        return resumen
    
    def visualizar_datos(self):
        figures = []

        # Función para convertir una figura a base64
        def fig_to_base64(fig):
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()
            return img_str

        # Visualizar la distribución de edades
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(self.df['edad'], kde=True, ax=ax)
        ax.set_title('Distribución de Edades')
        ax.set_xlabel('Edad')
        ax.set_ylabel('Frecuencia')
        img_str = fig_to_base64(fig)
        figures.append(img_str)
        plt.close(fig)
        
        # Visualizar la distribución de género
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='genero', data=self.df, ax=ax)
        ax.set_title('Distribución de Género')
        ax.set_xlabel('Género')
        ax.set_ylabel('Frecuencia')
        img_str = fig_to_base64(fig)
        figures.append(img_str)
        plt.close(fig)
        
        # Visualizar nacionalidades
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='nacionalidad', data=self.df, ax=ax)
        ax.set_title('Distribución de Nacionalidades')
        ax.set_xlabel('Nacionalidad')
        ax.set_ylabel('Frecuencia')
        img_str = fig_to_base64(fig)
        figures.append(img_str)
        plt.close(fig)
        
        return figures
    
    def generar_reporte(self):
        general = self.resumen_general()
        asistencia = self.resumen_asistencia()
        figuras = self.visualizar_datos()

        # Estilos CSS
        estilos = """
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { text-align: center; }
            h2 { color: #2F4F4F; }
            pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; }
            img { max-width: 100%; margin: 20px 0; }
        </style>
        """
        
        # Estructura del HTML
        html = f"""
        <html>
        <head>
            <title>Reporte del Curso</title>
            {estilos}
        </head>
        <body>
            <h1>Reporte del Curso</h1>
            {general}
            {asistencia}
        """
        for figura in figuras:
            html += f'<img src="data:image/png;base64,{figura}" alt="Figura">'
        
        html += """
        </body>
        </html>
        """
        
        # Guardar HTML temporalmente
        filename = "reporte_curso.html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)
        
        return filename