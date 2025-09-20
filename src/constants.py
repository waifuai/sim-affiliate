# Simulation parameters
NUM_SIMULATION_STEPS: int = 100
NUM_TOKENS: int = 5
NUM_AFFILIATES: int = 5

# Token parameters
INITIAL_SUPPLY: int = 10000
INITIAL_PRICE: float = 1.0
TRANSACTION_FEE_RATE: float = 0.0025  # 0.25% transaction fee
BURN_RATE: float = 0.0002  # 0.02% burn rate

# Affiliate parameters
INITIAL_COMMISSION_RATE: float = 0.10
AFFILIATE_STARTING_POINT: int = 0
INITIAL_BASE_CURRENCY: int = 1000
INITIAL_TOKEN_INVESTMENT: int = 10
COMMISSION_DYNAMICS_STEP: int = 10
DYNAMIC_ADJUSTMENT_RATE: float = 0.0005  # Reduced adjustment rate
MOVING_AVERAGE_WINDOW: int = 50  # Increased window for smoother price adjustments
COMMISSION_RATE_MIN: float = 0.0
COMMISSION_RATE_MAX: float = 0.20
WHALE_INVESTMENT_MIN: float = 5000
WHALE_INVESTMENT_MAX: float = 10000

# Trading parameters
BUY_PROBABILITY: float = 0.6
SELL_PROBABILITY: float = 0.05  # Reduced sell frequency
MAX_SELL_PERCENTAGE: float = 0.05  # Sell up to 5%
INVESTMENT_THRESHOLD: float = 50  # Threshold for commission adjustment

# Bonding curve parameters
PRICE_IMPACT_FACTOR: float = 0.01  # Reduced impact factor
BONDING_CURVE_TYPE_CHANGE_INTERVAL: int = 80 # Increased interval
BONDING_CURVE_PARAM_CHANGE_INTERVAL: int = 20 # Reduced interval for more frequent parameter tweaks
BONDING_CURVE_CHANGE_MIN_STEP: int = 500
BONDING_CURVE_CHANGE_MAX_STEP: int = 1000

# Variable bonding curve change intervals for each token
import numpy as np

def generate_bonding_curve_intervals(num_tokens: int, min_step: int = 500, max_step: int = 1001, seed: int = None) -> np.ndarray:
    """
    Generate random bonding curve change intervals for tokens.

    Args:
        num_tokens (int): Number of tokens.
        min_step (int): Minimum interval step.
        max_step (int): Maximum interval step.
        seed (int): Random seed for reproducibility.

    Returns:
        np.ndarray: Array of change intervals.
    """
    if seed is not None:
        np.random.seed(seed)
    return np.random.choice(range(min_step, max_step), size=num_tokens, replace=True)

# Generate bonding curve change intervals with default parameters
bonding_curve_change_intervals = generate_bonding_curve_intervals(NUM_TOKENS, BONDING_CURVE_CHANGE_MIN_STEP, BONDING_CURVE_CHANGE_MAX_STEP)