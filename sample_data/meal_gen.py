import requests
import json
import sys

TARGET_URL = 'https://www.themealdb.com'
FILE = "samples.json"

class MealSamples:
    """Class to generate sample meals for prototype"""
    @staticmethod
    def find_random_meal(meal):
        """Pull a random meal from themealdb.com and clean structure"""
        res = requests.get(f"{TARGET_URL}/api/json/v1/1/random.php")
        meal_raw = res.json()['meals'][0]
        meal[meal_raw['strMeal']]={}
        meal[meal_raw['strMeal']]['ingredients'] = []
        for key,val in meal_raw.items():
            if key.startswith("strIngredient") and val.strip()!="":
                meal[meal_raw['strMeal']]['ingredients'].append(val)
        meal[meal_raw['strMeal']]['tags'] = set()
        if meal_raw['strCategory']:
            meal[meal_raw['strMeal']]['tags'].add(meal_raw['strCategory'].strip())
        if meal_raw['strArea']:
            meal[meal_raw['strMeal']]['tags'].add(meal_raw['strArea'].strip())
        if meal_raw['strTags']:
            extra_tags = meal_raw['strTags'].split(',')
            meal[meal_raw['strMeal']]['tags'].update(extra_tags)

        meal[meal_raw['strMeal']]['tags'] = list(meal[meal_raw['strMeal']]['tags'])

    @staticmethod
    def find_n_random_meals(n):
        """Pull n random meals and store"""
        meals = dict()
        for i in range(n):
            MealSamples.find_random_meal(meals)

        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(meals, f, indent=4)
        return meals

def main():
    if len(sys.argv)<2:
        print("Usage: python meal_gen.py <n> (n = number of samples)")
        sys.exit()
    try:
        n = int(sys.argv[1])
        meals = MealSamples.find_n_random_meals(n)
        print(json.dumps(meals, indent=4))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()