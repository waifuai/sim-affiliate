import numpy as np
import logging
from .bonding_curves import bonding_curve_functions
from .constants import TRANSACTION_FEE_RATE, BURN_RATE
from typing import Callable, Dict, Any

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

class Token:
    """
    Represents a cryptocurrency token with a bonding curve.
    """
    def __init__(self, name: str, initial_supply: float, initial_price: float, bonding_curve_func: Callable[[np.ndarray], np.ndarray]):
        """
        Initializes a token.

        Args:
            name (str): The name of the token.
            initial_supply (float): The initial supply of the token.
            initial_price (float): The initial price of the token.
            bonding_curve_func (Callable[[np.ndarray], np.ndarray]): The bonding curve function for the token.

        Raises:
            ValueError: If initial_supply or initial_price are negative.
        """
        if initial_supply < 0:
            raise ValueError("Initial supply cannot be negative")
        if initial_price < 0:
            raise ValueError("Initial price cannot be negative")

        self.name: str = name
        self.supply: np.ndarray = np.array(initial_supply, dtype=np.float32)
        self.price: np.ndarray = np.array(initial_price, dtype=np.float32)
        self.bonding_curve_func: Callable[[np.ndarray], np.ndarray] = bonding_curve_func
        self.transaction_fee_rate: float = TRANSACTION_FEE_RATE
        self.burn_rate: float = BURN_RATE
        self.curve_metadata: Dict[str, Any] = {"function_name": bonding_curve_func.__name__}

    def calculate_price(self) -> np.ndarray:
        """Calculates the price of the token based on the bonding curve."""
        return self.bonding_curve_func(self.supply)

    def buy(self, amount: float) -> float:
        """
        Buys a certain amount of the token.

        Args:
            amount (float): The amount of the token to buy.

        Returns:
            float: The new price of the token.

        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Buy amount must be positive")

        fee = amount * self.transaction_fee_rate
        burn = amount * self.burn_rate
        amount_after_fee = amount - fee - burn

        if amount_after_fee <= 0:
            logging.warning(f"Buy amount too small after fees and burn for {self.name}. No tokens purchased.")
            return float(self.price)

        old_price = float(self.price)
        self.supply += np.array(amount_after_fee, dtype=np.float32)
        self.price = self.calculate_price()
        price_change = float(self.price) - old_price

        logging.info(
            f"Token {self.name} price updated from {old_price:.2f} to {float(self.price):.2f} (+{price_change:.2f}). Supply increased to {float(self.supply):.2f}"
        )
        return float(self.price)

    def sell(self, amount: float) -> float:
        """
        Sells a certain amount of the token.

        Args:
            amount (float): The amount of the token to sell.

        Returns:
            float: The new price of the token.

        Raises:
            ValueError: If amount is not positive or exceeds supply.
        """
        if amount <= 0:
            raise ValueError("Sell amount must be positive")
        if amount > float(self.supply):
            raise ValueError(f"Sell amount ({amount}) cannot exceed current supply ({float(self.supply)})")

        fee = amount * self.transaction_fee_rate
        burn = amount * self.burn_rate
        amount_after_fee = amount - fee - burn

        if amount_after_fee <= 0:
            logging.warning(f"Sell amount too small after fees and burn for {self.name}. No tokens sold.")
            return float(self.price)

        old_price = float(self.price)
        self.supply -= np.array(amount_after_fee, dtype=np.float32)
        self.price = self.calculate_price()
        price_change = old_price - float(self.price)

        logging.info(
            f"Token {self.name} price updated from {old_price:.2f} to {float(self.price):.2f} (-{price_change:.2f}). Supply decreased to {float(self.supply):.2f}"
        )
        return float(self.price)
    
    def change_bonding_curve(self) -> None:
        """Changes the bonding curve function of the token."""
        current_curve_index = bonding_curve_functions.index(self.bonding_curve_func)
        next_curve_index = (current_curve_index + 1) % len(bonding_curve_functions)
        self.bonding_curve_func = bonding_curve_functions[next_curve_index]
        self.curve_metadata = {"function_name": self.bonding_curve_func.__name__}
        logging.info(f"Token {self.name} bonding curve changed to {self.bonding_curve_func.__name__}")

    def change_bonding_curve_parameters(self) -> None:
        """Changes the parameters of the bonding curve function."""
        if self.bonding_curve_func.__name__ == "linear_bonding_curve":
            self.bonding_curve_func = lambda supply: bonding_curve_functions[0](supply, m=np.random.uniform(0.0005, 0.002), b=np.random.uniform(0.5, 1.5))
            self.curve_metadata = {"function_name": "linear_bonding_curve", "params": {"m": "dynamic", "b": "dynamic"}}
        elif self.bonding_curve_func.__name__ == "exponential_bonding_curve":
            self.bonding_curve_func = lambda supply: bonding_curve_functions[1](supply, a=np.random.uniform(0.8, 1.2), k=np.random.uniform(0.0004, 0.0006))
            self.curve_metadata = {"function_name": "exponential_bonding_curve", "params": {"a": "dynamic", "k": "dynamic"}}
        elif self.bonding_curve_func.__name__ == "sigmoid_bonding_curve":
            self.bonding_curve_func = lambda supply: bonding_curve_functions[2](supply, K=np.random.uniform(8, 12), k=np.random.uniform(0.00008, 0.00012), S0=np.random.uniform(4000, 6000))
            self.curve_metadata = {"function_name": "sigmoid_bonding_curve", "params": {"K": "dynamic", "k": "dynamic", "S0": "dynamic"}}
        elif self.bonding_curve_func.__name__ == "root_bonding_curve":
            self.bonding_curve_func = lambda supply: bonding_curve_functions[3](supply, k=np.random.uniform(0.08, 0.12))
            self.curve_metadata = {"function_name": "root_bonding_curve", "params": {"k": "dynamic"}}
        elif self.bonding_curve_func.__name__ == "inverse_bonding_curve":
            self.bonding_curve_func = lambda supply: bonding_curve_functions[4](supply, k=np.random.uniform(80000, 120000))
            self.curve_metadata = {"function_name": "inverse_bonding_curve", "params": {"k": "dynamic"}}
        logging.info(f"Token {self.name} bonding curve parameters changed for {self.curve_metadata['function_name']}")