import numpy as np
from .constants import (
    COMMISSION_DYNAMICS_STEP, DYNAMIC_ADJUSTMENT_RATE, MOVING_AVERAGE_WINDOW,
    INITIAL_COMMISSION_RATE, COMMISSION_RATE_MIN, COMMISSION_RATE_MAX,
    WHALE_INVESTMENT_MIN, WHALE_INVESTMENT_MAX, INVESTMENT_THRESHOLD
)
import logging
from typing import Dict, Any, List

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

class Affiliate:
    """
    Represents an affiliate in the system.
    """
    def __init__(self, affiliate_id: int, initial_commission_rate: float, is_whale: bool=False):
        """
        Initializes an affiliate.

        Args:
            affiliate_id (int): The ID of the affiliate.
            initial_commission_rate (float): The initial commission rate for the affiliate.
            is_whale (bool): Whether the affiliate is a whale (default: False).

        Raises:
            ValueError: If affiliate_id is negative or initial_commission_rate is out of bounds.
        """
        if affiliate_id < 0:
            raise ValueError("Affiliate ID cannot be negative")
        if not (COMMISSION_RATE_MIN <= initial_commission_rate <= COMMISSION_RATE_MAX):
            raise ValueError(f"Initial commission rate must be between {COMMISSION_RATE_MIN} and {COMMISSION_RATE_MAX}")

        self.affiliate_id: int = affiliate_id
        self.commission_rate: float = initial_commission_rate
        self.is_whale: bool = is_whale
        self.base_currency_balance: float = 1000.0
        self.wallet: Dict[str, float] = {}
        self.total_referral_amount: float = 0.0
        self.total_earned: float = 0.0
        self.earnings_history: List[float] = []
        self.commission_rate_history: List[float] = []
        self.recent_investment: List[float] = []  # Track recent investment amounts
        self.whale_investment_capacity: float = np.random.uniform(WHALE_INVESTMENT_MIN, WHALE_INVESTMENT_MAX) if is_whale else 0

    def adjust_commission_dynamically(self, step: int) -> None:
        """
        Adjusts the commission rate dynamically based on recent investment.

        Args:
            step (int): The current step in the simulation.
        """
        if step % COMMISSION_DYNAMICS_STEP == 0:
            avg_investment = np.mean(self.recent_investment) if self.recent_investment else 0
            if avg_investment > INVESTMENT_THRESHOLD:
                self.commission_rate += DYNAMIC_ADJUSTMENT_RATE
            else:
                self.commission_rate -= DYNAMIC_ADJUSTMENT_RATE
            self.commission_rate = max(COMMISSION_RATE_MIN, min(self.commission_rate, COMMISSION_RATE_MAX))
            logging.info(f"Affiliate {self.affiliate_id} commission rate adjusted to {self.commission_rate:.4f} based on avg investment {avg_investment:.2f}")

    def calculate_commission(self, trade_amount: float) -> float:
        """
        Calculates the commission earned on a trade.

        Args:
            trade_amount (float): The amount of the trade.

        Returns:
            float: The commission earned.
        """
        return trade_amount * self.commission_rate

    def track_referral(self, trade_amount: float) -> None:
        """
        Tracks a referral and updates the affiliate's earnings.

        Args:
            trade_amount (float): The amount of the trade.

        Raises:
            ValueError: If trade_amount is negative.
        """
        if trade_amount < 0:
            raise ValueError("Trade amount cannot be negative")

        commission_earned = self.calculate_commission(trade_amount)
        self.total_earned += commission_earned
        self.total_referral_amount += trade_amount
        logging.info(f"Affiliate {self.affiliate_id} earned commission: {commission_earned:.2f}")