import random
import datetime

CATEGORIES = ["Food", "Shopping", "Travel", "Bills", "Entertainment", "Other"]
MERCHANTS = {
    "Food": ["Chipotle", "Subway", "McDonalds", "Starbucks"],
    "Shopping": ["Target", "Walmart", "Amazon", "Best Buy"],
    "Travel": ["Uber", "Lyft", "Shell Gas"],
    "Bills": ["Verizon", "Comcast", "Electric Co", "Rent"],
    "Entertainment": ["Spotify", "Netflix", "AMC Theaters"],
    "Other": ["Misc Store", "Gym","Unknown"]
}

def generate_transaction():
    category = random.choice(CATEGORIES)
    merchant = random.choice(MERCHANTS[category])
    amount = round(random.uniform(5, 150), 2)
    date = datetime.date.today()

    return {
        "amount": amount,
        "merchant": merchant,
        "category": category,
        "date": str(date)
    }

def get_fake_transactions(n=20):
    return [generate_transaction() for _ in range(n)]
