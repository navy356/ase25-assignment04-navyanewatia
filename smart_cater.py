from meal_db import MealDB
from search_stratergy import *
from menu import *

def main():
    """Main function to launch SmartCater"""
    MealDB.create_sample_meals_from_file()
    #Only run textual app if textual is available
    use_textual = True
    if use_textual and TEXTUAL_AVAILABLE:
        run_textual_menu()
    else:
        run_console_menu()

if __name__ == "__main__":
    main()