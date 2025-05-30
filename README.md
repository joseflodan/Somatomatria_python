# Somatomatria_Python


REQUIERE LO SIGUIENTE 
Una carpeta nueva y vacia 
#usar el cmd como administrador y ejecutar lo siguiente

>$cd rutadetucarpeta

dentro de esto hacer lo siguiente 

iniciar un entorno virtual

   - >$python -m venv somatomatria
   - >$cd somatomatria
   - >$ mkdir src    
   - >$cd scripts
   - >$activate

una vez dentro de scripts y que estos esten activos se hace lo siguiente
instalar lo siguinte 

  - >$pip install PyQt6
  - >$pip install PyQt6-tools
  - >$pip install PySide6

Despues de eso abrimos un cmd y copiamos la ruta del somatomatria y aqui crearemos otros carpetas
   
   - >$cd rutadetucarpeta
   - >$cd somatomatria
   - >$cd src
   - >$mkdir backend
   - >$mkdir frontend


una ves fuera y con esto instalado bajar el codigo de este git en formato zip y hacer lo siguiente

   -descomprimir y mover todo a src y sus otras carpetas 

      -Todo el proyecto desplegado se deberia ver asi

         Nombre_de_tu_carpeta/
         |-Somatomatria/
           |-include/
           |-lib/
           |-script/
           |-src/
             |-backend/
               |-database.py/               
               |-scritp.sql/
             |-frontend/
               |-gui.py/
               |-usr.png/
             |-main.py/
           |-gitignore/
           |-pyvenv.cfg/
           |somatomatria.db/
   
   -para correrlo ocupamos el main.py / en caso de que la primer ejecucion falle no es por que este mal sono porque apenas creo somatomatria.db asi que ejecutar de nuevo 
    
