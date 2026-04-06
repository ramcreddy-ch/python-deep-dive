import time
import random
import logging
from prometheus_client import start_http_server, Gauge, Counter

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Metrics
MODEL_PREDICTIONS = Counter('ml_model_predictions_total', 'Total number of predictions')
MODEL_LATENCY = Gauge('ml_model_latency_seconds', 'Model inference latency')
MODEL_ACCURACY = Gauge('ml_model_accuracy_score', 'Real-time model accuracy estimate')

def simulate_inference():
    """
    Simulates a production ML inference loop with Prometheus metrics.
    Demonstrates: Prometheus client, Monitoring, and SRE patterns.
    """
    logger.info("ML Model Monitoring Started on port 8001...")
    start_http_server(8001)

    while True:
        # Increment prediction count
        MODEL_PREDICTIONS.inc()
        
        # Simulate latency
        latency = random.uniform(0.05, 0.4)
        MODEL_LATENCY.set(latency)
        
        # Simulate accuracy (drifting slightly over time)
        accuracy = 0.95 - (random.random() * 0.1)
        MODEL_ACCURACY.set(accuracy)
        
        if accuracy < 0.90:
            logger.warning(f"CRITICAL: Model accuracy dropped to {accuracy:.2f}")

        time.sleep(2)

if __name__ == "__main__":
    # simulate_inference()
    print("ML Monitoring Example ready. Exposes metrics on port 8001.")
