from meal_db import MealDB
from search_stratergy import *
from menu import *
import sys

def main():
    """Main function to launch SmartCater"""
    MealDB.create_sample_meals_from_file()
    #Only run textual app if textual is available
    use_textual = True
    if len (sys.argv)>1 and sys.argv[1] == "console":
        use_textual = False
    if use_textual and TEXTUAL_AVAILABLE:
        run_textual_menu()
    else:
        run_console_menu()

if __name__ == "__main__":
    main()