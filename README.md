**Overview**
- **Project**: `banking.py` — a small CLI and programmatic helper for collecting monthly expenses and computing a "Budget Bee" score.
- **Purpose**: Help a user gather a simple monthly expense survey, compute category and total spending, then produce a single Budget Bee score (10–100) that reflects how well the user is staying within a monthly budget.

**Quick Start**
- **Run CLI**: `python banking.py` — walks through a questionnaire, asks for a monthly budget, computes the initial Budget Bee score, and allows adding extra transactions interactively.
- **Requirements**: Python 3.8+ (no external packages).

**API / Main Classes**
- **`Login(username, password)`**: basic login handling with `validate_credentials(stored_username, stored_password)`, `login()`, and `logout()`.
- **`User(username, password, email=None)`**: extends `Login` and stores `email`.
- **`Budget()`**: simple category limits and tracking. Methods: `set_limit(category, amount)`, `add_spending(category, amount)`, `is_overspending(category)`, `total_spent()`.
- **`Survey(username, password, email=None, monthly_budget=0.0)`**: main utility for the survey and Budget Bee score.
	- `fill_expense(category, item, amount)` — programmatic way to set a single survey line.
	- `collect_expenses_cli()` — interactive CLI questionnaire to fill the survey.
	- `calculate_totals()` — returns `(total_spent, category_totals)`.
	- `compute_budget_bee_score(total_spent, monthly_budget)` — static method that maps spending to a 10–100 score.
	- `initialize_bee_score()` — computes and sets `bee_score` from current survey and `monthly_budget`.
	- `add_transaction(amount, description="")` — add an extra expense and update the `bee_score`.

**Budget Bee scoring (brief)**
- Score range: 10 (worst / heavy overspending) to 100 (best / little to no spending).
- If no monthly budget is set (<= 0), the code returns a neutral score of `50`.
- The scoring formula caps the effect of overspending at 150% of the budget and maps 0% → 100, 100% → ~40, 150% → ~10.

**Programmatic Example**
Use the `Survey` class directly in code:

```python
from banking import Survey

# Create a survey user and set a monthly budget
s = Survey(username="alice", password="secret", monthly_budget=2000.0)

# Fill a few survey items programmatically
s.fill_expense("Food", "Groceries and household supplies", 300.0)
s.fill_expense("Housing", "Rent or mortgage", 900.0)

# Compute totals and initial Budget Bee score
score, total_spent, category_totals = s.initialize_bee_score()
print("Score:", score)
print("Total:", total_spent)
print("By category:", category_totals)

# Add an extra transaction and see the score update
new_score, new_total = s.add_transaction(45.50, "coffee and snacks")
print("Updated score:", new_score)
```

**CLI Usage**
- Run: `python banking.py`.
- The CLI will:
	- Create a `Survey` instance (example user `samira` in the script).
	- Prompt the user to enter monthly expense items (press ENTER to skip items).
	- Ask for the total monthly budget.
	- Show initial totals and the Budget Bee score.
	- Allow adding extra transactions interactively and update the score.

**Notes / Implementation details**
- Input helpers include `get_float_input(prompt, allow_empty=False)` and `get_yes_no(prompt)` for robust CLI input handling.
- `FAKE_BANK` exists in the file as a static example dataset but is not required for the survey flow.

**Extending the code**
- You can integrate `Survey` into a web or GUI front end by calling `fill_expense(...)` from form handlers and using `initialize_bee_score()` and `add_transaction(...)` to keep the score up to date.

**License**
- No license file included. Use and modify as you see fit.
