"""
clase vacuna, contenedor de atributos
"""

class Vaccine():
    def __init__(self,
                 vaccine_type,
                 inventory,
                 second_dose=0):

        self.vaccine_type = vaccine_type
        self.inventory = inventory
        self.second_dose = second_dose

    def get_vaccine_type(self):
        return self.vaccine_type

    def get_inventory(self):
        return self.inventory

    def use(self):
        if self.inventory == 0:
            return False
        else:
            self.inventory -= 1
            return True