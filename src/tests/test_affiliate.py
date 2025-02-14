import unittest
import numpy as np
from affiliate.src.affiliate import Affiliate
from affiliate.src.constants import INITIAL_COMMISSION_RATE, DYNAMIC_ADJUSTMENT_RATE

class TestAffiliate(unittest.TestCase):
    def setUp(self):
        self.affiliate = Affiliate(1, INITIAL_COMMISSION_RATE)

    def test_initialization(self):
        self.assertEqual(self.affiliate.affiliate_id, 1)
        self.assertEqual(self.affiliate.commission_rate, INITIAL_COMMISSION_RATE)
        self.assertEqual(self.affiliate.is_whale, False)
        self.assertTrue(np.isclose(self.affiliate.base_currency_balance, np.array(1000.0, dtype=np.float32)))
        self.assertEqual(self.affiliate.wallet, {})
        self.assertTrue(np.isclose(self.affiliate.total_referral_amount, np.array(0.0, dtype=np.float32)))
        self.assertTrue(np.isclose(self.affiliate.total_earned,  np.array(0.0, dtype=np.float32)))
        self.assertEqual(self.affiliate.earnings_history, [])
        self.assertEqual(self.affiliate.commission_rate_history, [])
        self.assertEqual(self.affiliate.recent_investment, [])
        self.assertEqual(self.affiliate.whale_investment_capacity, 0)

    def test_calculate_commission(self):
        trade_amount = 100.0
        expected_commission = trade_amount * INITIAL_COMMISSION_RATE
        commission = self.affiliate.calculate_commission(trade_amount)
        self.assertTrue(np.isclose(commission, expected_commission))

    def test_adjust_commission_dynamically_increase(self):
        self.affiliate.recent_investment = [60.0, 70.0, 80.0]
        self.affiliate.adjust_commission_dynamically(10)
        self.assertTrue(np.isclose(self.affiliate.commission_rate, INITIAL_COMMISSION_RATE + DYNAMIC_ADJUSTMENT_RATE))
        self.affiliate.commission_rate = 0.1999
        self.affiliate.adjust_commission_dynamically(10)
        self.assertTrue(np.isclose(self.affiliate.commission_rate, 0.20))

    def test_adjust_commission_dynamically_decrease(self):
        self.affiliate.recent_investment = [10.0, 20.0, 30.0]
        self.affiliate.adjust_commission_dynamically(10)
        self.assertTrue(np.isclose(self.affiliate.commission_rate, INITIAL_COMMISSION_RATE - DYNAMIC_ADJUSTMENT_RATE))
        self.affiliate.commission_rate = 0.0001
        self.affiliate.adjust_commission_dynamically(10)
        self.assertTrue(np.isclose(self.affiliate.commission_rate, 0.0))

    def test_track_referral(self):
        trade_amount = 50.0
        commission_earned = self.affiliate.calculate_commission(trade_amount)
        self.affiliate.track_referral(trade_amount)
        self.assertTrue(np.isclose(self.affiliate.total_earned, np.array(commission_earned, dtype=np.float32)))
        self.assertTrue(np.isclose(self.affiliate.total_referral_amount, np.array(trade_amount, dtype=np.float32)))

    def test_whale_initialization(self):
        whale = Affiliate(2, INITIAL_COMMISSION_RATE, is_whale=True)
        self.assertEqual(whale.affiliate_id, 2)
        self.assertTrue(whale.is_whale)
        self.assertGreater(whale.whale_investment_capacity, 5000)
        self.assertLess(whale.whale_investment_capacity, 10000)

if __name__ == '__main__':
    unittest.main()