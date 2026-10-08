# Personal Finance Toolkit

[![tests](https://github.com/qtshxbd/personal-finance-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/qtshxbd/personal-finance-toolkit/actions/workflows/tests.yml)

A pure-Python library for everyday money math: how savings grow, what a loan really costs, and where a monthly budget stands. No dependencies outside the standard library, with a pytest suite that checks results against known closed-form values.

## What's inside

| Module | Functions | What it answers |
|---|---|---|
| `interest` | `future_value`, `growth_schedule`, `continuous_future_value`, `effective_annual_rate`, `years_to_reach`, `rule_of_72` | How much will this account be worth, and when will it hit a goal? |
| `loans` | `payment_amount`, `amortization_schedule`, `total_interest`, `compare_extra_payment` | What's my payment, how much goes to interest, and what does paying extra save? |
| `budget` | `Budget`, `fifty_thirty_twenty` | How much is left in each category, and where am I over? |

## The math

**Compound growth with contributions.** With periodic rate *r* = annual rate / periods per year and *n* periods:

FV = P(1 + r)ⁿ + C · [(1 + r)ⁿ − 1] / r

Contributions made at the start of each period (an annuity due) are multiplied by an extra (1 + r).

**Loan payment.** The fixed payment that brings a balance of *P* to zero after *n* payments:

A = P · r / [1 − (1 + r)⁻ⁿ]

The amortization schedule applies this payment period by period. Each payment covers that period's interest first and the rest reduces principal. Extra payments go entirely to principal, and the final payment shrinks so the balance ends at exactly zero.

## Quick start

```bash
git clone https://github.com/qtshxbd/personal-finance-toolkit.git
cd personal-finance-toolkit
pip install -e ".[test]"
python examples/demo.py
```

```python
from finance_toolkit import future_value, compare_extra_payment, Budget

future_value(5000, 0.06, 10, contribution=200)        # 41872.85...

result = compare_extra_payment(25_000, 0.07, 5, extra_payment=100)
result.payments_saved, round(result.interest_saved, 2)  # (11, 938.99)

budget = Budget(income=3000)
budget.set_limit("Fun", 200)
budget.add_expense(240, "Fun", "concert tickets")
budget.over_budget()                                    # ['fun']
```

## Demo output

`python examples/demo.py`:

```
== Savings: $5,000 start + $200/month at 6% for 10 years ==
Final balance: $41,872.85
  Year  1: $  7,775.50  (interest $375.50)
  Year  4: $ 17,172.01  (interest $921.39)
  Year  7: $ 28,416.63  (interest $1,574.64)
  Year 10: $ 41,872.85  (interest $2,356.38)

== Loan: $25,000 car loan at 7% for 5 years ==
Monthly payment: $495.03
Total interest:  $4,701.80
Paying $100 extra/month saves 11 payments and $938.99 in interest

== Budget: $3,000/month ==
  rent       $1,200.00 of $1,200.00 (100.0%)
  groceries  $ 310.00 of $ 400.00 ( 77.5%)
  transport  $  95.00 of $ 150.00 ( 63.3%)
  fun        $ 240.00 of $ 200.00 (120.0%)
Over budget: fun
Left to save: $1,155.00
```

## Testing

```bash
pytest
```

The suite checks results against textbook values (for example, a $200,000 30-year mortgage at 6% has a $1,199.10 payment). It also checks internal consistency: the year-by-year schedule must match the closed-form formula, each loan row must balance, and principal paid must sum to the amount borrowed. Invalid inputs are tested too. GitHub Actions runs the suite on Python 3.9 through 3.12 for every push.

## Project layout

```
src/finance_toolkit/
    interest.py   compound growth, APY, time-to-goal
    loans.py      payments, amortization, extra-payment savings
    budget.py     category limits, expense tracking, 50/30/20 split
tests/            pytest suite
examples/demo.py  end-to-end walkthrough
```

## License

MIT
