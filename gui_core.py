"""
El "main" de la interfaz
"""
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,Gdk

# Imports de librerias
from gui_numbify import NumberEntry
from gui_config import ConfigWindow
from sim_core import SimulatorCore
from gui_about import About

class Core(Gtk.Window):
    def __init__(self):
        # Builder - Conf. Inicial
        super().__init__()
        self.set_default_size(800,600)
        self.set_border_width(10)
        self.set_resizable(False)

        # Variables Por Definición
        self.loaded = False
        self.started = False

        self.parameters = []

        self.simulation_parameters = []

        """Construcción de la UI"""
        
        # Boton - Abrir
        btn_openfile = Gtk.Button(label="Abrir")
        btn_openfile.connect("clicked",self.openFile)

        # Boton - Configurar
        btn_config = Gtk.Button(label="✎")
        btn_config.connect("clicked",self.config)

        # Boton - About
        btn_about = Gtk.Button(label="[ i ]")
        btn_about.connect("clicked",self.about)
    
        # HeaderBar
        self.header = Gtk.HeaderBar(title = "SIR Pymulator mk.2")
        self.header.props.show_close_button = True

        self.header.pack_start(btn_openfile)
        self.header.pack_start(btn_config)
        self.header.pack_end(btn_about)

        self.set_titlebar(self.header)

        # Labels - Parametros
        """Comunidad"""
        lbl_community_title = Gtk.Label()
        lbl_community_title.set_markup("<b>Comunidad</b>")
        
        lbl_community_name = Gtk.Label(label="nom: ---")
        lbl_community_population = Gtk.Label(label="pob: ---")
        lbl_community_contact_prom = Gtk.Label(label="ctp: --")
        lbl_community_contact_prob = Gtk.Label(label="ct%: --%")
        lbl_community_family_min = Gtk.Label(label="fm[-]: --")
        lbl_community_family_max = Gtk.Label(label="fm[+]: --")
        lbl_community_initial_infected = Gtk.Label(label="ini: --")

        self.parameters.append(lbl_community_title)
        self.parameters.append(lbl_community_name)
        self.parameters.append(lbl_community_population)
        self.parameters.append(lbl_community_contact_prom)
        self.parameters.append(lbl_community_contact_prob)
        self.parameters.append(lbl_community_family_min)
        self.parameters.append(lbl_community_family_max)
        self.parameters.append(lbl_community_initial_infected)

        """Enfermedad"""
        lbl_disease_title = Gtk.Label()
        lbl_disease_title.set_markup("<b>Enfermedad</b>")

        lbl_disease_infection_prob = Gtk.Label(label="in%: --%")
        lbl_disease_infection_duration = Gtk.Label(label="dur: --")
        lbl_disease_infection_type = Gtk.Label(label="typ: --")
        lbl_disease_vulnerable_population = Gtk.Label(label="vln: --")

        self.parameters.append(lbl_disease_title)
        self.parameters.append(lbl_disease_infection_prob)
        self.parameters.append(lbl_disease_infection_duration)
        self.parameters.append(lbl_disease_infection_type)
        self.parameters.append(lbl_disease_vulnerable_population)

        """Vacunas"""
        lbl_vaccines_title = Gtk.Label()
        lbl_vaccines_title.set_markup("<b>Vacunas</b>")

        lbl_vaccines_vacunation_start = Gtk.Label(label="Inicia el paso --")
        lbl_vaccines_vacunation_end = Gtk.Label(label="Acaba el paso --")

        self.parameters.append(lbl_vaccines_title)
        self.parameters.append(lbl_vaccines_vacunation_start)
        self.parameters.append(lbl_vaccines_vacunation_end)

        # Label - Estado de la simulación
        self.lbl_status = Gtk.Label()
        self.lbl_status.set_markup("<span foreground='yellow'>Esperando datos de simulación</span>")

        # Entry - Pasos
        self.ent_steps = NumberEntry()
        self.ent_steps.set_placeholder_text("Número de pasos")

        # Boton - Iniciar Simulacion
        self.btn_start = Gtk.Button(label="Iniciar [⊳]")
        self.btn_start.connect("clicked",self.start)
        self.btn_start.set_sensitive(False)

        # Treeview - Lista de ciudadanos
        self.lss_citizens = Gtk.ListStore(int)   # Paso

        self.trv_citizens = Gtk.TreeView(model = self.lss_citizens)
        self.trv_citizens.connect("cursor-changed",self.show_citizen_data)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Id", renderer, text=0)
        self.trv_citizens.append_column(column)

        # Scrolled Window - Lista de ciudadanos
        scr_population = Gtk.ScrolledWindow()
        scr_population.set_vexpand(True)
        scr_population.set_hexpand(True)

        scr_population.add(self.trv_citizens)

        # Treeview - Lista de resultados por paso
        self.lss_results = Gtk.ListStore(int,   # Paso
                                         int,   # Casos Activos
                                         int,   # Casos Totales
                                         int,   # Muertos
                                         int,   # Curados
                                         str)   # Vacunados

        trv_results = Gtk.TreeView(model = self.lss_results)

        for i, column_title in enumerate(["Paso",
                                          "Activos",
                                          "Totales", 
                                          "Muertos",
                                          "Curados",
                                          "Vacunados"]):

            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            trv_results.append_column(column)

        # Scrolled Window - Lista de resultados por paso
        scr_result = Gtk.ScrolledWindow()
        scr_result.set_vexpand(True)
        scr_result.set_hexpand(True)
        scr_result.add(trv_results)

        # Box - Parámetros
        box_parameters = Gtk.Box(orientation=1,spacing=5)
        
        for parameter in self.parameters:
            parameter.set_xalign(0)
            box_parameters.pack_start(parameter,True,True,0) 

        # Grid - Información detallada del ciudadano
        grd_citizen = Gtk.Grid()
        grd_citizen.set_row_spacing(5)
        grd_citizen.set_column_spacing(20)

        self.lbl_citizen_title = Gtk.Label()
        self.lbl_citizen_title.set_xalign(0)
        self.lbl_citizen_title.set_markup("<b>Ciudadano</b>       --")

        self.lbl_citizen_status = Gtk.Label()
        self.lbl_citizen_status.set_xalign(0)
        self.lbl_citizen_status.set_markup("<span foreground='cyan'>Sano</span>")

        self.lbl_citizen_age = Gtk.Label(label="Edad: --")
        self.lbl_citizen_age.set_xalign(0)

        self.lbl_citizen_family = Gtk.Label(label="Familiares: --")
        self.lbl_citizen_family.set_xalign(0)

        self.lbl_citizen_condition_a = Gtk.Label(label="Enfermedad: --")
        self.lbl_citizen_condition_a.set_xalign(0)

        self.lbl_citizen_condition_b = Gtk.Label(label="Afección: --")
        self.lbl_citizen_condition_b.set_xalign(0)

        self.lbl_citizen_date = Gtk.Label(label="--")
        self.lbl_citizen_date.set_xalign(0)

        self.lbl_citizen_personal_log = Gtk.Label(label="")
        self.lbl_citizen_personal_log.set_xalign(0)

        grd_citizen.add(self.lbl_citizen_title)
        grd_citizen.attach(self.lbl_citizen_status,1,0,1,1)
        grd_citizen.attach(self.lbl_citizen_age,0,1,1,1)
        grd_citizen.attach(self.lbl_citizen_family,1,1,1,1)
        grd_citizen.attach(self.lbl_citizen_condition_a,0,2,1,1)
        grd_citizen.attach(self.lbl_citizen_condition_b,1,2,1,1)
        grd_citizen.attach(self.lbl_citizen_date,0,3,1,1)
        grd_citizen.attach(self.lbl_citizen_personal_log,0,4,2,1)

        # Contenedores
        grd_simulation = Gtk.Grid()
        grd_simulation.set_column_spacing(20)
        grd_simulation.add(scr_population)
        grd_simulation.attach(scr_result,1,0,7,1)
        grd_simulation.attach(box_parameters,8,0,4,1)

        box_steps = Gtk.Box()
        box_steps.pack_start(self.ent_steps,False,False,0)
        box_steps.pack_start(self.btn_start,False,False,0)

        box_status = Gtk.Box(orientation=1,spacing=10)
        box_status.pack_start(self.lbl_status,False,False,0)
        box_status.pack_start(box_steps,False,False,0)

        box_info = Gtk.Box(spacing=150)
        box_info.pack_start(grd_citizen,False,False,10)
        box_info.pack_end(box_status,False,False,10)
        #box_info.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0.2,0.2,0.2,100))
        
        grd_main = Gtk.Grid()
        grd_main.set_row_spacing(30)

        grd_main.add(grd_simulation)
        grd_main.attach(box_info,0,1,1,1)

        print(self.get_size())

        self.add(grd_main)

    # Actualizar los datos de la simulación
    def updateSimulationParameters(self,update):
        self.btn_start.set_sensitive(True)
        if self.loaded:
            self.simulation_parameters = []
        for item in update:
            self.simulation_parameters.append(item)

        """Comunidad"""
        self.parameters[1].set_text(("nom: "+update[0]))
        self.parameters[2].set_text(("pob: "+update[1]))
        self.parameters[3].set_text(("ctp: "+update[2]))
        self.parameters[4].set_text(("ct%: "+update[3]))
        self.parameters[5].set_text(("fm[-]: "+update[4]))
        self.parameters[6].set_text(("fm[+]: "+update[5]))
        self.parameters[7].set_text(("ini: "+update[6]))

        """Enfermedad"""
        self.parameters[9].set_text(("in%: "+update[7]))
        self.parameters[10].set_text(("dur: "+update[8]))
        
        # Definir tipo de enfermedad por nombre, no por id
        if int(update[9]) == 0:
            typ = "Breatitis"
        if int(update[9]) == 1:
            typ = "VGIA"
        if int(update[9]) == 2:
            typ = "IRA"
        if int(update[9]) == 3:
            typ = "DMCR"

        self.parameters[11].set_text(("typ: "+typ))
        self.parameters[12].set_text(("vln: "+str(update[10])))
        
        """Vacunas"""
        self.parameters[14].set_text(("sta: "+update[11]))
        self.parameters[15].set_text(("end: "+update[12]))

    # Comenzar con la simulación
    def start(self,widget):
        if self.ent_steps.get_text() != "":
            self.started = True
            sim_core = SimulatorCore(self,int(self.ent_steps.get_text()))

        else:
            self.newStatus("<span foreground='Firebrick 2'>Ingresa la cantidad de pasos a simular</span>")

    # Check de compatibilidad del archivo
    def isCompatible(self,file,total_lines):
        if total_lines == 15:
            for index,line in enumerate(file):
                if index == 0:
                    if "#SIR_Pymulator_compatible" in line:
                        return True

    def isNotCompatible(self):
        dialog = Gtk.MessageDialog(transient_for=self, flags=0,
                                   message_type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.CANCEL,
                                   text="Archivo erróneo o corrupto",)

        dialog.format_secondary_text(("El archivo que trataste de cargar no es compatible"+
                                     "o está dañado, asegurate de que sea compatible visi"+
                                     "tando el repositorio del proyecto y comprobandolo e"+
                                     "n la sección de \n\nCREANDO UN PRE-CONFIG"))
        dialog.run()
        dialog.destroy()

    # Abrir el dialogo para seleccionar un archivo de precofig
    def openFile(self,widget):
        fileDialog = Gtk.FileChooserDialog(title="Seleccion de archivo pre-cargado",
                                            parent=self,
                                            action=Gtk.FileChooserAction.OPEN)
            
        fileDialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        # Filtro de archivos
        filter_txt = Gtk.FileFilter()
        filter_txt.set_name("archivo de texto (.txt)")
        filter_txt.add_pattern("*txt")

        fileDialog.add_filter(filter_txt)

        response = fileDialog.run()
        if response == Gtk.ResponseType.OK:
            # Contenedor de datos
            file_data = []

            # Almacenamiento del archivo en una varible
            file = open(fileDialog.get_filename(), "r+")

            with open(fileDialog.get_filename(), "r+") as data_file:
                total_lines = sum(1 for space in data_file)

            # Guardado de nombre en el subtítulo
            file_name = fileDialog.get_filename().split("/")
            self.header.set_subtitle(("Archivo cargado: " + file_name[-1]))

            # Procesado del archivo
            if self.isCompatible(file,total_lines):
                self.loaded = True
                for index,line in enumerate(file):
                    if index != 0:
                        line_text = line.replace("\n","")
                        file_data.append(line_text)
                    
                self.updateSimulationParameters(file_data)
            else:
                fileDialog.destroy()
                self.isNotCompatible()
                self.header.set_subtitle((file_name[-1]+" dañado o no es compatible"))

            fileDialog.destroy()
        else:
            fileDialog.destroy()

    # Error de la población
    def populationNoGenerated(self):
        dialog = Gtk.MessageDialog(transient_for=self, flags=0,
                                   message_type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.CANCEL,
                                   text="Error en la generación de la comunidad",)

        dialog.format_secondary_text(("Hubo un error al crear la comunidad, esto se debe a"+
                                     "que en la creación de las familias existían familias "+
                                     "a las que le faltan miembros aunque existan disponibles"+
                                     "\n\n Intenta cambiar el minimo de los familiares a 1"))
        dialog.run()
        dialog.destroy()

    # Cargar los ciudadanos
    def load_citizen_data(self,citizen_data):
        self.lss_citizens.clear()
        self.citizens = citizen_data

        for citizen_id in self.citizens:
            self.lss_citizens.append([citizen_id.get_id_number()])

    # Mostrar datos del ciudadano
    def show_citizen_data(self,widget):
        if not self.started:
            model, treeiter = widget.get_selection().get_selected()
            if treeiter != None:
                citizen_id = model[treeiter][0]
                        
            # Mostrar info del ciudadano correspondiente
            self.lbl_citizen_title.set_markup("<b>Ciudadano</b> <b>   <big>"+str(self.citizens[citizen_id].get_id_number())+"</big></b>")
            self.lbl_citizen_status.set_markup(str(self.citizens[citizen_id].get_info_status()))
            self.lbl_citizen_age.set_markup("Edad "+str(self.citizens[citizen_id].get_age()))
            self.lbl_citizen_family.set_markup(self.citizens[citizen_id].get_family_ids())
            self.lbl_citizen_condition_a.set_markup(self.citizens[citizen_id].get_base_disease())
            self.lbl_citizen_condition_b.set_markup(self.citizens[citizen_id].get_afection())
            self.lbl_citizen_date.set_markup(self.citizens[citizen_id].get_infection_date())
            self.lbl_citizen_personal_log.set_markup(self.citizens[citizen_id].get_personal_log())

    def show_log(self,logs):
        self.lss_results.clear()
        for log in logs:
            self.lss_results.append(log)

    # Abrir el dialogo de configuracion/creacion de simulacion
    def config(self,widget):
        config = ConfigWindow(self)
        config.run()
        config.destroy()

    def newStatus(self,status):
        self.lbl_status.set_markup(status)

    # Abrir el dialogo about
    def about(self,widget):
        About(self)
        
# Ejecución core
main = Core()
main.connect("destroy", Gtk.main_quit)
main.show_all()
Gtk.main()