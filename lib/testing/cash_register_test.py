#!/usr/bin/env python3

from cash_register import CashRegister
import io
import sys

class TestCashRegister:
    '''Tests for the CashRegister class'''

    def setup_method(self):
        '''Initialize CashRegister instances for tests'''
        self.cash_register = CashRegister()
        self.cash_register_with_discount = CashRegister(20)

    def reset_register_totals(self):
        '''Resets totals for both registers'''
        self.cash_register.total = 0
        self.cash_register_with_discount.total = 0

    def test_discount_attribute(self):
        '''Tests if the discount is correctly initialized'''
        assert self.cash_register.discount == 0
        assert self.cash_register_with_discount.discount == 20

    def test_total_attribute(self):
        '''Tests if the total is correctly initialized to zero'''
        assert self.cash_register.total == 0
        assert self.cash_register_with_discount.total == 0

    def test_items_attribute(self):
        '''Tests if the items list is initialized to an empty list'''
        assert self.cash_register.items == []
        assert self.cash_register_with_discount.items == []

    def test_add_item(self):
        '''Tests adding an item with default quantity of 1'''
        self.cash_register.add_item("eggs", 0.98)
        assert self.cash_register.total == 0.98
        self.reset_register_totals()

    def test_add_item_optional_quantity(self):
        '''Tests adding an item with a specified quantity'''
        self.cash_register.add_item("book", 5.00, 3)
        assert self.cash_register.total == 15.00
        self.reset_register_totals()

    def test_add_item_with_multiple_items(self):
        '''Tests adding multiple items and updates total accordingly'''
        self.cash_register.add_item("Lucky Charms", 4.5)
        assert self.cash_register.total == 4.5
        self.cash_register.add_item("Ritz Crackers", 5.0)
        assert self.cash_register.total == 9.5
        self.cash_register.add_item("Justin's Peanut Butter Cups", 2.50, 2)
        assert self.cash_register.total == 14.5
        self.reset_register_totals()

    def test_apply_discount(self):
        '''Tests applying a discount to the total'''
        self.cash_register_with_discount.add_item("macbook air", 1000)
        self.cash_register_with_discount.apply_discount()
        assert self.cash_register_with_discount.total == 800.00
        self.reset_register_totals()

    def test_apply_discount_success_message(self):
        '''Tests if success message with updated total is printed correctly'''
        captured_out = io.StringIO()
        sys.stdout = captured_out
        self.cash_register_with_discount.add_item("macbook air", 1000)
        self.cash_register_with_discount.apply_discount()
        sys.stdout = sys.__stdout__
        assert captured_out.getvalue() == "After the discount, the total comes to $800.00\n"
        self.reset_register_totals()

    def test_apply_discount_reduces_total(self):
        '''Tests if applying a discount reduces the total'''
        self.cash_register_with_discount.add_item("macbook air", 1000)
        self.cash_register_with_discount.apply_discount()
        assert self.cash_register_with_discount.total == 800.00
        self.reset_register_totals()

    def test_apply_discount_when_no_discount(self):
        '''Tests if correct message is printed when no discount is available'''
        captured_out = io.StringIO()
        sys.stdout = captured_out
        self.cash_register.apply_discount()
        sys.stdout = sys.__stdout__
        assert captured_out.getvalue() == "There is no discount to apply.\n"
        self.reset_register_totals()

    def test_items_list_without_multiples(self):
        '''Tests if items list correctly reflects added items without multiples'''
        new_register = CashRegister()
        new_register.add_item("eggs", 1.99)
        new_register.add_item("tomato", 1.76)
        assert new_register.items == ["eggs", "tomato"]

    def test_items_list_with_multiples(self):
        '''Tests if items list correctly reflects added items including multiples'''
        new_register = CashRegister()
        new_register.add_item("eggs", 1.99, 2)
        new_register.add_item("tomato", 1.76, 3)
        assert new_register.items == ["eggs", "eggs", "tomato", "tomato", "tomato"]

    def test_void_last_transaction(self):
        '''Tests if the last transaction is correctly voided'''
        self.cash_register.add_item("apple", 0.99)
        self.cash_register.add_item("tomato", 1.76)
        self.cash_register.void_last_transaction()
        assert self.cash_register.total == 0.99
        self.reset_register_totals()

    def test_void_last_transaction_with_multiples(self):
        '''Tests if voiding the last transaction works when multiple items were added'''
        self.cash_register.add_item("tomato", 1.76, 2)
        self.cash_register.void_last_transaction() 
        assert self.cash_register.total == 0.00
        self.reset_register_totals()
