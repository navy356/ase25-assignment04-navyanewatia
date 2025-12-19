from meal_db import MealDB
import shutil
from helpers import *
from search_stratergy import *

try:
    #Option to use a nicer menu interface
    from textual.app import *
    from textual.widgets import *
    from textual.containers import *
    from textual.screen import Screen
    from textual.widget import *
    from rich.panel import Panel

    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False


if TEXTUAL_AVAILABLE:

    class MealCard(ListItem):
        """Card that holds meal data"""
        def __init__(self, meal):
            super().__init__(classes="meal-card")
            self.meal = meal

        def compose(self):
            """Construct the visual content of the list item."""
            # Main panel with meal name and tags
            header_text = f"[b]{self.meal.name}[/b]\nTags: {', '.join(self.meal.tags)}"
            yield Static(header_text)
            # Collapsible ingredients
            ingredients_text = "\n".join(self.meal.ingredients)
            with Collapsible(title="Ingredients"):
                yield Label(ingredients_text)

    class MainMenu(Screen):
        """Main Menu Screen"""
        def compose(self):
            """Construct visual elements"""
            # Access app instance via self.app
            yield Header()
            with VerticalScroll():
                with Horizontal():
                    # A RadioSet built up from RadioButtons.
                    with RadioSet(id="focus_me"):
                        for choice in self.app.choices:
                            yield RadioButton(choice["name"])
            yield Footer()

        def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
            """On selection proceed according to choice"""
            label = event.pressed.label
            index = event.radio_set.pressed_index
            event.radio_set.action_toggle_button() #reset radio state
            self.app.push_screen(self.app.choices[index]["screen"](index))

        async def on_mount(self) -> None:
            """Focus radio menu on start"""
            radio = self.query_one(RadioSet)
            radio.focus()

    class SearchScreen(Screen):
        """Search Screen"""
        BINDINGS = [("escape", "app.back", "Go back"),("backspace", "app.back", "Go back")]

        def __init__(self, choice_index):
            """Initialise with selected choice from menu"""
            super().__init__()
            self.choice_index = choice_index
            self.results_list = ListView(
                id="results_list"
            )

        def compose(self):
            """Construct visual elements"""
            # Access app instance via self.app
            yield Header()
            with VerticalScroll():
                with Vertical():
                    yield Input(
                        placeholder=self.app.choices[self.choice_index]["placeholder"]
                    )
                    yield self.results_list
            yield Footer()

        async def on_mount(self) -> None:
            """Focus input"""
            #Commented out to avoid navigation confusion
            # self.query_one(Input).focus()
            pass

        async def on_input_submitted(self, event: Input.Submitted) -> None:
            """Display results on submitting query"""
            query = event.value
            strategy = self.app.choices[self.choice_index]["stratergy"]
            self.results_list.clear()

            results = MealDB.search(query, strategy)

            self.results_list.clear()

            # Add meal cards
            if results:
                meal_cards = []
                for meal in results:
                    meal_cards.append(MealCard(meal))
                await self.results_list.extend(meal_cards)
            else:
                await self.results_list.append(ListItem(Static("No results found.")))

    class AllMealsScreen(Screen):
        "All Meals Screen (Different as no input is needed)"
        BINDINGS = [("escape", "app.back", "Go back"),("backspace", "app.back", "Go back")]

        def __init__(self, choice_index):
            """Initialise with selected choice from menu"""
            super().__init__()
            self.choice_index = choice_index
            self.results_list = ListView(
                id="results_list"
            )

        def compose(self):
            """Construct visual elements"""
            yield Header()
            with VerticalScroll():
                with Vertical():
                    yield self.results_list
            yield Footer()

        async def on_mount(self) -> None:
            """Show all meals from 'db' results"""
            strategy = self.app.choices[self.choice_index]["stratergy"]
            self.results_list.clear()
            results = MealDB.search("", strategy)
            self.results_list.clear()

            # Add meal cards
            if results:
                meal_cards = []
                for meal in results:
                    meal_cards.append(MealCard(meal))
                await self.results_list.extend(meal_cards)
            else:
                await self.results_list.append(ListItem(Static("No meals found.")))

    class QuitScreen(Screen):
        """Screen with a dialog to quit."""

        def compose(self) -> ComposeResult:
            yield Grid(
                Label("Are you sure you want to quit?", id="question"),
                Button("Quit", variant="error", id="quit"),
                Button("Cancel", variant="primary", id="cancel"),
                id="dialog",
            )

        def on_button_pressed(self, event: Button.Pressed) -> None:
            if event.button.id == "quit":
                self.app.exit()
            else:
                self.app.pop_screen()

    class MealMenu(App):
        """A Textual app for SmartCater."""

        CSS_PATH = "app.tcss"
        BINDINGS = [("q", "quit", "Quit")]
        SCREENS = {
            "MainMenu": MainMenu,
            "SearchScreen": SearchScreen,
            "QuitScreen": QuitScreen,
            "AllMealsScreen":AllMealsScreen
        }

        def __init__(self):
            "Initialise with menu choices"
            super().__init__()
            self.choices = [
                {
                    "name": "Search Meals by Name",
                    "placeholder": "Search By Name",
                    "screen": SearchScreen,
                    "stratergy": SearchByName(),
                },
                {
                    "name": "Search Meals by Ingredients",
                    "placeholder": "Search By Ingredients",
                    "screen": SearchScreen,
                    "stratergy": SearchByIngredients(),
                },
                {
                    "name": "Search Meals by Tags",
                    "placeholder": "Search By Tags",
                    "screen": SearchScreen,
                    "stratergy": SearchByTags(),
                },
                {
                    "name": "Show all Meals",
                    "placeholder": "Search By Name",
                    "screen":AllMealsScreen,
                    "stratergy": SearchDefault()
                },
                {
                    "name": "Exit",
                    "args": ("Thank you for visiting SmartCater!",),
                    "screen": QuitScreen,
                },
            ]

        def on_mount(self) -> None:
            """Set theme, title and push main menu screen"""
            self.theme = "gruvbox"
            self.title = "SmartCater"
            self.push_screen("MainMenu")

        def compose(self) -> ComposeResult:
            """Construct visual elements"""
            yield Header()
            yield Footer()

    def run_textual_menu():
        """Run Textual App"""
        menu = MealMenu()
        menu.run()


class ConsonleMealMenu:
    """Console App for SmartCater"""
    def __init__(self):
        """initialise"""
        self.quit = False

    def start_quit(self, msg):
        """exit with a message"""
        self.quit = True
        center_print(msg)

    def list_info(self, info_function, info_display):
        """show requested info"""
        print()
        center_print(info_display, "-")
        data = info_function()
        for item in data:
            center_print(f"{item}")
        center_print("", "-")
        print()

    def search(self, search_stratergy, query=None):
        """show search results"""
        if query is None:
            query = input("Enter search query: ")
        results = MealDB.search(query, search_stratergy)
        center_print(" Search Results ", "-")
        if len(results)==0:
            center_print("No meals found.")
        for result in results:
            print(result)
        center_print("", "-")

    def main_menu(self):
        """main menu"""
        self.quit = False
        while not self.quit:
            choices = [
                {
                    "name": "Search Meals by Name",
                    "helper_function": self.search,
                    "args": (SearchByName(),),
                },
                {
                    "name": "Search Meals by Ingredients",
                    "helper_function": self.search,
                    "args": (SearchByIngredients(),),
                },
                {
                    "name": "Search Meals by Tags",
                    "helper_function": self.search,
                    "args": (SearchByTags(),),
                },
                {
                    "name": "Show all Meals (Default Search Result)",
                    "helper_function": self.search,
                    "args": (SearchDefault(), ""),
                },
                {
                    "name": "List available ingredients",
                    "args": (
                        MealDB.list_available_ingredients,
                        " Available Ingredients ",
                    ),
                    "helper_function": self.list_info,
                },
                {
                    "name": "List available tags",
                    "helper_function": self.list_info,
                    "args": (MealDB.list_available_tags, " Available Tags "),
                },
                {
                    "name": "List available meal names",
                    "args": (MealDB.list_available_meals, "Available Meal Names"),
                    "helper_function": self.list_info,
                },
                {
                    "name": "Exit",
                    "args": ("Thank you for visiting SmartCater!",),
                    "helper_function": self.start_quit,
                },
            ]
            center_print(" Smart Cater ", "=")
            for index in range(len(choices)):
                center_print(f"{index+1}. {choices[index]['name']}")
            center_print("", "=")
            choice = input("Enter your choice: ")
            try:
                choice = int(choice)
                if choice - 1 >= len(choices):
                    raise Exception
                selected_choice = choices[choice - 1]
                selected_choice["helper_function"](*selected_choice["args"])
            except Exception as e:
                print(f"Please enter a valid number between 1 and {len(choices)}")


def run_console_menu():
    """Run console app"""
    ConsonleMealMenu().main_menu()
