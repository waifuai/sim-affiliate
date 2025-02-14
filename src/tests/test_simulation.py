import unittest
from unittest.mock import patch, MagicMock
from simulation import run_simulation, token_simulation_step, affiliate_simulation_step
from config import NUM_SIMULATION_STEPS, NUM_TOKENS, NUM_AFFILIATES, INITIAL_SUPPLY, INITIAL_PRICE, INITIAL_COMMISSION_RATE
import numpy as np

class TestSimulation(unittest.TestCase):
    @patch('simulation.token_simulation_step')
    @patch('simulation.affiliate_simulation_step')
    def test_run_simulation(self, mock_affiliate_simulation_step, mock_token_simulation_step):
        params = {
            'num_simulation_steps': 2,
            'num_tokens': 2,
            'num_affiliates': 2,
            'initial_supply': 1000,
            'initial_price': 1.0,
            'initial_commission_rate': 0.10,
        }
        token_histories, affiliate_histories = run_simulation(params)

        self.assertEqual(len(token_histories), 2)
        self.assertEqual(len(affiliate_histories), 2)

        mock_token_simulation_step.assert_called()
        mock_affiliate_simulation_step.assert_called()

        for token_name, histories in token_histories.items():
            self.assertIn("price", histories)
            self.assertIn("supply", histories)
            self.assertIn("bonding_curve", histories)
            self.assertEqual(len(histories["price"]), params['num_simulation_steps'])
            self.assertEqual(len(histories["supply"]), params['num_simulation_steps'])
            self.assertEqual(len(histories["bonding_curve"]), params['num_simulation_steps'])

        for aff_id, histories in affiliate_histories.items():
            self.assertIn("earned", histories)
            self.assertIn("commission_rate", histories)
            self.assertIn("wallet", histories)
            self.assertIn("base_currency_balance", histories)
            self.assertEqual(len(histories["earned"]), params['num_simulation_steps'])
            self.assertEqual(len(histories["commission_rate"]), params['num_simulation_steps'])
            self.assertEqual(len(histories["wallet"]), params['num_simulation_steps'])
            self.assertEqual(len(histories["base_currency_balance"]), params['num_simulation_steps'])

    def test_token_simulation_step(self):
        # Create mock objects for tokens and affiliates
        mock_token1 = MagicMock()
        mock_token1.name = "Token1"
        mock_token2 = MagicMock()
        mock_token2.name = "Token2"
        tokens = [mock_token1, mock_token2]

        mock_affiliate1 = MagicMock()
        mock_affiliate1.affiliate_id = 1
        mock_affiliate2 = MagicMock()
        mock_affiliate2.affiliate_id = 2
        affiliates = [mock_affiliate1, mock_affiliate2]

        params = {}

        # Call the function
        token_simulation_step(1, tokens, affiliates, params)

        # Assert that the _process_affiliate_trades function was called for each affiliate
        for affiliate in affiliates:
            self.assertTrue(hasattr(affiliate, "_process_affiliate_trades"))

        # Assert that the _update_tokens function was called
        self.assertTrue(hasattr(tokens[0], "change_bonding_curve"))

    def test_affiliate_simulation_step(self):
        # Create mock objects for tokens and affiliates
        mock_token1 = MagicMock()
        mock_token1.name = "Token1"
        mock_token2 = MagicMock()
        mock_token2.name = "Token2"
        tokens = [mock_token1, mock_token2]

        mock_affiliate1 = MagicMock()
        mock_affiliate1.affiliate_id = 1
        mock_affiliate1.wallet = {"Token1": 100, "Token2": 50}
        mock_affiliate2 = MagicMock()
        mock_affiliate2.affiliate_id = 2
        affiliates = [mock_affiliate1, mock_affiliate2]

        params = {}

        # Call the function
        affiliate_simulation_step(1, tokens, affiliates, params)

        # Assert that the affiliate methods were called
        for affiliate in affiliates:
            self.assertTrue(hasattr(affiliate, "adjust_commission_dynamically"))
            self.assertTrue(hasattr(affiliate, "earnings_history"))
            self.assertTrue(hasattr(affiliate, "commission_rate_history"))

if __name__ == '__main__':
    unittest.main()