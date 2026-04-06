import numpy as np
from scipy.stats import ks_2samp
import json
import logging

logger = logging.getLogger(__name__)

class DriftDetector:
    """
    Detects statistical drift between training and production data.
    Demonstrates: NumPy, SciPy (MLOps patterns), and Drift Detection.
    """
    def __init__(self, threshold=0.05):
        self.threshold = threshold # p-value threshold (standard 0.05)
        self.reference_data = None

    def set_reference(self, data):
        """Usually the data used during training"""
        self.reference_data = np.array(data)
        logger.info("Reference data loaded for drift detection.")

    def detect(self, current_data):
        """
        Uses the Kolmogorov-Smirnov test to compare distributions.
        Returns True if drift is detected.
        """
        if self.reference_data is None:
            raise ValueError("Reference data must be set before detection.")
        
        current_data = np.array(current_data)
        
        # KS Test
        statistic, p_value = ks_2samp(self.reference_data, current_data)
        
        is_drifting = p_value < self.threshold
        
        results = {
            "statistic": float(statistic),
            "p_value": float(p_value),
            "drift_detected": bool(is_drifting)
        }
        
        return results

if __name__ == "__main__":
    # Example usage
    detector = DriftDetector()
    
    # Training data (Normal distribution)
    train_data = np.random.normal(loc=0, scale=1, size=1000)
    detector.set_reference(train_data)
    
    # Case 1: Healthy production data
    prod_data_healthy = np.random.normal(loc=0.05, scale=1.05, size=1000)
    res_1 = detector.detect(prod_data_healthy)
    print(f"Healthy Set: {res_1}")
    
    # Case 2: Drifting production data (Skews older/higher)
    prod_data_drift = np.random.normal(loc=1.5, scale=1.2, size=1000)
    res_2 = detector.detect(prod_data_drift)
    print(f"Drifting Set: {res_2}")
