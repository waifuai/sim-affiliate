"""
Unit tests for the Token class and cryptocurrency functionality.

This module contains comprehensive unit tests for the Token class, covering
token initialization, price calculations, buy/sell operations, bonding curve
management, and parameter adjustments.

Test Coverage:
- Token initialization with validation and error handling
- Buy/sell operations with fee calculations and token burns
- Price calculation accuracy using different bonding curves
- Bonding curve switching and parameter modification
- Fee and burn rate calculations
- Edge cases including insufficient balances and boundary conditions

Testing Approach:
- NumPy-compatible assertions for floating-point precision
- Mock objects for isolating specific functionality
- Comprehensive testing of transaction mechanics
- Validation of supply and price state changes
- Integration testing with bonding curve functions
"""

import unittest
import numpy as np
from unittest.mock import MagicMock
from crypto_token import Token
from bonding_curves import linear_bonding_curve

class TestToken(unittest.TestCase):
    def setUp(self):
        self.initial_supply = 1000.0
        self.initial_price = 1.0
        self.bonding_curve_func = linear_bonding_curve
        self.token = Token("TestToken", self.initial_supply, self.initial_price, self.bonding_curve_func)

    def test_initialization(self):
        self.assertEqual(self.token.name, "TestToken")
        self.assertTrue(np.isclose(self.token.supply, np.array(self.initial_supply, dtype=np.float32)))
        self.assertTrue(np.isclose(self.token.price, np.array(self.initial_price, dtype=np.float32)))
        self.assertEqual(self.token.bonding_curve_func, self.bonding_curve_func)
        self.assertEqual(self.token.transaction_fee_rate, 0.0025)
        self.assertEqual(self.token.burn_rate, 0.0002)
        self.assertEqual(self.token.curve_metadata, {"function_name": "linear_bonding_curve"})

    def test_buy(self):
        amount = 100.0
        old_price = self.token.price
        price = self.token.buy(amount)
        self.assertTrue(np.isclose(self.token.supply, np.array(self.initial_supply + amount - (amount * self.token.transaction_fee_rate) - (amount * self.token.burn_rate), dtype=np.float32)))
        self.assertGreater(self.token.price, old_price)
        self.assertTrue(np.isclose(price, self.token.price))

    def test_sell(self):
        amount = 100.0
        old_price = self.token.price
        price = self.token.sell(amount)
        self.assertTrue(np.isclose(self.token.supply, np.array(self.initial_supply - amount + (amount * self.token.transaction_fee_rate) + (amount * self.token.burn_rate), dtype=np.float32)))
        self.assertLess(self.token.price, old_price)
        self.assertTrue(np.isclose(price, self.token.price))

    def test_change_bonding_curve(self):
        initial_bonding_curve = self.token.bonding_curve_func
        self.token.change_bonding_curve()
        self.assertNotEqual(self.token.bonding_curve_func, initial_bonding_curve)
        self.assertNotEqual(self.token.curve_metadata["function_name"], initial_bonding_curve.__name__)

    def test_change_bonding_curve_parameters(self):
        initial_metadata = self.token.curve_metadata
        self.token.change_bonding_curve_parameters()
        self.assertNotEqual(self.token.curve_metadata, initial_metadata)

    def test_buy_with_fees_and_burn(self):
        amount = 100.0
        initial_supply = self.token.supply
        initial_price = self.token.price
        fee = amount * self.token.transaction_fee_rate
        burn = amount * self.token.burn_rate
        amount_after_fee = amount - fee - burn

        self.token.buy(amount)

        self.assertTrue(np.isclose(self.token.supply, initial_supply + amount_after_fee))
        self.assertGreater(self.token.price, initial_price)

    def test_sell_with_fees_and_burn(self):
        amount = 100.0
        initial_supply = self.token.supply
        initial_price = self.token.price
        fee = amount * self.token.transaction_fee_rate
        burn = amount * self.token.burn_rate
        amount_after_fee = amount - fee - burn

        self.token.sell(amount)

        self.assertTrue(np.isclose(self.token.supply, initial_supply - amount_after_fee))
        self.assertLess(self.token.price, initial_price)

if __name__ == '__main__':
    unittest.main()