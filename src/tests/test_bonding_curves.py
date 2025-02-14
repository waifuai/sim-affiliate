import unittest
import numpy as np
from bonding_curves import (
    linear_bonding_curve,
    exponential_bonding_curve,
    sigmoid_bonding_curve,
    root_bonding_curve,
    inverse_bonding_curve,
)

class TestBondingCurves(unittest.TestCase):
    def test_linear_bonding_curve(self):
        supply = np.array([1000], dtype=np.float32)
        price = linear_bonding_curve(supply)
        self.assertTrue(isinstance(price, np.ndarray))
        self.assertTrue(np.isclose(price, np.array([1.001], dtype=np.float32)))

        supply = np.array([0], dtype=np.float32)
        price = linear_bonding_curve(supply)
        self.assertTrue(isinstance(price, np.ndarray))
        self.assertTrue(np.isclose(price, np.array([1.0], dtype=np.float32)))

    def test_exponential_bonding_curve(self):
        supply = np.array([1000], dtype=np.float32)
        price = exponential_bonding_curve(supply)
        self.assertTrue(isinstance(price, np.ndarray))
        self.assertTrue(np.isclose(price, np.array([1.64872127], dtype=np.float32)))

        supply = np.array([0], dtype=np.float32)
        price = exponential_bonding_curve(supply)
        self.assertTrue(isinstance(price, np.ndarray))
        self.assertTrue(np.isclose(price, np.array([1.0], dtype=np.float32)))

    def test_sigmoid_bonding_curve(self):
        supply = np.array([5000], dtype=np.float32)
        price = sigmoid_bonding_curve(supply)
        self.assertTrue(isinstance(price, np.ndarray))
        self.assertTrue(np.isclose(price, np.array([5.0], dtype=np.float32)))

        supply = np.array([0], dtype=np.float32)
        price = sigmoid_bonding_curve(supply)
        self.assertTrue(isinstance(price, np.ndarray))
        self.assertTrue(np.isclose(price, np.array([10.0 / (1 + np.exp(5000 * 0.0001))], dtype=np.float32)))

    def test_root_bonding_curve(self):
        supply = np.array([10000], dtype=np.float32)
        price = root_bonding_curve(supply)
        self.assertTrue(isinstance(price, np.ndarray))
        self.assertTrue(np.isclose(price, np.array([10.0], dtype=np.float32)))

        supply = np.array([0], dtype=np.float32)
        price = root_bonding_curve(supply)
        self.assertTrue(isinstance(price, np.ndarray))
        self.assertTrue(np.isclose(price, np.array([0.0], dtype=np.float32)))

    def test_inverse_bonding_curve(self):
        supply = np.array([10000], dtype=np.float32)
        price = inverse_bonding_curve(supply)
        self.assertTrue(isinstance(price, np.ndarray))
        self.assertTrue(np.isclose(price, np.array([9.99900009e+00], dtype=np.float32)))

        supply = np.array([0], dtype=np.float32)
        price = inverse_bonding_curve(supply)
        self.assertTrue(isinstance(price, np.ndarray))
        self.assertTrue(np.isclose(price, np.array([100000.0], dtype=np.float32)))

if __name__ == '__main__':
    unittest.main()