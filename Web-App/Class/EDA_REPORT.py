import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import os

class EDA_REPORT:
    def __init__(self, data):
        self.df = pd.DataFrame(data)
    
    def resumen_general(self):
        resumen = f"""
        Resumen General del Curso
        Número total de asistentes: {self.df.shape[0]}
        Promedio de edad: {self.df['edad'].mean():.2f}
        Distribución de género:
        {self.df['genero'].value_counts().to_string()}
        Nacionalidades:
        {self.df['nacionalidad'].value_counts().to_string()}
        Comunas:
        {self.df['comuna'].value_counts().to_string()}
        Barrios:
        {self.df['barrio'].value_counts().to_string()}
        """
        return resumen

    def resumen_asistencia(self):
        resumen = f"""
        Resumen de Asistencia
        Porcentaje de asistencia:
        {self.df['asistencia'].value_counts(normalize=True) * 100}
        Asistencia promedio: {self.df['asistencia_promedio'].mean():.2f}
        """
        return resumen
    
    def visualizar_datos(self):
        figures = []

        # Visualizar la distribución de edades
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(self.df['edad'], kde=True, ax=ax)
        ax.set_title('Distribución de Edades')
        ax.set_xlabel('Edad')
        ax.set_ylabel('Frecuencia')
        fig.savefig('edad.png')
        figures.append('edad.png')
        plt.close(fig)
        
        # Visualizar la distribución de género
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='genero', data=self.df, ax=ax)
        ax.set_title('Distribución de Género')
        ax.set_xlabel('Género')
        ax.set_ylabel('Frecuencia')
        fig.savefig('genero.png')
        figures.append('genero.png')
        plt.close(fig)
        
        # Visualizar la asistencia promedio
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(self.df['asistencia_promedio'], kde=True, ax=ax)
        ax.set_title('Distribución de Asistencia Promedio')
        ax.set_xlabel('Asistencia Promedio')
        ax.set_ylabel('Frecuencia')
        fig.savefig('asistencia_promedio.png')
        figures.append('asistencia_promedio.png')
        plt.close(fig)
        
        # Visualizar nacionalidades
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='nacionalidad', data=self.df, ax=ax)
        ax.set_title('Distribución de Nacionalidades')
        ax.set_xlabel('Nacionalidad')
        ax.set_ylabel('Frecuencia')
        fig.savefig('nacionalidades.png')
        figures.append('nacionalidades.png')
        plt.close(fig)
        
        return figures
    
    def generar_reporte(self):
        general = self.resumen_general()
        asistencia = self.resumen_asistencia()
        figuras = self.visualizar_datos()
        
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("Arial", size=12)
        
        # Agregar Resumen General
        pdf.multi_cell(0, 10, general)
        
        # Agregar Resumen de Asistencia
        pdf.multi_cell(0, 10, asistencia)
        
        # Agregar Gráficos
        for figura in figuras:
            pdf.add_page()
            pdf.image(figura, x=10, y=10, w=190)
        
        # Generar nombre de archivo único
        filename = "reporte_curso.pdf"
        counter = 1
        while os.path.isfile(filename):
            filename = f"reporte_curso_{counter}.pdf"
            counter += 1
        
        # Guardar PDF
        pdf.output(filename)
        print(f"Reporte generado: {filename}")

# Crear la clase con los datos proporcionados
data = {
    'asistenteid': [7, 8, 9],
    'rut': ['4679029', '81714347', '14741758'],
    'digito_v': [4, 7, 6],
    'nombre': ['Aliro  De la Fuente Lizama', 'Guillermina  Gutierrez Cid', 'Blanca  Azcue Quispe'],
    'telefono': ['995363805', '977907615', '973152191'],
    'correo': ['alidelafue@yahoo.com', 'guillerminagutierrezcid51@gmail.com', 'blanca.azcueq@gmail.com'],
    'genero': ['Masculino', 'Masculino', 'Masculino'],
    'edad': [74, 69, 65],
    'nacionalidad': ['Chilena', 'Chilena', 'Peruana'],
    'comuna': ['Santiago', 'Santiago', 'Santiago'],
    'barrio': ['Santa Isabel (7)', 'República (9)', 'Yungay (3)'],
    'cursoid': [10, 10, 10],
    'asistencia': ['Presente', 'Presente', 'Ausente'],
    'asistencia_promedio': [6.666667, 6.666667, 6.666667]
}

# Instanciar la clase y generar el reporte
#curso_eda = EDA_REPORT(data)
#curso_eda.generar_reporte()
