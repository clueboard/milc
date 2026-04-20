# CODESTYLE.md: Functional-Procedural Programming (FPP)

## Philosophy: Optimize for the Reader
Code is read far more often than it is written. In the era of AI-generated code, the human's role has shifted from **Writer** to **Auditor**. This style is designed to reduce cognitive load, eliminate "magic," and make logic immediately scannable.

---

## 1. Architecture: Functions over Classes
* **Functions First:** Default to top-level functions. 
* **The "Two-Method" Rule:** Do not create a class if it only contains `__init__` and one other method. Use a function instead.
* **State Mutation:** Use classes only when they provide unique advantages, such as storing and mutating state over time.
* **The Pythonic Singleton:** Use modules to organize related logic and state rather than implementing Singleton classes.

## 2. Function Anatomy (The "Manifest" Pattern)
Every function should follow a strict vertical rhythm to ensure the "Eye-Track" can scan it effectively.

### A. The Manifest (Variables)
* Group all variable declarations and initial assignments at the very top of the function.
* Treat this as a "Table of Contents" for what the function will handle.
* **Constraint:** Do not declare new variables in the middle of a logic block. If you need a new variable, "check it in" at the top.

### B. Vertical Rhythm (Spacing)
* **The Gap:** Use a single blank line to separate variable assignments from business logic.
* **Blocks**:
    * **Block Starters:** Place a single blank line *above* every block starter (`if`, `for`, `try`, `while`, `with`).
    * **Block Continuers:** Place a single blank line *above* every block continuer (`elif`, `else`, `except`, `finally`) except when the overall block structure is fewer than 6 lines. 
    * **Exceptions To The Block Rules**: Do not insert a blank line between two block starters. IE, use 'if foo:\n    for line in...' not 'if foo:\n\n    for line in...'.
* **The Exit:** Place a single blank line before the `raise` or `return` statement(s) to make it stand out.
  * *Exception:* A blank line is not required if it is the only line inside a block (e.g., inside a guard clause).

## 3. Control Flow: The "Bouncer" Pattern
* **Early Returns:** Use guard clauses to handle edge cases, invalid inputs, or errors immediately.
* **Flat Logic:** Avoid deep nesting. By "bouncing" invalid cases early, the "happy path" of your logic should remain at the lowest level of indentation.
* **Multiple Returns:** Reject the "Single Return" pattern. Return as soon as the function's execution is logically complete.

## 4. No Magic (Anti-Abstraction)
* **Explicit Over Implicit:** Prefer standard `__init__` methods over `@dataclass` or other framework-specific decorators that hide internal mechanics.
* **Standard Types:** Prefer dictionaries, tuples, or simple classes for data structures. 
* **Transparent Logic:** If the logic cannot be followed without prior knowledge of a specific framework's "hidden" behaviors, it should be refactored into explicit Python code.

---

## Example Implementation

```python
def calculate_final_invoice(user_id, items, discount_code):
    # --- THE MANIFEST ---
    user_profile = fetch_user(user_id)
    base_total = sum(item.price for item in items)
    tax_rate = 0.08
    final_amount = 0

    # --- THE BOUNCER (Guard Clauses) ---
    if not items:
        return 0

    if user_profile.is_suspended:
        raise ValueError("Cannot invoice suspended account")

    # --- BUSINESS LOGIC ---
    if discount_code:
        base_total = apply_discount(base_total, discount_code)

    final_amount = base_total * (1 + tax_rate)

    return round(final_amount, 2)
