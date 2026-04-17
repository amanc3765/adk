# DevRel Agent Design

This document outlines the design for a Developer Relations (DevRel) Agent aimed at testing Android libraries and finding issues by building sample applications.

## Role & Primary Task
The agent acts as a DevRel Engineer. Its primary task is to take a target Android library, explore its APIs, and attempt to build a comprehensive sample app that utilizes all possible features to uncover edge cases or bugs.

## Inputs
*   **Target Library**: The specific Android library to be tested (e.g., a Jetpack library).

## Architecture & Components

The system is designed with a 3-level hierarchy of agents.

### Level 3: Top Manager
#### Main Orchestrator
*   **Purpose**: To oversee the entire process, coordinate between knowledge and implementation phases, and interact with the user for final feedback.
*   **Functionality**: Manages Level 2 agents (Knowledge Agent, Android Developer Manager, and Issue Resolution Manager).

### Level 2: Manager Agents
#### Knowledge Agent
*   **Purpose**: To act as a single point of contact for any kind of knowledge.
*   **Functionality**: Interfaces with the leaf agents (1, 2, 3) to gather information from documentation and code.

#### Android Developer Manager
*   **Purpose**: To manage the coding and design process.
*   **Functionality**: Interfaces with the leaf agents (4, 5, 6) to produce the sample app architecture and code.

#### Issue Resolution Manager
*   **Purpose**: To manage the feedback and issue reporting process.
*   **Functionality**: Interfaces with the leaf agents (7, 8) to document issues and file bugs.

### Level 1: Leaf Agents
These are the agents that perform specific, localized tasks.

#### 1. Reference Docs Explorer
*   **Purpose**: To understand the available APIs, their signatures, and intended usage.
*   **Functionality**: Reads and parses API reference documentation for the target library.

#### 2. Implementation Fetcher (GitHub)
*   **Purpose**: To inspect the actual source code of the library when documentation is insufficient or to understand internal behavior.
*   **Functionality**: Fetches specific source files or snippets from the library's GitHub repository.

#### 3. Documentation Reader
*   **Purpose**: To understand integration guides, best practices, and high-level concepts.
*   **Functionality**: Reads guides, tutorials, and readmes associated with the library.

#### 4. API Lister
*   **Purpose**: To read reference documentation and create a comprehensive list of all public APIs to be tested.
*   **Functionality**: Focuses specifically on extracting API signatures and names from reference docs.

#### 5. App Architect
*   **Purpose**: To design the architecture of the sample app based on the list of APIs and documentation.
*   **Functionality**: Interacts with the user to get input and creates a finalized app architecture plan.

#### 6. Android Developer
*   **Purpose**: To implement the Android application based on the architecture plan.
*   **Functionality**: Generates the actual code, creates the project structure, and ensures the sample app builds.

#### 7. Friction Logger
*   **Purpose**: To document issues found during user testing in a structured format.
*   **Functionality**: Creates a friction log in markdown based on user input, listing issues and suggested improvements.

#### 8. Bug Filer
*   **Purpose**: To file formal bug reports in the tracking system.
*   **Functionality**: Interacts with the bug tracking system (e.g., Buganizer) to create tickets for identified issues.

## Workflow

1.  **Initialization**: The *Main Orchestrator* (L3) receives the target library as input.
2.  **Knowledge Gathering**: The *Main Orchestrator* asks the *Knowledge Agent* (L2) to discover APIs and build a mental model.
    *   The *Knowledge Agent* delegates to the *API Lister* (L1) to get the API list.
    *   The *Knowledge Agent* uses the *Reference Docs Explorer* (L1) and *Documentation Reader* (L1) to explore.
3.  **Architecture & Coding**: The *Main Orchestrator* asks the *Android Developer Manager* (L2) to produce the app.
    *   The *Android Developer Manager* uses the *App Architect* (L1) to design the architecture, interacting with the user for feedback.
    *   The *Android Developer Manager* uses the *Android Developer* (L1) to generate the code.
4.  **Issue Identification**: The *Android Developer Manager* identifies issues during building.
5.  **Feedback Loop**: When the user tests the app and reports issues, the *Main Orchestrator* uses the *Issue Resolution Manager* (L2) to handle them.
    *   The *Issue Resolution Manager* uses the *Friction Logger* (L1) to document the issues.
    *   The *Issue Resolution Manager* uses the *Bug Filer* (L1) to create tickets in the tracking system.
