

class Simulation():
    def __init__(self,community,core):
        self.community = community
        self.core = core
    
    def run(self,steps):
        if self.community.population_is_generated:
            for i in range(int(steps)):
                self.community.take_step()
        else:
            self.core.populationNoGenerated()
        
        self.community.show_population()
        self.community.get_log()