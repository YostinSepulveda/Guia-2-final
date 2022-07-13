"""
El "main" de la interfaz
"""
from tokenize import Number
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Imports de librerias
from gui_numbify import NumberEntry

class ConfigWindow(Gtk.Dialog):
    def __init__(self,parent):
        super().__init__(title="Parámetros de la simulación", transient_for=parent)

        self.set_default_size(400, 200)
        self.set_border_width(10)

        # Parametros
        self.parent = parent
        self.data = []
        self.data_entrys = []
        
        # Variables
        self.confirm_clicks = 0
        
        # Boton - Confirmar
        self.lbl_confirm = Gtk.Label()
        self.lbl_confirm.set_markup("<b><span foreground='Chartreuse'>Confirmar cambios</span></b>")

        box_confirm = Gtk.Box()
        box_confirm.pack_start(self.lbl_confirm,True,True,0)

        self.btn_confirm = Gtk.Button()
        self.btn_confirm.add(box_confirm)
        self.btn_confirm.connect("clicked",self.confirmChanges)
        self.btn_confirm.set_sensitive(False)

        # Boton - Cancelar
        lbl_cancel = Gtk.Label()
        lbl_cancel.set_markup("<span foreground='Firebrick 2'>Cancelar</span>")

        box_cancel = Gtk.Box()
        box_cancel.pack_start(lbl_cancel,True,True,0)

        btn_cancel = Gtk.Button()
        btn_cancel.add(box_cancel)
        btn_cancel.connect("clicked",self.cancel)
        
        # Entrys
        """Comunidad"""
        self.ent_community_name = Gtk.Entry()
        self.ent_community_population = NumberEntry(minimum=4)
        self.ent_community_contact_prom = NumberEntry()
        self.ent_community_contact_prob = NumberEntry(limit=100)
        self.ent_community_family_min = NumberEntry()
        self.ent_community_family_max = NumberEntry()
        self.ent_community_initial_infected = NumberEntry()

        """Enfermedad"""
        self.ent_disease_infection_prob = NumberEntry(limit=100)
        self.ent_disease_infection_duration = NumberEntry()

        """Vacunas"""
        self.ent_vaccines_vacunation_start = NumberEntry()
        self.ent_vaccines_vacunation_end = NumberEntry()

        # Combo Box - Tipo de enfermedad
        self.cbb_disease_infection_type = Gtk.ComboBoxText()
        self.cbb_disease_infection_type.append("0", "Breatitis")
        self.cbb_disease_infection_type.append("1", "VGIA")
        self.cbb_disease_infection_type.append("2", "IRA")
        self.cbb_disease_infection_type.append("3", "DMCR")
        self.cbb_disease_infection_type.set_active(0)

        # Combo Box - Población Vulnerable
        self.cbb_disease_vulnerable_population = Gtk.ComboBoxText()
        self.cbb_disease_vulnerable_population.append("0", "Niño")
        self.cbb_disease_vulnerable_population.append("1", "Adolecente")
        self.cbb_disease_vulnerable_population.append("2", "Adulto")
        self.cbb_disease_vulnerable_population.append("3", "Adulto Mayor")
        self.cbb_disease_vulnerable_population.set_active(0)

        # Labels
        """Comunidad"""
        lbl_community_title = Gtk.Label()
        lbl_community_title.set_markup("<b><big>Comunidad</big></b>")

        lbl_community_name = Gtk.Label(label="Nombre")
        lbl_community_population = Gtk.Label(label="Población")
        lbl_community_contact_prom = Gtk.Label(label="Promedio de contactos")
        lbl_community_contact_prob = Gtk.Label(label="Probabilidad de contacto")
        lbl_community_family_min = Gtk.Label(label="Min. Familiares")
        lbl_community_family_max = Gtk.Label(label="Max. Familiares")
        lbl_community_initial_infected = Gtk.Label(label="Infectados Iniciales")

        """Enfermedad"""
        lbl_disease_title = Gtk.Label()
        lbl_disease_title.set_markup("<b><big>Enfermedad</big></b>")

        lbl_disease_infection_prob = Gtk.Label(label="Probabilidad de infección")
        lbl_disease_infection_duration = Gtk.Label(label="Duración de la enfermedad")
        lbl_disease_infection_type = Gtk.Label(label="Tipo de enfermedad")
        lbl_disease_vulnerable_population = Gtk.Label(label="Población Vulnerable")

        """Vacunas"""
        lbl_vaccines_title = Gtk.Label()
        lbl_vaccines_title.set_markup("<b><big>Vacunas</big></b>")

        lbl_vaccines_vacunation_start = Gtk.Label(label="Inicia el paso")
        lbl_vaccines_vacunation_end = Gtk.Label(label="Acaba el paso")

        # Grid - Comunidad y Vacunas (Lado Izquierdo)
        grd_left = Gtk.Grid()
        grd_left.set_row_spacing(10)
        grd_left.set_column_spacing(10)
        
        """Comunidad"""
        grd_left.attach(lbl_community_title,0,0,4,1)
        
        grd_left.attach(lbl_community_name,0,1,3,1)
        grd_left.attach(self.ent_community_name,3,1,1,1)
        
        grd_left.attach(lbl_community_population,0,2,3,1)
        grd_left.attach(self.ent_community_population,3,2,1,1)

        grd_left.attach(lbl_community_contact_prom,0,3,3,1)
        grd_left.attach(self.ent_community_contact_prom,3,3,1,1)

        grd_left.attach(lbl_community_contact_prob,0,4,3,1)
        grd_left.attach(self.ent_community_contact_prob,3,4,1,1)

        grd_left.attach(lbl_community_family_min,0,5,3,1)
        grd_left.attach(self.ent_community_family_min,3,5,1,1)

        grd_left.attach(lbl_community_family_max,0,7,3,1)
        grd_left.attach(self.ent_community_family_max,3,7,1,1)

        grd_left.attach(lbl_community_initial_infected,0,8,3,1)
        grd_left.attach(self.ent_community_initial_infected,3,8,1,1)

        """Vacunas"""
        grd_left.attach(lbl_vaccines_title,0,9,4,1)

        grd_left.attach(lbl_vaccines_vacunation_start,0,10,3,1)
        grd_left.attach(self.ent_vaccines_vacunation_start,3,10,1,1)
        
        grd_left.attach(lbl_vaccines_vacunation_end,0,11,3,1)
        grd_left.attach(self.ent_vaccines_vacunation_end,3,11,1,1)

        # Grid - Enfermedad (Lado Derecho Superior)
        grd_right_top = Gtk.Grid()
        grd_right_top.set_row_spacing(10)
        grd_right_top.set_column_spacing(10)

        grd_right_top.attach(lbl_disease_title,0,0,4,1)

        grd_right_top.attach(lbl_disease_infection_prob,0,1,3,1)
        grd_right_top.attach(self.ent_disease_infection_prob,3,1,1,1)

        grd_right_top.attach(lbl_disease_infection_duration,0,2,3,1)
        grd_right_top.attach(self.ent_disease_infection_duration,3,2,1,1)

        grd_right_top.attach(lbl_disease_infection_type,0,3,3,1)
        grd_right_top.attach(self.cbb_disease_infection_type,3,3,1,1)

        grd_right_top.attach(lbl_disease_vulnerable_population,0,4,3,1)
        grd_right_top.attach(self.cbb_disease_vulnerable_population,3,4,1,1)

        # Grid - Efecto del tipo de enfermedad
        grd_right_bottom = Gtk.Grid()
        grd_right_bottom.set_row_spacing(10)
        grd_right_bottom.set_column_spacing(10)

        #Box - Derecha
        box_right = Gtk.Box(orientation=1,spacing=20)
        box_right.pack_start(grd_right_top,True,True,0)
        box_right.pack_start(grd_right_bottom,True,True,0)

        # Box - Superior
        box_upper = Gtk.Box(spacing=20)
        box_upper.pack_start(grd_left,True,True,0)
        box_upper.pack_start(box_right,True,True,0)

        # Box - Inferior
        box_bottom = Gtk.Box()
        box_bottom.pack_start(self.btn_confirm,True,True,0)
        box_bottom.pack_start(btn_cancel,True,False,0)

        # Box - Madre
        box = Gtk.Box(orientation =1, spacing = 30)
        box.pack_start(box_upper,True,True,0)
        box.pack_start(box_bottom,True,True,0)

        box_dialog = self.get_content_area()
        box_dialog.add(box)

        # Almacenamiento de entrys
        self.data_entrys.append(self.ent_community_name)
        self.data_entrys.append(self.ent_community_population)
        self.data_entrys.append(self.ent_community_contact_prom)
        self.data_entrys.append(self.ent_community_contact_prob)
        self.data_entrys.append(self.ent_community_family_min)
        self.data_entrys.append(self.ent_community_family_max)
        self.data_entrys.append(self.ent_community_initial_infected)
        self.data_entrys.append(self.ent_disease_infection_prob)
        self.data_entrys.append(self.ent_disease_infection_duration)
        self.data_entrys.append(self.cbb_disease_infection_type)
        self.data_entrys.append(self.cbb_disease_vulnerable_population)
        self.data_entrys.append(self.ent_vaccines_vacunation_start)
        self.data_entrys.append(self.ent_vaccines_vacunation_end)

        # Carga de datos previos
        if self.parent.loaded:
            for index,item in enumerate(self.parent.simulation_parameters):
                if index == 9:
                    self.data_entrys[index].set_active(int(item))
                elif index == 10:
                    self.data_entrys[index].set_active(int(item))
                else:
                    self.data_entrys[index].set_text(item)

        # Conectar los entrys con el checkeo de espacios vacíos
        for widget in self.data_entrys:
            widget.connect("changed",self.checkFullEntrys)            

        self.show_all()

    # Port de los datos al core
    def saveChanges(self):
        self.parent.updateSimulationParameters(self.data)
        self.parent.loaded = True

    # Confirmar/Guardar/Cerrar
    def confirmChanges(self,widget):
        self.confirm_clicks += 1
        
        if self.confirm_clicks == 1:
            self.lbl_confirm.set_markup("<b><big><span foreground='Chartreuse'>¿Seguro?</span></big></b>")
        
        if self.confirm_clicks == 2:
            # Almacenamiento de entrys

            for index,item in enumerate(self.data_entrys):
                if index == 9:
                    self.data.append(item.get_active())
                elif index == 10:
                    self.data.append(item.get_active())
                else:
                    self.data.append(item.get_text())

            self.saveChanges()
            self.lbl_confirm.set_markup("<span foreground='Yellow'>Cerrar ventana</span>")
            self.data=[]

        if self.confirm_clicks == 3:
            self.destroy()
    
    # Destruir el diálogo
    def cancel(self,widget):
        self.destroy()

    # Detectar espacios vacios para bloquear el botón de guardado
    def checkFullEntrys(self,widget):
        self.confirm_clicks = 0
        self.lbl_confirm.set_markup("<b><span foreground='Chartreuse'>Confirmar cambios</span></b>")
        self.btn_confirm.set_sensitive(True)

        for index in range(12):
            if index != 9:
                if index != 10:
                    if self.data_entrys[index].get_text() == "":
                        self.btn_confirm.set_sensitive(False)