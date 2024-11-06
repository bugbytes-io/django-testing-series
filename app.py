class Superhero:
    def __init__(self, name, strength_level):
        self.name = name
        self.strength_level = strength_level

    def __str__(self):
        return self.name
    
    def is_stronger_than(self, other_hero) -> bool:
        return self.strength_level > other_hero.strength_level