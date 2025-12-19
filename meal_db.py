import json
from meal import Meal
from search_stratergy import *

class MealDB:
    """
    This class represents a database that will hold the meal data.
    For the prototype, we have used a simple list in python to hold the data.
    """
    _meals : list = []
    SAMPLES_FILE : str = "sample_data/samples.json"

    @staticmethod
    def create_meal(name,ingredients,tags=None):
        """Create a new meal and add it to the 'db'"""
        MealDB._meals.append(Meal(name,ingredients,tags))

    @staticmethod
    def create_sample_meals_from_file(file=SAMPLES_FILE):
        """Load sample meals for the prototype"""
        meals = {}
        with open(file,"r",encoding="utf-8") as f:
            meals = json.load(f)
        for meal_name,meal_data in meals.items():
            MealDB.create_meal(meal_name,meal_data['ingredients'],meal_data['tags'])

    @staticmethod
    def search(query="",stratergy=SearchDefault()):
        """Search for meals based on a given stratergy (Stratergy pattern)"""
        res = filter(lambda meal: stratergy.execute(meal,query),MealDB._meals)
        return list(res)

    @staticmethod
    def list_available_ingredients():
        """List available ingredients"""
        ingredients = set(ingredient for meal in MealDB._meals for ingredient in meal.ingredients)
        return ingredients

    @staticmethod
    def list_available_tags():
        """List available tags"""
        tags = set(tag for meal in MealDB._meals for tag in meal.tags)
        return tags

    @staticmethod
    def list_available_meals():
        """List available meal names"""
        meals = set(meal.name for meal in MealDB._meals)
        return meals