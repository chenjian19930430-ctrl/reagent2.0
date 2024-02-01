"""Seed initial data for development."""
import json
import random
from datetime import datetime, timedelta


def generate_customers(count: int = 100) -> list:
    customers = []
    for i in range(count):
        customers.append({
            "id": f"cust_{i:04d}",
            "name": f"Customer_{i}",
            "email": f"user{i}@example.com",
            "segment": random.choice(["high_value", "active", "engaging", "cold"]),
            "engagement_score": round(random.random(), 2),
        })
    return customers


def generate_interactions(customers: list, days: int = 90) -> list:
    interactions = []
    base = datetime.utcnow() - timedelta(days=days)
    for cust in customers:
        for _ in range(random.randint(1, 20)):
            ts = base + timedelta(
                days=random.randint(0, days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            interactions.append({
                "customer_id": cust["id"],
                "type": random.choice(["page_view", "click", "purchase", "email_open"]),
                "timestamp": ts.isoformat(),
                "metadata": {},
            })
    return interactions


if __name__ == "__main__":
    customers = generate_customers()
    interactions = generate_interactions(customers)
    with open("seed_customers.json", "w") as f:
        json.dump(customers, f, indent=2)
    with open("seed_interactions.json", "w") as f:
        json.dump(interactions, f, indent=2)
    print(f"Generated {len(customers)} customers and {len(interactions)} interactions")
