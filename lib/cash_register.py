#!/usr/bin/env python3

class CashRegister:
    def __init__(self, discount=0):
        self.total = 0
        self.discount = discount
        self.items = []
        self.last_transaction_amount = 0

    def add_item(self, title, price, quantity=1):
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number.")
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer.")
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        
        self.total += price * quantity
        self.last_transaction_amount = price * quantity
        self.items.extend([title] * quantity)

    def apply_discount(self):
        if self.discount == 0:
            print("There is no discount to apply.")
            return

        discount_amount = self.total * (self.discount / 100)
        self.total -= discount_amount
        self.discount = 0  # Reset the discount after applying
        print(f"After the discount, the total comes to ${self.total:.2f}")
        return

    def void_last_transaction(self):
        self.total -= self.last_transaction_amount
        if self.last_transaction_amount > 0:
            price = self.last_transaction_amount
            num_items_to_remove = self.items.count(price)
            for _ in range(num_items_to_remove):
                self.items.remove(price)
        self.last_transaction_amount = 0
