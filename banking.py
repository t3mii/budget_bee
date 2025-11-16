FAKE_BANK = [
    {"amount": 12.75, "merchant": "Chipotle",    "category": "Food",          "date": "2025-11-01"},
    {"amount": 8.50,  "merchant": "Subway",      "category": "Food",          "date": "2025-11-03"},
    {"amount": 5.25,  "merchant": "Starbucks",   "category": "Food",          "date": "2025-11-04"},

    {"amount": 45.99, "merchant": "Target",      "category": "Shopping",      "date": "2025-11-02"},
    {"amount": 27.49, "merchant": "Amazon",      "category": "Shopping",      "date": "2025-11-05"},
    {"amount": 60.00, "merchant": "Walmart",     "category": "Shopping",      "date": "2025-11-07"},

    {"amount": 18.20, "merchant": "Uber",        "category": "Transportation","date": "2025-11-03"},
    {"amount": 14.75, "merchant": "Lyft",        "category": "Transportation","date": "2025-11-06"},
    {"amount": 35.00, "merchant": "Shell Gas",   "category": "Transportation","date": "2025-11-09"},

    {"amount": 65.00, "merchant": "Verizon",     "category": "Bills",         "date": "2025-11-01"},
    {"amount": 90.00, "merchant": "Comcast",     "category": "Bills",         "date": "2025-11-01"},
    {"amount": 120.00,"merchant": "Electric Co", "category": "Bills",         "date": "2025-11-08"},

    {"amount": 10.99, "merchant": "Spotify",     "category": "Entertainment", "date": "2025-11-02"},
    {"amount": 15.49, "merchant": "Netflix",     "category": "Entertainment", "date": "2025-11-04"},
    {"amount": 22.00, "merchant": "AMC Theaters","category": "Entertainment", "date": "2025-11-10"},

    {"amount": 30.00, "merchant": "Gym",         "category": "Other",         "date": "2025-11-05"},
    {"amount": 12.00, "merchant": "Misc Store",  "category": "Other",         "date": "2025-11-06"},
]


def get_float_input(prompt, allow_empty=False):
    """
    Ask the user for a number.
    - Keeps asking until the user enters a valid float.
    - If allow_empty=True and user hits ENTER, returns None.
    """
    while True:
        value = input(prompt).strip()

        if allow_empty and value == "":
            return None
        
        try:
            return float(value)
        except ValueError:
            print(" Invalid input. Please enter a number.")


def get_yes_no(prompt):
    """
    Ask a yes/no question.
    Returns True for yes, False for no.
    """
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("  ❌ Please type 'y' or 'n'.")



class Login:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_logged_in = False
    
    def validate_credentials(self, stored_username, stored_password):
        """
        Validate if the provided credentials match the stored credentials.
        """
        if self.username == stored_username and self.password == stored_password:
            self.is_logged_in = True
            return True
        return False
    
    def login(self):
        """
        Attempt to log in.
        """
        print(f"Attempting login for user: {self.username}")
        return self.is_logged_in
    
    def logout(self):
        """Log out the user."""
        self.is_logged_in = False
        print(f"User {self.username} logged out successfully.")


class User(Login):
    """Extended user class that inherits from Login."""
    
    def __init__(self, username, password, email=None):
        """Initialize user with additional information."""
        super().__init__(username, password)
        self.email = email


class Budget:
    def __init__(self):
        self.limits = {}
        self.spending = {}

    def set_limit(self, category, amount):
        self.limits[category] = float(amount)

    def add_spending(self, category, amount):
        self.spending[category] = self.spending.get(category, 0.0) + float(amount)

    def is_overspending(self, category):
        return self.spending.get(category, 0.0) > self.limits.get(category, float('inf'))

    def total_spent(self):
        return sum(self.spending.values())


class Survey(User):
    """
    Survey class:
    - Inherits from User (so it also has login info)
    - Stores monthly expense answers in a nested dict
    - Computes total expenses
    - Maintains a Budget Bee score that updates after each transaction
    """
    def __init__(self, username, password, email=None, monthly_budget=0.0):
        super().__init__(username, password, email)
        self.monthly_budget = float(monthly_budget)
        self.expenses = self._init_expense_structure()
        self.extra_transactions = [] 
        self.bee_score = None

    def _init_expense_structure(self):
        """Initialize the questionnaire structure."""
        return {
            "Housing": {
                "Rent or mortgage": 0.0,
                "Insurance (home, car, etc)": 0.0,
                "Utilities (Gas, Electric, Water, etc)": 0.0,
                "Internet and phone": 0.0,
                "Other housing expenses": 0.0,
            },
            "Food": {
                "Groceries and household supplies": 0.0,
                "Eating out / food delivery": 0.0,
                "Other food expenses": 0.0,
            },
            "Transportation": {
                "Public transportation": 0.0,
                "Taxis / rideshares": 0.0,
                "Gas for cars": 0.0,
                "Parking and tolls": 0.0,
                "Car maintenance": 0.0,
                "Car insurance": 0.0,
                "Car payment": 0.0,
                "Other transportation expenses": 0.0,
            },
            "Health": {
                "Health insurance": 0.0,
                "Prescriptions": 0.0,
                "Doctor co-pays": 0.0,
                "Other health expenses": 0.0,
            },
            "Personal and family": {
                "Childcare": 0.0,
                "Child support you pay": 0.0,
                "Money you send to family": 0.0,
            }
        }

    # ---------- Expense collection / aggregation ---------- #

    def fill_expense(self, category, item, amount):
        """
        Programmatic way to fill one line of the survey.
        (Useful if your UI is not CLI.)
        """
        if category in self.expenses and item in self.expenses[category]:
            self.expenses[category][item] = float(amount)
        else:
            raise KeyError(f"Unknown category/item: {category} / {item}")

    def collect_expenses_cli(self):
        """
        Simple CLI-based questionnaire for testing.
        """
        print("\nEnter your expenses for THIS month.")
        print("(Press ENTER for any item you want to skip)\n")

        for category, items in self.expenses.items():
            print(f"\n--- {category} ---")
            for item in items:
                value = get_float_input(f"{item}: ", allow_empty=True)
                self.expenses[category][item] = value if value is not None else 0.0

    def calculate_totals(self):
        """
        Returns:
            total_spent (float),
            category_totals (dict: category -> float)
        """
        category_totals = {}
        total_spent = 0.0

        for category, items in self.expenses.items():
            cat_sum = sum(items.values())
            category_totals[category] = cat_sum
            total_spent += cat_sum

        return total_spent, category_totals

    # ---------- Budget Bee score logic ---------- #

    @staticmethod
    def compute_budget_bee_score(total_spent, monthly_budget):
        """
        Returns a score between 10 and 100.

        - 100 = spent almost nothing
        - ~70-90 = under budget, doing well
        - ~40-69 = getting close to budget
        - 10-39 = overspending zone
        """
        if monthly_budget <= 0:
            return 50  # neutral score if no budget set

        ratio = total_spent / monthly_budget  # e.g. 0.5 = 50% of budget
        ratio = min(ratio, 1.5)               # cap overspending effect at 150%

        # ratio = 0   → score = 100
        # ratio = 1   → score = 40
        # ratio = 1.5 → score = 10
        score = 100 - (ratio * 60)
        score = max(10, min(100, int(round(score))))
        return score

    def initialize_bee_score(self):
        """
        Call this after initial survey is filled and monthly_budget is set.
        Includes existing extra transactions (e.g. fake bank history).
        """
        base_spent, category_totals = self.calculate_totals()

        # Include all extra transactions (e.g. from FAKE_BANK)
        extra_spent = sum(t["amount"] for t in self.extra_transactions)
        current_total = base_spent + extra_spent

        score = self.compute_budget_bee_score(current_total, self.monthly_budget)
        self.bee_score = score
        return score, current_total, category_totals

    def add_transaction(self, amount, description=""):
        """
        Add a new transaction (positive number for expense) and update the score.
        """
        amount = float(amount)
        if amount < 0:
            raise ValueError("Use positive numbers for expenses.")

        self.extra_transactions.append({
            "amount": amount,
            "description": description
        })

        # Recompute total spent this month = survey base + extra
        base_spent, _ = self.calculate_totals()
        extra_spent = sum(t["amount"] for t in self.extra_transactions)
        current_total = base_spent + extra_spent

        self.bee_score = self.compute_budget_bee_score(
            current_total,
            self.monthly_budget
        )

        return self.bee_score, current_total


# ---------------- Example test run (CLI) ---------------- #


if __name__ == "__main__":

    # Ask the user for login info (ANY login is accepted)
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Create the Survey user with the provided login info
    s = Survey(username=username, password=password, email=None, monthly_budget=0.0)

    # Automatically accept login
    s.is_logged_in = True
    print("\nLogin successful.\n")

    # Load the fake bank transactions into the account automatically
    for tx in FAKE_BANK:
        s.extra_transactions.append({
            "amount": tx["amount"],
            "description": f"{tx['merchant']} ({tx['category']}) on {tx['date']}"
        })

    # Collect initial survey answers in CLI mode
    s.collect_expenses_cli()

    # Ask for monthly budget with validation
    s.monthly_budget = get_float_input("\nWhat is your TOTAL monthly budget: $")

    # Initialize Budget Bee score from the survey + fake bank
    # Calculate the final Budget Bee score (the only score)
    score, total_spent, cat_totals = s.initialize_bee_score()

    print("\nYour monthly spending summary:")
    for cat, amt in cat_totals.items():
        print(f"  {cat}: ₹{amt:.2f}")

    print(f"\nTotal spent this month (survey + bank transactions): ${total_spent:.2f}")
    print(f"Your Budget Bee Score: {score}\n")

    s.logout()
