"""Category-based budgeting: set spending limits, log expenses, and track what's left."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Expense:
    amount: float
    category: str
    description: str = ""


@dataclass(frozen=True)
class CategorySummary:
    category: str
    limit: float
    spent: float
    remaining: float
    percent_used: float


def _normalize(category: str) -> str:
    name = category.strip().lower()
    if not name:
        raise ValueError("category name cannot be empty")
    return name


class Budget:
    """A monthly budget built from an income and per-category spending limits."""

    def __init__(self, income: float) -> None:
        if income < 0:
            raise ValueError("income must be non-negative")
        self.income = income
        self._limits: dict[str, float] = {}
        self._expenses: list[Expense] = []

    def set_limit(self, category: str, amount: float) -> None:
        if amount < 0:
            raise ValueError("limit must be non-negative")
        self._limits[_normalize(category)] = amount

    def add_expense(self, amount: float, category: str, description: str = "") -> Expense:
        if amount <= 0:
            raise ValueError("expense amount must be positive")
        name = _normalize(category)
        if name not in self._limits:
            raise KeyError(f"no limit set for category '{name}'; call set_limit first")
        expense = Expense(amount, name, description)
        self._expenses.append(expense)
        return expense

    @property
    def categories(self) -> list[str]:
        return list(self._limits)

    @property
    def expenses(self) -> list[Expense]:
        return list(self._expenses)

    def spent(self, category: str | None = None) -> float:
        """Total spent in one category, or across all categories if none is given."""
        if category is None:
            return sum(e.amount for e in self._expenses)
        name = _normalize(category)
        return sum(e.amount for e in self._expenses if e.category == name)

    def remaining(self, category: str) -> float:
        """Amount left in a category's limit (negative when over budget)."""
        name = _normalize(category)
        if name not in self._limits:
            raise KeyError(f"no limit set for category '{name}'")
        return self._limits[name] - self.spent(name)

    def over_budget(self) -> list[str]:
        """Categories where spending has exceeded the limit."""
        return [c for c in self._limits if self.remaining(c) < 0]

    def unallocated(self) -> float:
        """Income not yet assigned to any category limit."""
        return self.income - sum(self._limits.values())

    def savings(self) -> float:
        """Income left after all logged expenses."""
        return self.income - self.spent()

    def summary(self) -> list[CategorySummary]:
        rows = []
        for category, limit in self._limits.items():
            spent = self.spent(category)
            percent = (spent / limit * 100) if limit else 0.0
            rows.append(CategorySummary(category, limit, spent, limit - spent, percent))
        return rows


def fifty_thirty_twenty(income: float) -> dict[str, float]:
    """Split income using the 50/30/20 rule: needs, wants, and savings."""
    if income < 0:
        raise ValueError("income must be non-negative")
    return {"needs": income * 0.50, "wants": income * 0.30, "savings": income * 0.20}
