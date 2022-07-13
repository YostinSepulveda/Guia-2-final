
from sim_community import Community
from sim_disease import Disease
from sim_simulation import Simulation
from sim_vaccine import Vaccine

class SimulatorCore():
    def __init__(self,core,steps):

        # Creación de la enfermedad
        disease = Disease(int(core.simulation_parameters[7]),
                          int(core.simulation_parameters[8]),
                          int(core.simulation_parameters[9]),
                          int(core.simulation_parameters[10]))

        # Creación de las vacunas
        vaccine_A = Vaccine(vaccine_type=1,
                            inventory=int(int(core.simulation_parameters[1])*0.250),
                            second_dose=6)

        vaccine_B = Vaccine(vaccine_type=2,
                            inventory=int(int(core.simulation_parameters[1])*0.165),
                            second_dose=3)

        vaccine_C = Vaccine(vaccine_type=3,
                            inventory=int(int(core.simulation_parameters[1])*0.085))

        vaccines = [vaccine_A,vaccine_B,vaccine_C]

        # Creación de la comunidad
        community = Community(core.simulation_parameters[0],        #Nombre de la comunidad
                              int(core.simulation_parameters[1]),   #Población
                              int(core.simulation_parameters[2]),   #Promedio de contacto Físico
                              int(core.simulation_parameters[3]),   #Probabilidad de contacto
                              int(core.simulation_parameters[4]),   #Minimo de familiares
                              int(core.simulation_parameters[5]),   #Maximo de familiares
                              int(core.simulation_parameters[6]),   #Infectados Iniciales
                              disease,                              #Enfermedad
                              vaccines,                             #Vacunas
                              int(core.simulation_parameters[11]),  #Inicio del plan de vacunación
                              int(core.simulation_parameters[12]),  #Fin del plan de vacunación
                              core)                                 #El UI

        # Creación de la simulación
        self.simulation = Simulation(community,
                                core)
        


        self.simulation.run(steps)

        core.started = False
        
        if community.population_is_generated:
            core.newStatus("<span foreground='Chartreuse'>Mostrando Resultados</span>")
        else:
            core.newStatus("<span foreground='Firebrick 2'>Error de la generación de las familias</span>")

        