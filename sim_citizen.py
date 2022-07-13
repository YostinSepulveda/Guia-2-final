
from random import randrange,choice

class Citizen():
    def __init__(self,id_number,
                      community,
                      years_old,
                      disease):
        
        # Variables por definición
        self.id_number = id_number
        self.community = community
        self.years = years_old
        self.disease = disease
        self.status = False
        self.inmune = False
        self.infection_date = "<span foreground='cyan'>Nunca fué infectado</span>"
        self.infection_step = 0
        self.isAlive = True

        # Variables por Asignación
        self.family = []
        self.affection = "Ninguna"
        self.base_disease = "Ninguna"
        self.mortality = 30
        self.infection_status = 0
        self.is_in_danger = False
        self.vaccinated = False
        self.vaccine = 0
        self.personal_log = ""

        if self.years <= 12:
            self.age = "Niño"
        elif self.years <= 18:
            self.age = "Adolecente"
        elif self.years <= 60:
            self.age = "Adulto"
        else:
            self.age = "Adulto Mayor"


    # Terminar generación
    def end_gen(self):
        if self.age in self.disease.get_vulnerable_population():
            self.mortality += 10
        if self.affection in self.disease.get_vulnerable_population():
            self.mortality += 10
        if self.base_disease in self.disease.get_vulnerable_population():
            self.mortality += 15

    # Infección
    def infect(self,step):
        self.inmune = True
        self.status = True
        self.disease.add_case()
        self.infection_date = "Fue infectado en el paso <span foreground='Lime'>"+str(step)+"</span>"
        self.infection_step = int(step)

        if step == 0:
            self.infection_date = "<span foreground='Lime'>Paciente 0</span>"

    def try_infection(self,step,increment):
        if randrange(100) < self.disease.get_prob()+increment:
            self.infect(step)

    # Evolución de la infección
    def evolve(self,step):
        if self.status:
            if (step - self.infection_step) >= self.disease.get_duration():
                self.status = False
                self.inmune = True

            if randrange(100) < self.mortality:
                self.infection_status += self.disease.get_increment()
            if self.infection_status >= 70:
                self.is_in_danger = True
            if self.infection_status >= 70:
                self.isAlive = False

    # Vacunación
    def vaccinate(self,vaccine,step):
        self.vaccine = vaccine
        self.vaccinated = True
        self.personal_log = "<span foreground='cyan'>Vacunado["+str(self.vaccine)+"]</span> en el paso "+str(step)
        if self.vaccine == 1:
            self.mortality -= 25
        if self.vaccine == 2:
            self.mortality = 0
        if self.vaccine == 3:
            self.status = False

    # Setters & Getters
    def get_family(self):
        return self.family

    def add_family_member(self,family_member):
        self.family.append(family_member)

    def is_inmune(self):
        return self.inmune

    def get_status(self):
        return self.status

    def set_affection(self):
        self.affection = choice(["Obesidad","Desnutrición"])
        self.mortality += 10
        
    
    def set_base_disease(self):
        self.base_disease = choice(["Asma","Enfermedad Cerebrovascular","Fibrosis Quistica","Hipertension"])
        self.mortality += 15

    def get_id_number(self):
        return self.id_number

    def get_age(self):
        info_age = str(self.years)+" <b>("+self.age+")</b>"
        return info_age

    def get_afection(self):
        return self.affection

    def get_base_disease(self):
        return self.base_disease
    
    def is_alive(self):
        return self.isAlive

    def get_family_ids(self):
        family_ids = ""
        for member in self.family:
            family_ids = family_ids +" "+str(member.get_id_number())+" "
        return ("["+family_ids+"]")

    def get_info_status(self):
        if self.isAlive:
            if self.status:
                return "<span foreground='Lime'>Infectado</span>"
            else:
                if self.inmune:
                    return "<span foreground='magenta'>Curado</span>"
                else:
                    return "<span foreground='cyan'>Sano</span>"
        else:
            return "<span foreground='Firebrick 2'>Muerto</span>"

    def get_infection_date(self):
        return self.infection_date

    def is_vaccinated(self):
        return self.vaccinated

    def get_personal_log(self):
        return self.personal_log