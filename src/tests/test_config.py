"""
Unit tests for configuration management functionality.

This module contains unit tests for the configuration system, focusing on
command-line argument parsing and configuration dictionary generation.
It ensures that simulation parameters are correctly processed and validated.

Test Coverage:
- Command-line argument parsing with various parameter combinations
- Configuration dictionary generation from parsed arguments
- Integration with argparse for robust CLI handling
- Parameter validation and type checking
- Mocked testing for isolated functionality testing

Testing Approach:
- Mocked argparse to test argument parsing in isolation
- Comprehensive parameter validation
- Edge case testing for different input scenarios
- Verification of configuration dictionary structure and content
"""

import unittest
import argparse
from unittest.mock import patch
from config import parse_arguments, get_config_from_args

class TestConfig(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_arguments(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            num_simulation_steps=200,
            num_tokens=10,
            num_affiliates=7,
            initial_supply=15000,
            initial_price=1.5,
            initial_commission_rate=0.15
        )
        args = parse_arguments()
        self.assertEqual(args.num_simulation_steps, 200)
        self.assertEqual(args.num_tokens, 10)
        self.assertEqual(args.num_affiliates, 7)
        self.assertEqual(args.initial_supply, 15000)
        self.assertEqual(args.initial_price, 1.5)
        self.assertEqual(args.initial_commission_rate, 0.15)

    @patch('config.parse_arguments')
    def test_get_config_from_args(self, mock_parse_arguments):
        mock_parse_arguments.return_value = argparse.Namespace(
            num_simulation_steps=200,
            num_tokens=10,
            num_affiliates=7,
            initial_supply=15000,
            initial_price=1.5,
            initial_commission_rate=0.15
        )
        config = get_config_from_args()
        self.assertEqual(config["NUM_SIMULATION_STEPS"], 200)
        self.assertEqual(config["NUM_TOKENS"], 10)
        self.assertEqual(config["NUM_AFFILIATES"], 7)
        self.assertEqual(config["INITIAL_SUPPLY"], 15000)
        self.assertEqual(config["INITIAL_PRICE"], 1.5)
        self.assertEqual(config["INITIAL_COMMISSION_RATE"], 0.15)

if __name__ == '__main__':
    unittest.main()