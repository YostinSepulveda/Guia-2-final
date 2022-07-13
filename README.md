Simulador de modelo SIR
Este proyecto es un simulador de una infección codificada entorno al modelo SIR para análisis de infecciones infecciosas.

Requisitos:
Librería Gtk

Ejecucion
Para ejecutar el proyecto se debe abrir el archivo gui_core.py desde la terminal mediante el uso de python3. $python3 gui_core.py

Primer Lanzamiento
Apenas se ejecuta el "core" de la interfaz gráfica, se desplegará la ventana del núcleo del proyecto. Los elementos que se lograron ver son:

Botón ACERCA DE :

Este botón despliega una ventana que muestra la información del proyecto además de incluir un botón que te redirige a este repositorio.

Boton Abrir :

En es
Boton ✏️(lapiz):

Al presionar este botón tendremos acceso a la edición de distintos parámetros para la simulación de nuestra enfermedad.
Entradas de Parámetros.

Luego de presionar el botón se abre una ventana en donde debemos ingresar los distintos datos tales como; Nombre de la enfermedad, población de nuestra comunidad, promedios de contactos, etcétera.
Botón Confirmar cambios :

Este botón nos permite confirmar los parametros ingresados, luego se abrira un boton pidiendonos confirmar nuevamente nuestros datos.
																										
Botón y entrada Iniciar(pasos) :

Aqui se ingresa el numero de pasos a ejecutar y se da inicio al programa.
Tabla de resultados :

Aquí se desplegará el registro paso por paso de la simulación, mostrando datos como el número del paso, la cantidad de casos activos, casos totales, muertos, curados y vacunados
Lista de ID:

Aqui se desplegará el registro seleccionable de todos los ciudadanos separados por su id
Display inferior:

Aqui se mostraran los datos unicos de cada persona seleccionada en la Lista de ID, como su edad, familiares y afecciones
Display derecho

Aqui se mostra un resumen de los parametros de la enfermedad previamente ingresados

metodologia
El proyecto consta de 10 archivos de ejecución.

gui_core (Gtk.Window) Es el núcleo de la intefáz gráfica del usuario, en esta se lleva a cabo la gran mayoría de métodos relacionados con el uso de información en la pantalla. Consta de los siguientes métodos:

updateSimulationParameters este método se encarga de detectar el cambio dentro de las entradas de cada variable con el fin de cambiar la alerta en caso de tratar de iniciar la simulación con alguna variable vacía.

start Método accionado por el botón de tras presionar el boton incisr, este se encarga de recolectar y administrar la información para entregarla al core de la simulación.

openFile Este metodo nos permite abrir un archivo de nuestro directorio para ser abierto en nuestro programa

isCompatible este metodo se encarga de chequear si el archivo es compatible con el programa.

isNotCompatible este metodo es accionado si el archivo no es compatible con el programa indicandolo mediante una ventana informativa.

populationNoGenerated Este metodo es accionado cuando existe un problema en la generacion de la poblacion, entregandonos un mensaje dentro de una ventana con una posible solucion.

load_citizen_data Este metodo nos permite cargar a los ciudadanos

show_citiezen_data Este metodo se encarga de mostrar todos los datos de los ciudadanos de la comunidad

config Este metodo abre la ventana para crear nuestra simulacion

about Muestra la ventana con informacion.

gui_stepsWindow (Gtk.Dialog) Es la ventana de diálogo encargada de confirmar toda la información de la simulación antes de ejecutarla, además de pedir la cantidad de pasos a simular.

gui_about (Gtk.Dialog) Es la ventana de diálogo contenedora de información del proyecto.

sim_core Es el objeto encargado de organizar todo para la correcta ejecución de la simulación, funciona como el "main" del código encargado de la simulación, crea la comunidad, la enfermedad, las vacunas, las afecciones y las ingresa de la simulación que también es creado por este objeto (tanto la comunidad, la enfermedad y la comunidad son objetos).

sim_simulation Este objeto se encarga de ejecutar los pasos indicados en la comunidad que se le es entregada.

sim_comunity Este es uno de los objetos más complejos, apenas es creado genera la población indicada, círculos cercanos y por último infecta inicialmente la cantidad de personas indicadas. 

sim_disease La enfermedad, se encarga de infectar a los ciudadanos de acuerdo a su vulnerabilidad.

sim_citizen El ciudadano o persona, se generó con un identificador único en sim_comunidad, es el objeto más complejo del proyecto, se encarga de manejar todos los datos y acciones de un ciudadano.

sim_vaccine.py Las vacunas creadas para poder combatir la enfermedad.

gui_config.py Configuracion de la ventana del ingreso de parametros de la simulacion.

gui_numbify.py Nos permite limitar la entrada de datos no deseados, ya sea limitandolos a solo letras o solo numeros.

Desarrollado por Ángel Guerrero y Yostin Sepúlveda
Gracias especiales a:
Ivo Wetzel Por crear las bases para el archivo numbify.py y publicarlo en la página de ayuda de stack overflow .
