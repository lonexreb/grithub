# utils/bio_gears_simulator.py

def simulate_physiology(difficulty: str) -> str:
    """
    Dummy function to simulate physiological response using BioGears.
    This function takes a difficulty level ('low', 'medium', 'high') and returns
    a simulated insight string. In production, replace this with actual BioGears API calls.
    """
    if difficulty == "low":
        return "Physiological simulation: Stable metrics, minimal strain."
    elif difficulty == "medium":
        return "Physiological simulation: Moderate strain observed, 20-minute recovery."
    elif difficulty == "high":
        return "Physiological simulation: High strain detected, 30-minute recovery recommended."
    else:
        return "No simulation data available."
