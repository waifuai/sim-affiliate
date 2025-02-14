import unittest
from unittest.mock import patch
import io
import sys
from affiliate.src.main import main

class TestMain(unittest.TestCase):
    @patch('affiliate.src.main.run_simulation')
    def test_main(self, mock_run_simulation):
        # Mock the return value of run_simulation
        mock_run_simulation.return_value = (
            {
                "Token_0": {
                    "price": [1.1, 1.2],
                    "supply": [1000.0, 1100.0],
                    "bonding_curve": ["linear_bonding_curve", "exponential_bonding_curve"],
                }
            },
            {
                0: {
                    "earned": [10.0, 11.0],
                    "commission_rate": [0.1, 0.11],
                    "wallet": [{"Token_0": 100.0}, {"Token_0": 110.0}],
                    "base_currency_balance": [900.0, 800.0],
                }
            },
        )

        # Capture the printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the main function
        main()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Assert that the summary is printed
        output = captured_output.getvalue()
        self.assertIn("--- Token Summary ---", output)
        self.assertIn("Token: Token_0", output)
        self.assertIn("Final Price: 1.20", output)
        self.assertIn("Final Supply: 1100.00", output)
        self.assertIn("Final Bonding Curve: exponential_bonding_curve", output)
        self.assertIn("--- Affiliate Summary ---", output)
        self.assertIn("Affiliate: 0", output)
        self.assertIn("Final Base Currency: 800.00", output)
        self.assertIn("Final Commission Rate: 0.1100", output)

if __name__ == '__main__':
    unittest.main()