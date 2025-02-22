# GritHub
Sports and Healthcare Track Project for Hacklytics 2025

# Entry Point (app.py):

- It initializes and starts the FastAPI application, and includes the API routes (via the controller).
- Think of it as the “main” file that launches the backend server.
  
# Data Models (models/training_model.py):

- These are Pydantic models that define the structure of incoming requests (user input) and outgoing responses (training plan).
- They ensure data validation and serve as a contract between the API and the client.

# Controllers (controllers/training_controller.py):

- Controllers handle HTTP requests and route them to the appropriate service functions.
- They separate the presentation layer (what the client sees) from the business logic.

# Services (services/training_service.py):

- This layer contains the business logic—processing user input, generating the 10‑step training plan, and integrating the BioGears simulation.
- It acts as the “brain” of the application and is kept separate to follow the Single Responsibility Principle.

# Repositories & Utilities:

- Repositories (repositories/training_repository.py): Manage data persistence (for MVP, using an in-memory store).
- Utilities (utils/bio_gears_simulator.py): Contains helper functions, like our dummy function to simulate physiological insights via BioGears.

