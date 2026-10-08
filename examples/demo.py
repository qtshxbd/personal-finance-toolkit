"""Walk through the toolkit's three modules with realistic numbers."""

from finance_toolkit import (
    Budget,
    amortization_schedule,
    compare_extra_payment,
    future_value,
    growth_schedule,
    payment_amount,
    total_interest,
)


def savings_projection() -> None:
    print("== Savings: $5,000 start + $200/month at 6% for 10 years ==")
    print(f"Final balance: ${future_value(5000, 0.06, 10, contribution=200):,.2f}")
    for row in growth_schedule(5000, 0.06, 10, contribution=200)[::3]:
        print(f"  Year {row.year:>2}: ${row.end_balance:>10,.2f}  (interest ${row.interest:,.2f})")


def loan_breakdown() -> None:
    print("\n== Loan: $25,000 car loan at 7% for 5 years ==")
    schedule = amortization_schedule(25_000, 0.07, 5)
    print(f"Monthly payment: ${payment_amount(25_000, 0.07, 5):,.2f}")
    print(f"Total interest:  ${total_interest(schedule):,.2f}")
    result = compare_extra_payment(25_000, 0.07, 5, extra_payment=100)
    print(
        f"Paying $100 extra/month saves {result.payments_saved} payments "
        f"and ${result.interest_saved:,.2f} in interest"
    )


def monthly_budget() -> None:
    print("\n== Budget: $3,000/month ==")
    budget = Budget(income=3000)
    for category, limit in {"Rent": 1200, "Groceries": 400, "Transport": 150, "Fun": 200}.items():
        budget.set_limit(category, limit)
    budget.add_expense(1200, "Rent")
    budget.add_expense(310, "Groceries")
    budget.add_expense(95, "Transport")
    budget.add_expense(240, "Fun", "concert tickets")
    for row in budget.summary():
        print(f"  {row.category:<10} ${row.spent:>7,.2f} of ${row.limit:>7,.2f} ({row.percent_used:5.1f}%)")
    print(f"Over budget: {', '.join(budget.over_budget()) or 'none'}")
    print(f"Left to save: ${budget.savings():,.2f}")


if __name__ == "__main__":
    savings_projection()
    loan_breakdown()
    monthly_budget()
