# utils/bio_gears_simulator.py
def simulate_physiology(training_intensity: str) -> str:
    """
    Dummy function to simulate physiological response.
    In a real integration, you would call BioGears engine functions.
    """
    insights = {
        "low": "Simulated heart rate remains stable. Recovery time: 10 minutes.",
        "medium": "Moderate increase in heart rate. Recovery time: 20 minutes.",
        "high": "Significant stress observed. Recovery time: 30 minutes.",
    }
    return insights.get(training_intensity, "No simulation available.")
