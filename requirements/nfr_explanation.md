# Adressing the selected NFR
**As a developer, I want the platform to be easy to maintain and extend with new meal types or dietary rules so that the platform can evolve with changing requirements.**
## Explanation
The implementation supports maintainability and extensibility by separating meal storage, search logic, and user interface concerns into independent components. Meal search behavior is implemented using the Strategy pattern, allowing new dietary rules or search criteria (such as vegan or gluten-free meals) to be added by introducing new strategy classes without modifying existing search code. This design ensures that adding new meal types, tags, or dietary rules does not impact core application functionality.
## Assumptions
- The implementation uses MealDB as a class to store meal data. For the prototype it is simply stored in a list but in a proper application it would be replaced with a database. MealDB mimics such a database.
- This implementation assumes that core functionalily of the app itself is not changed when adding new meal types or dietary rules. Eg: A Vegan tag is not expected to check if all ingredients are actually vegan.
- We assume that the tags associated with the meal are correct.
- We assume that the customer will only search by one ingredient or tag for the prototype. It can be extended for the proper app.
## Limitations
- While the Strategy pattern makes it easy to add new search or dietary rules, some extensions may still require changes to supporting components (e.g., user interface menus or configuration), meaning extensibility is not completely isolated.
- Dietary rules are represented as simple tags rather than rule-based evaluations of ingredients, which limits how far the system can be extended without introducing more complex validation logic.
- The use of in-memory data simplifies extension for the prototype, but it does not reflect the additional maintenance complexity introduced by real databases, migrations, or data consistency constraints.
<!--stackedit_data:
eyJoaXN0b3J5IjpbMzgyMzY1OTk0XX0=
-->