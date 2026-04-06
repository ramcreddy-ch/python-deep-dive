from kubernetes import client, config, watch
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_pods(namespace='default'):
    """
    Monitors Pod events in a given namespace.
    Demonstrates: Kubernetes Python Client, In-cluster Auth, and Watches.
    """
    try:
        # Load config from incluster or local kubeconfig
        if "KUBERNETES_SERVICE_HOST" in os.environ:
            config.load_incluster_config()
        else:
            config.load_kube_config()
            
        v1 = client.CoreV1Api()
        w = watch.Watch()
        
        logger.info(f"Monitoring Pods in namespace: {namespace}")
        
        # Stream events
        for event in w.stream(v1.list_namespaced_pod, namespace):
            pod = event['object']
            event_type = event['type']
            
            # Simple health logic
            status = pod.status.phase
            if status == 'Failed' or status == 'Unknown':
                logger.error(f"ALERT: Pod {pod.metadata.name} is in state {status}!")
            else:
                logger.info(f"Event: {event_type} | Pod: {pod.metadata.name} | Status: {status}")

    except Exception as e:
        logger.error(f"Error connecting to Kubernetes: {e}")

if __name__ == "__main__":
    # monitor_pods()
    print("Kubernetes monitoring script initialized. Requires access to a K8s cluster.")
