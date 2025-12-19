from abc import ABC, abstractmethod

## Strategy interface
class SearchStrategy(ABC):
    """Abstract class for stratergy pattern for searching meals"""
    @abstractmethod
    def execute(self,meal,query):
        pass

## Concrete strategies
class SearchByName(SearchStrategy):
    """Search for a meal by its name (substring)"""
    def execute(self,meal,query):
        return query.lower() in meal.name.lower()

class SearchByIngredients(SearchStrategy):
    """Search for a meal by ingredient"""
    def execute(self,meal,query):
        return query.lower() in [ingredient.lower() for ingredient in meal.ingredients]

class SearchByTags(SearchStrategy):
    """Search for a meal by tag"""
    def execute(self,meal,query):
        return query.lower() in [tag.lower() for tag in meal.tags]

class SearchDefault(SearchStrategy):
    """Default search which returns all meals"""
    def execute(self,meal,query):
        return True