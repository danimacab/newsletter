import argparse
import pandas as pd
from bs4 import BeautifulSoup

def main(csv_file, email_title, output_name):
    # Leer el archivo CSV
    df = pd.read_csv(csv_file, sep=";")
    print(df)



    # Cargar el documento HTML plantilla
    with open('mail-plantilla/index.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Modificar el contenido del elemento <h2> con id "titulo"
    titulo_element = soup.find(id='titulo')
    if titulo_element:
        h1 = soup.new_tag('h1', style='font-size:40px;margin:0;font-family:Arial,sans-serif; color: #000000 !important;')
        h1.string = email_title
        titulo_element.append(h1)
    else:
        print("No se encontró el elemento <h2> con id 'titulo' en la plantilla HTML.")

    
    # Encontrar la tabla específica por id
    table = soup.find('table', id='temas')

    # Asegurarse de que se encontró la tabla
    if table:
        # Iterar sobre el DataFrame y crear los elementos <td> con estilos
        print(df.iterrows())
        for index, row in df.iterrows():
            tr = soup.new_tag('tr')            
            td = soup.new_tag('td', style='padding:0 0 36px 0;color:#000000 !important;')

            htype = "h1" if str(row['Tipo']) == 'Principal' else 'h2' 
            hsize = "24" if str(row['Tipo']) == 'Principal' else '22' 
            
            hx = soup.new_tag(htype, style=f'font-size:{hsize}px;margin:10px 10px 20px 10px;font-family:Arial,sans-serif;color:#000000 !important;')
            hx.string = row['Titulo']
            td.append(hx)
            
            '''p = soup.new_tag('p', style='margin:12px;font-size:16px;line-height:24px;font-family:Arial,sans-serif;')
            p.string = row['Contenido']
            td.append(p)'''
            if pd.notna(row['Contenido']):
                # Reemplazar '\n' con saltos de línea reales en HTML
                contenido_html = row['Contenido'].split('|')
                for contenido in contenido_html:
                    p = soup.new_tag('p', style='margin:12px;font-size:16px;line-height:24px;font-family:Arial,sans-serif;color:#000000 !important;')
                    p.string = contenido
                    td.append(p)


            if pd.notna(row['Links']) and row['Links']:
                item_counter = 1
                
                links = row['Links'].split('|')  # Suponiendo que los links están separados por comas
                for link in links:
                    text, url = link.split(',')
                    p = soup.new_tag('p', style='margin:0 12px 0 12px ;font-size:16px;line-height:24px;font-family:Arial,sans-serif;color:#000000 !important;')
                    a = soup.new_tag('a', href=url.strip(), target='_blank')
                    a.string = '[{}] {}'.format(item_counter, text.strip())
                    item_counter += 1
                    p.append(a)
                    td.append(p)

            if pd.notna(row['Imagen']) and row['Imagen']:
                imagen = row['Imagen']
                img = soup.new_tag('img', src=imagen, style="width:90%;height:auto;padding:0 5%;")
                td.append(img)
            
            tr.append(td)
            table.append(tr)

        # Guardar el HTML modificado para revisión
        with open(output_name, 'w', encoding='utf-8') as file:
            file.write(soup.prettify(formatter="html"))
    else:
        print("No se encontró la tabla con id 'tabla-destino'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Procesar un archivo CSV y modificar una plantilla HTML.')
    parser.add_argument('csv_file', help='El nombre del archivo CSV con los textos.')
    parser.add_argument('output_name', help='El nombre del html renderizado.')
    parser.add_argument('email_title', help='El título del newsletter.')

    args = parser.parse_args()
    main(args.csv_file, args.email_title, args.output_name)
