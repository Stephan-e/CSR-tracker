from enumfields import Enum

class IngredientCategory(Enum):
    PLANT_BASED = 'plant_based'
    ANIMAL_BASED = 'animal_based'
    BASE = 'base'
    NONE = 'none'