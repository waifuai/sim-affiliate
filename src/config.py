"""
Configuration management for token economy simulation.

This module handles command-line argument parsing and configuration management for
the token economy simulation. It provides a centralized way to configure simulation
parameters and makes the simulation easily customizable through command-line options.

Key Features:
- Command-line argument parsing with sensible defaults
- Configuration dictionary generation for easy parameter passing
- Integration with constants module for consistent parameter values
- Support for both programmatic and CLI-based configuration

Command Line Options:
- Simulation steps, token count, affiliate count
- Initial supply, price, and commission rate settings
- Easy extension for additional parameters
"""

import argparse
import logging
from constants import NUM_SIMULATION_STEPS, NUM_TOKENS, NUM_AFFILIATES, INITIAL_SUPPLY, INITIAL_PRICE, INITIAL_COMMISSION_RATE, INITIAL_TOKEN_INVESTMENT, bonding_curve_change_intervals, BONDING_CURVE_PARAM_CHANGE_INTERVAL
from typing import Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def parse_arguments() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="Simulate a token economy.")
    parser.add_argument(
        "--num_simulation_steps", type=int, default=100, help="Number of simulation steps."
    )
    parser.add_argument(
        "--num_tokens", type=int, default=5, help="Number of tokens to simulate."
    )
    parser.add_argument(
        "--num_affiliates", type=int, default=5, help="Number of affiliates."
    )
    parser.add_argument(
        "--initial_supply", type=int, default=10000, help="Initial token supply."
    )
    parser.add_argument(
        "--initial_price", type=float, default=1.0, help="Initial token price."
    )
    parser.add_argument(
        "--initial_commission_rate",
        type=float,
        default=0.10,
        help="Initial affiliate commission rate.",
    )
    return parser.parse_args()

def get_config_from_args() -> Dict[str, Any]:
    """Gets configuration from command line arguments."""
    args = parse_arguments()
    return {
        "NUM_SIMULATION_STEPS": args.num_simulation_steps,
        "NUM_TOKENS": args.num_tokens,
        "NUM_AFFILIATES": args.num_affiliates,
        "INITIAL_SUPPLY": args.initial_supply,
        "INITIAL_PRICE": args.initial_price,
        "INITIAL_COMMISSION_RATE": args.initial_commission_rate,
    }

if __name__ == "__main__":
    config: Dict[str, Any] = get_config_from_args()
    NUM_SIMULATION_STEPS: int = config["NUM_SIMULATION_STEPS"]
    NUM_TOKENS: int = config["NUM_TOKENS"]
    NUM_AFFILIATES: int = config["NUM_AFFILIATES"]
    INITIAL_SUPPLY: int = config["INITIAL_SUPPLY"]
    INITIAL_PRICE: float = config["INITIAL_PRICE"]
    INITIAL_COMMISSION_RATE: float = config["INITIAL_COMMISSION_RATE"]