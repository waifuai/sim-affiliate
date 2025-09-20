"""
Bonding curve implementations for token price calculations.

This module provides various mathematical bonding curve functions that determine how
token prices change based on supply. These curves are essential for simulating different
token economy behaviors and price dynamics.

Available Bonding Curves:
- Linear: Price increases linearly with supply (constant slope)
- Exponential: Price grows exponentially with supply (rapid price increase)
- Sigmoid: Price follows an S-curve with upper bound (logistic growth)
- Root: Price increases with square root of supply (diminishing returns)
- Inverse: Price decreases as supply increases (deflationary)

Key Features:
- NumPy-compatible implementations for efficient vectorized calculations
- Parameter validation and error handling for robustness
- Configurable parameters for each curve type
- Collection of all curves for easy integration with token systems
"""

import numpy as np
from typing import Callable, List
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Bonding Curve Functions (Numpy Compatible) ---

def linear_bonding_curve(supply: np.ndarray, m: float=0.001, b: float=1) -> np.ndarray:
    """
    Calculates the price using a linear bonding curve.

    Args:
        supply (np.ndarray): The current supply.
        m (float): The slope of the line.
        b (float): The y-intercept of the line.

    Returns:
        np.ndarray: The price.

    Raises:
        ValueError: If supply is negative.
    """
    if np.any(supply < 0):
        raise ValueError("Supply cannot be negative")
    return np.array(m, dtype=np.float32) * np.array(supply, dtype=np.float32) + np.array(b, dtype=np.float32)

def exponential_bonding_curve(supply: np.ndarray, a: float=1, k: float=0.0005) -> np.ndarray:
    """
    Calculates the price using an exponential bonding curve.

    Args:
        supply (np.ndarray): The current supply.
        a (float): The scaling factor.
        k (float): The exponent coefficient.

    Returns:
        np.ndarray: The price.

    Raises:
        ValueError: If supply is negative or if k is too large causing overflow.
    """
    if np.any(supply < 0):
        raise ValueError("Supply cannot be negative")
    if abs(k) > 0.01:  # Prevent potential overflow
        raise ValueError("k coefficient is too large, may cause overflow")
    return np.array(a, dtype=np.float32) * np.exp(np.array(k, dtype=np.float32) * np.array(supply, dtype=np.float32))

def sigmoid_bonding_curve(supply: np.ndarray, K: float=10, k: float=0.0001, S0: float=5000) -> np.ndarray:
    """
    Calculates the price using a sigmoid bonding curve.

    Args:
        supply (np.ndarray): The current supply.
        K (float): The maximum price.
        k (float): The steepness of the curve.
        S0 (float): The supply at the midpoint of the curve.

    Returns:
        np.ndarray: The price.

    Raises:
        ValueError: If supply is negative, K is non-positive, or k is non-positive.
    """
    if np.any(supply < 0):
        raise ValueError("Supply cannot be negative")
    if K <= 0:
        raise ValueError("K (maximum price) must be positive")
    if k <= 0:
        raise ValueError("k (steepness) must be positive")
    return np.array(K, dtype=np.float32) / (
        1
        + np.exp(
            -np.array(k, dtype=np.float32)
            * (np.array(supply, dtype=np.float32) - np.array(S0, dtype=np.float32))
        )
    )

def root_bonding_curve(supply: np.ndarray, k: float=0.1) -> np.ndarray:
    """
    Calculates the price using a root bonding curve.

    Args:
        supply (np.ndarray): The current supply.
        k (float): The scaling factor.

    Returns:
        np.ndarray: The price.

    Raises:
        ValueError: If supply is negative.
    """
    if np.any(supply < 0):
        raise ValueError("Supply cannot be negative")
    return np.sqrt(np.array(supply, dtype=np.float32)) * np.array(k, dtype=np.float32)

def inverse_bonding_curve(supply: np.ndarray, k: float=100000) -> np.ndarray:
    """
    Calculates the price using an inverse bonding curve.

    Args:
        supply (np.ndarray): The current supply.
        k (float): The scaling factor.

    Returns:
        np.ndarray: The price.

    Raises:
        ValueError: If supply is negative or k is non-positive.
    """
    if np.any(supply < 0):
        raise ValueError("Supply cannot be negative")
    if k <= 0:
        raise ValueError("k (scaling factor) must be positive")
    return np.array(k, dtype=np.float32) / (np.array(supply, dtype=np.float32) + 1)

bonding_curve_functions: List[Callable[[np.ndarray, float, float], np.ndarray]] = [
    linear_bonding_curve,
    exponential_bonding_curve,
    sigmoid_bonding_curve,
    root_bonding_curve,
    inverse_bonding_curve,
]