# newsletter
Proyecto de desarrollo de newsletter para la Comisión de Mujeres de la Federación Argentina de Karate y Kobudo Okinawense. 

## Antes de empezar...
### Librerías necesarias
Es necesario instalar las siguientes librerías para python:
* argparse
* pandas 
* bs4 
* os
* csv
* smtplib
* argparse
* email  

Todas ellas se instalan con el siguiente comando: 
```bash 
pip install nombrelibreria
```

## Cómo crear un newsletter
### 1. Crear contenido

Se debe crear un archivo con formato .csv y separadores de tipo punto y coma: `;`

Qué poner en cada columna del csv:

* **Fecha**: 
  En formato `Mes año`  
  Por ejemplo: `Junio 2024`
* **Tipo**: 
  El tipo de contenido. Por ahora tenemos dos: 
  * Principal: para la nota principal del boletín.
  * Nota: Para el resto de los contenidos.  
* **Titulo**: 
  El título para el contenido
* **Contenido**:
  El contenido correspondiente al anterior título.  
  Para establecer un salto de línea se debe usar el caracter de barra vertical: `|`
  Ejemplo: `Texto linea 1|Texto linea 2`
* **Links**: 
  Se pueden agregar links de referencia para el contenido correspondiente, con el siguiente formato: 
  `Texto 1,url 1;Texto 2,url 2`  
  Ejemplo de uso:
  `Sitio web FAKKO,https://www.fakko.org/;Sitio web google,https://google.com`  
* **Imagen**:
  Cada contenido puede tener una imagen que, por el momento, se muestra al final del mismo. Por las limitaciones de seguridad de algunos servicios de correo, se recomienda referenciar la imagen con una URL pública (es decir, la imagen debe estar subida en algún sitio web y se debe copiar su dirección web).  
  Ejemplo de uso: 
  `https://www.fakko.org/wp-content/uploads/2019/12/logo-fakko-peq.png`

Ejemplo de un archivo de notas genérico: 
```csv
Fecha;Tipo;Titulo;Contenido;Links;Imagen
Junio 2024;Principal;Titulo 1;Contenido 1 linea 1|Contenido 1 linea 2;Sitio web FAKKO,https://www.fakko.org/;Sitio web google,https://google.com;https://www.fakko.org/wp-content/uploads/2019/12/logo-fakko-peq.png
Junio 2024;Nota;Titulo 2;Contenido 2;;
```
#### Recomendaciones: 
* Crear un archivo diferente por fecha.
* Por cada contenido se debe agregar una línea nueva al final del archivo.
* No hay un límite en la cantidad de líneas que se deba agregar.
* Si el formato es complicado, se puede construir en un archivo excel (o de hojas de cálculo de google) y luego exportar a formato .csv especificando que el separador sea punto y coma.
* Guardar el archivo en la carpeta `inputs` para mantener el orden del repositorio.

### 2. Crear el newsletter en formato html

Este repositorio cuenta con una plantilla en formato html para renderizar el correo a enviar.  

Elementos necesarios para renderizar el correo: 
1. La plantilla recién mencionada
2. El archivo .csv con su contenido. 
3. Un nombre para titular el newsletter.
4. Una ubicación y un nombre para el archivo resultante.

Se debe usar el código ubicado en el directorio raiz: `createNewsLetter.py` a través de la línea de comandos (o consola) de la siguiente manera:  
`python createNewsLetter.py csv_file output_file 'email_title'`  
Siendo: 
* **csv_file**: la ubicación y nombre del archivo de contenidos
* **output_file**: la ubicacion y nombre que queremos para el archivo resultante.
* **email_title**: El título principal para nuestro newsletter.  
Ejemplo de uso: 
```bash 
python createNewsLetter.py inputs/2024-06.csv outputs/2024-06.html 'Newsletter Junio 2024'
```
### 3. Establecer credenciales y lista de destinatarios
Para enviar un correo electrónico con un html renderizado, es necesario hacerlo por fuera de las interfaces habituales de nuestro servicio de correo. En nuestro caso, vamos a usar la linea de comandos.  
Para mantener la seguridad del repositorio, no se guardan las contraseñas en el código. Para esto necesitamos crear un archivo especial con nuestro usuario y contraseña de correo.

* **Credenciales**: 
  Se debe crear un archivo con formato `.env` para definir el email desde el cual se debe enviar el newsletter y su contraseña.  
  El archivo debe verse de la siguiente manera: 
  ```env 
    EMAIL_USER=correo@gmail.com
    EMAIL_PASS=contraseña
  ```
* **Destinatarios**: 
  Se debe crear un archivo .csv con los correos destinatarios con el siguiente formato: 
  ```csv
    email
    destinatario1@example.com
    destinatario2@example.com
    destinatario3@example.com
  ```

  ### 4. Enviar correo 
  El repositorio cuenta con un segundo archivo python `sender.py` para enviar el correo a sus destinatarios.

  Elementos necesarios para enviar el correo: 

  1. El archivo .env descripto en el punto anterior.
  2. El archivo .csv descripto en el punto anterior.
  3. El archivo html resultante del paso 2.
  4. Un asunto para el correo a enviar.

  Se debe usar el código ubicado en el directorio raiz: `sender.py` a través de la línea de comandos (o consola) de la siguiente manera:  
  `python sender credencial destinatarios contenido asunto`

  Ejemplo de uso: 
  ```bash 
    python sender.py credenciales/credencial-testing.env inputs/destinatarixs.csv outputs/2024-06.html 'testing sender'
  ```

  Si el envío del correo fue exitoso se verá en consola el siguiente mensaje: 
  ```bash
    Correo electrónico enviado correctamente a la siguiente lista de destinatarixs:
    ['dest1@ejemplo.com', 'dest2@ejemplo.com']
  ```
  
----

## Proyecto a futuro: 
Se planea desarrollar una plataforma que permita ingresar la información en un entorno amigable para personas que no están familiarizadas con el uso de linea de comandos.


Consultas sobre el código o el funcionamiento de la herramienta:

* Desarrolladora: 
  * [github.com/danimacab](https://github.com/danimacab)
