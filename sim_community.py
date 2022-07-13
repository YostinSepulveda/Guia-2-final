
from random import randrange,choice
from sim_citizen import Citizen

class Community():
    def __init__(self,
                 name,
                 population,
                 contactProm,
                 contactProb,
                 minFam,
                 maxFam,
                 initialInfected,
                 disease,
                 vaccines,
                 vaccines_start,
                 vaccines_end,
                 core):

        # Variables por definición
        self.name = name
        self.population = population
        self.contactProm = contactProm
        self.contactProb = contactProb
        self.minFam = minFam
        self.maxFam = maxFam
        self.initialInfected = initialInfected

        self.disease = disease

        self.vaccines = vaccines
        self.vaccines_start = vaccines_start
        self.vaccine_period = vaccines_end - vaccines_start
        
        self.core = core

        # Variables por asignación
        self.population_is_generated = True
        self.citizens = []
        self.citizens_disease = []
        self.citizens_affection = []
        self.log = []
        self.step = 0

        # Generar población
        self.core.newStatus("<span foreground='Chartreuse'>Generando Población</span>")
            
        for id_number in range(self.population):

            years_old = randrange(91)
            self.citizens.append(Citizen(id_number,
                                         self,
                                         years_old,
                                         self.disease))

        # Asignar enfermedades base  
        while len(self.citizens_disease) != int(self.population/4):
            target_citizen = choice(self.citizens)
            if not target_citizen in self.citizens_disease:
                target_citizen.set_base_disease()
                self.citizens_disease.append(target_citizen)
        
        # Asignar afeccion
        while len(self.citizens_affection) != int(self.population*0.65):
            target_citizen = choice(self.citizens)
            if not target_citizen in self.citizens_affection:
                target_citizen.set_affection()
                self.citizens_affection.append(target_citizen)

        # Asignar pacientes 0   
        while self.disease.get_cases() != self.initialInfected:
            target_citizen = choice(self.citizens)
            if not target_citizen.is_inmune():
                target_citizen.infect(step=0)

        # Creación de familias
        for citizen in self.citizens:
            if len(citizen.get_family()) < self.minFam:
                if self.avaible_family():
                    while len(citizen.get_family()) < self.minFam:
                        family_member = choice(self.citizens)
                        if family_member != citizen:
                            if len(family_member.get_family()) < self.minFam:
                                if not citizen in family_member.get_family():
                                    citizen.add_family_member(family_member)
                                    family_member.add_family_member(citizen)
                else:
                    self.population_is_generated = False
                    break
        
        for citizen in self.citizens:
                new_max = randrange(self.maxFam+1)
                while len(citizen.get_family()) < new_max:
                    family_member = choice(self.citizens)
                    if family_member != citizen:
                        if len(family_member.get_family()) < self.maxFam:
                            if not citizen in family_member.get_family():
                                citizen.add_family_member(family_member)
                                family_member.add_family_member(citizen)
                citizen.end_gen()

        self.update_log()


    def avaible_family(self):
        avaible_family_spaces = 0
        for citizen in self.citizens:
            if len(citizen.get_family()) < self.minFam:
                avaible_family_spaces += 1
                if avaible_family_spaces == 2:
                    return True
        return False

    def show_population(self):
        self.core.load_citizen_data(self.citizens)

    def take_step(self):
        self.step += 1

        # Vacunación
        if self.step >= self.vaccines_start:
            for i in range(3):
                if self.vaccines[i].get_inventory() != 0:
                    vaccinations = randrange(self.vaccines[i].get_inventory())
                    for k in range(vaccinations):
                        not_ready = True
                        while not_ready:
                            citizen = choice(self.citizens)
                            if not citizen.is_vaccinated():
                                citizen.vaccinate(self.vaccines[i].get_vaccine_type(),self.step)
                                self.vaccines[i].use()
                                not_ready = False

        # Evolución
        for citizen in self.citizens:
            citizen.evolve(self.step)

        # Contacto Cercano
        for contact in range(self.contactProm):
            contact_increment = 0
            infection_increment = 0

            while True:
                citizen_a = choice(self.citizens)
                citizen_b = choice(self.citizens)
                if citizen_a != citizen_b:
                    break

            # Contacto Muy Estrecho
            if citizen_a in citizen_b.get_family():
                contact_increment = 10
                infection_increment = 5

            if randrange(100) < self.contactProb+contact_increment:
                # A infecta B
                if citizen_a.get_status():
                    if not citizen_b.is_inmune():
                        citizen_b.try_infection(self.step,infection_increment)

                # B infecta A
                if citizen_b.get_status():
                    if not citizen_a.is_inmune():
                        citizen_a.try_infection(self.step,infection_increment)

        self.update_log()
    
    def update_log(self):
        active_cases = 0
        death_cases = 0
        curated_cases = 0
        vaccinated_cases = 0

        for citizen in self.citizens:
            if citizen.get_status():
                active_cases += 1
            else:
                if citizen.is_inmune():
                    curated_cases += 1

            if not citizen.is_alive():
                death_cases += 1
            if citizen.is_vaccinated():
                vaccinated_cases += 1

        if vaccinated_cases == 0:
            vaccinated_cases = "---"

        step_log = [int(self.step),
                    int(active_cases),
                    int(self.disease.get_cases()),
                    int(death_cases),
                    int(curated_cases),
                    str(vaccinated_cases)]
        self.log.append(step_log)

    def get_step(self):
        return self.step
    
    def get_log(self):
        self.core.show_log(self.log)
