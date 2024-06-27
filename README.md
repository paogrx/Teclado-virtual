# Teclado Virtual con Detección de Gestos

Este proyecto implementa un teclado virtual que utiliza la cámara para detectar gestos de la mano y permite la selección de teclas en pantalla. Es una herramienta útil para interacciones sin contacto en diversas aplicaciones.

## Características

- Detección de gestos de la mano usando MediaPipe.
- Interfaz de teclado en pantalla completa con todas las letras, números y teclas de control.
- Funciones de escritura y edición de texto directamente desde la cámara.
- Incluye teclas especiales como "Borrar" y "Limpiar".

## Requisitos

- Python 3.7 o superior
- OpenCV
- MediaPipe
- Pynput

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu-usuario/teclado-virtual-gestos.git
    cd teclado-virtual-gestos
    ```

2. Instala las dependencias necesarias
    1. Python
Asegúrate de tener Python 3.7 o una versión superior instalada en tu sistema.
    
    pip install python


OpenCV
 es una librería de visión artificial que permite procesar imágenes y videos en tiempo real
    
    pip install opencv-python-headless
    

MediaPipe 
es una biblioteca desarrollada por Google que facilita la implementación de aplicaciones basadas en la percepción, como la detección de gestos.

    pip install mediapipe

Pynput
permite controlar y monitorizar dispositivos de entrada como el teclado y el ratón. Es útil para simular la pulsación de teclas

    pip install pynput

Asegúrate de que tu sistema tenga los siguientes paquetes instalados para evitar problemas de compatibilidad, especialmente si estás trabajando en un entorno Linux (Este proyecto lo desarolle en linux Mint)

    sudo apt-get update
    sudo apt-get install -y python3-pip python3-dev
    sudo apt-get install -y libsm6 libxext6 libxrender-dev
    sudo apt-get install -y libgl1-mesa-glx



    ```

3. Ejecuta el script principal:

       Teclado.py
 
    ```

## Uso

1. Asegúrate de que la cámara está conectada y funcionando.
2. Ejecuta el script `Teclado.py`.
3. El teclado virtual aparecerá en la pantalla.
4. Usa gestos para seleccionar y pulsar teclas:
    - Mueve tu dedo índice sobre la tecla deseada.
    - Para pulsar una tecla, realiza un gesto de pulsación moviendo el dedo hacia abajo.
    - Usa la tecla "Borrar" para eliminar la última letra escrita.
    - Usa la tecla "Limpiar" para borrar todo el texto escrito.

## Contribución

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature-nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva característica'`).
4. Sube tus cambios (`git push origin feature-nueva-caracteristica`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la MIT License - consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para cualquier consulta o sugerencia, puedes contactame: paogrxx@gmail.com
- **Nombre**: Pahola Teobal (Paogrx)
  

---

_Disfruta usando el teclado virtual y contribuye para mejorarlo!_

