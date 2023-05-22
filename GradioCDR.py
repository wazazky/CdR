import pandas as pd
import gradio as gr

def encontrar_resultados_mayor_seis(df):
    resultados = []

    # Iterar sobre las filas del DataFrame
    for index, row in df.iterrows():
        # Obtener las respuestas de la persona actual
        respuestas_persona_actual = row[2:]  # Ignorar las primeras dos columnas (marca temporal y dirección de correo electrónico)

        # Comparar las respuestas de la persona actual con las demás personas
        for i in range(index + 1, len(df)):
            respuestas_otra_persona = df.iloc[i, 2:]  # Ignorar las primeras dos columnas (marca temporal y dirección de correo electrónico)

            # Sumar las respuestas de ambas personas
            suma_respuestas = respuestas_persona_actual + respuestas_otra_persona

            # Verificar si la suma es mayor a 6
            if suma_respuestas.sum() > 6:
                # Obtener los correos electrónicos de ambas personas
                correo_persona_actual = df.iloc[index, 1]
                correo_otra_persona = df.iloc[i, 1]

                # Obtener las columnas donde se obtuvo el resultado mayor a 6
                columnas = suma_respuestas[suma_respuestas > 6].index.tolist()

                # Agregar los resultados a la lista
                resultados.append({
                    'correo_persona_actual': correo_persona_actual,
                    'correo_otra_persona': correo_otra_persona,
                    'columnas': columnas
                })

    return resultados

def interfaz_gradio(file):
    # Leer el archivo CSV con las respuestas
    df = pd.read_csv(file.name)

    resultados = encontrar_resultados_mayor_seis(df)

    if len(resultados) == 0:
        return "No se encontraron resultados mayores a 6."

    output_text = ""
    for resultado in resultados:
        output_text += f"Relacion encontrada entre {resultado['correo_persona_actual']} y {resultado['correo_otra_persona']}\n"
        output_text += f"Columnas: {', '.join(resultado['columnas'])}\n"
        output_text += "---\n"

    # Guardar los resultados en un archivo de texto
    with open('resultados.txt', 'w') as f:
        f.write(output_text)

    return output_text.strip()

iface = gr.Interface(fn=interfaz_gradio, inputs="file", outputs="text")
iface.launch()
