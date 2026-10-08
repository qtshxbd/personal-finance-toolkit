import pytest

from finance_toolkit import Budget, fifty_thirty_twenty


@pytest.fixture
def budget():
    b = Budget(income=3000)
    b.set_limit("Rent", 1200)
    b.set_limit("Groceries", 400)
    b.set_limit("Fun", 200)
    return b


def test_spent_by_category_and_total(budget):
    budget.add_expense(120, "Groceries", "weekly shop")
    budget.add_expense(80, "Groceries")
    budget.add_expense(1200, "Rent")
    assert budget.spent("Groceries") == pytest.approx(200)
    assert budget.spent() == pytest.approx(1400)


def test_remaining(budget):
    budget.add_expense(150, "Groceries")
    assert budget.remaining("Groceries") == pytest.approx(250)


def test_category_names_are_case_insensitive(budget):
    budget.add_expense(50, "  GROCERIES ")
    assert budget.spent("groceries") == pytest.approx(50)


def test_over_budget_detection(budget):
    budget.add_expense(250, "Fun")
    budget.add_expense(100, "Groceries")
    assert budget.over_budget() == ["fun"]
    assert budget.remaining("Fun") == pytest.approx(-50)


def test_unallocated_and_savings(budget):
    budget.add_expense(1200, "Rent")
    assert budget.unallocated() == pytest.approx(3000 - 1800)
    assert budget.savings() == pytest.approx(1800)


def test_summary_reports_percent_used(budget):
    budget.add_expense(100, "Groceries")
    rows = {row.category: row for row in budget.summary()}
    assert rows["groceries"].percent_used == pytest.approx(25)
    assert rows["rent"].spent == 0
    assert set(rows) == {"rent", "groceries", "fun"}


def test_summary_handles_zero_limit():
    b = Budget(1000)
    b.set_limit("misc", 0)
    assert b.summary()[0].percent_used == 0


def test_expense_requires_existing_category(budget):
    with pytest.raises(KeyError):
        budget.add_expense(20, "Travel")


@pytest.mark.parametrize("amount", [0, -10])
def test_expense_must_be_positive(budget, amount):
    with pytest.raises(ValueError):
        budget.add_expense(amount, "Fun")


def test_invalid_budget_setup():
    with pytest.raises(ValueError):
        Budget(-1)
    b = Budget(100)
    with pytest.raises(ValueError):
        b.set_limit("food", -5)
    with pytest.raises(ValueError):
        b.set_limit("   ", 10)


def test_fifty_thirty_twenty_split():
    split = fifty_thirty_twenty(4000)
    assert split == {"needs": 2000, "wants": 1200, "savings": 800}
    assert sum(split.values()) == pytest.approx(4000)
