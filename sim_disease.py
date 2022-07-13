class Disease():
    def __init__(self, probInfection,
                       duration,
                       infectionType,
                       vulnerable):
        
        self.probInfection = probInfection
        self.duration = duration

        self.vulnerable_population = []

        # 20% de mortalidad 
        self.infection_increment = 70/duration

        # Creación de población vulnerable
        if infectionType == 0:
            self.vulnerable_population.append("Asma")
            self.vulnerable_population.append("Fibrosis Quistica")
            self.vulnerable_population.append("Obesidad")

        if infectionType == 1:
            self.vulnerable_population.append("Enfermedad Cerebrovascular")
            self.vulnerable_population.append("Hipertension")
            self.vulnerable_population.append("Obesidad")

        if infectionType == 2:
            self.vulnerable_population.append("Asma")
            self.vulnerable_population.append("Fibrosis Quistica")
            self.vulnerable_population.append("Desnutrición")

        if infectionType == 3:
            self.vulnerable_population.append("Enfermedad Cerebrovascular")
            self.vulnerable_population.append("Hipertension")
            self.vulnerable_population.append("Desnutrición")

        if vulnerable == 0:
            self.vulnerable_population.append("Niño")
        if vulnerable == 1:
            self.vulnerable_population.append("Adolecente")
        if vulnerable == 2:
            self.vulnerable_population.append("Adulto")
        if vulnerable == 3:
            self.vulnerable_population.append("Adulto Mayor")

        self.cases = 0
        
    # Fun - Añadir caso
    def add_case(self):
        self.cases += 1

    """ GETTERS """
    def get_prob(self):
        return self.probInfection
    
    def get_duration(self):
        return self.duration

    def get_cases(self):
        return self.cases

    def get_vulnerable_population(self):
        return self.vulnerable_population

    def get_increment(self):
        return self.infection_increment