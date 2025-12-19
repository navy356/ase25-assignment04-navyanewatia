class Meal:
    """
    This class represents one meal with its associated data
    """
    def __init__(self,name,ingredients,tags=None):
        self.name = name
        self.ingredients = ingredients
        self.tags = tags or []

    def __repr__(self):
        """Display the meal in a neat format"""
        neat_tags = ""
        for tag in self.tags:
            neat_tags = neat_tags + tag + ","
        neat_tags = neat_tags[:-1]
        neat_ingredients = ""
        for ingredient in self.ingredients:
            neat_ingredients = neat_ingredients + ingredient + ","
        neat_ingredients = neat_ingredients[:-1]
        meal_format = f"Name: {self.name} | Tags: {neat_tags} | Ingredients: {neat_ingredients}"
        return meal_format