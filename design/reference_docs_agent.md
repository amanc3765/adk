# Reference Docs Agent Design

This document outlines the refined design for the Reference Docs Agent in the DevRel Agent system.

## Role
The Reference Docs Agent is responsible for locating, crawling, and managing API reference documentation for target libraries. It acts as the single point of truth for questions about API usage, signatures, and documentation from other agents.

*   **Concise Description (for ADK routing)**: Finds, crawls, and searches API reference documentation for libraries.

## Workflow & Responsibilities

### 1. Root Discovery
*   **Trigger**: The agent receives a high-level request from the Knowledge Manager or the user.
*   **Action**: The agent prompts the user to provide the root URL of the library's documentation (e.g., `https://developer.android.com/reference/kotlin/androidx/media3/ui/compose/`).

### 2. Crawling & Processing
*   **Action**: Crawl all links sharing the root URL prefix to discover sub-packages and class summaries.
*   **Markdown Generation**: For each visited link, convert the HTML page content to markdown format.

### 3. Knowledge Storage
*   **Structure**: Store all generated markdown files into a specific directory structure in the user's project:
    ```
    /knowledge/reference/
    ```
*   **Action**: Populate this directory with the downloaded and converted documentation pages, serving as a local knowledge repository.

### 4. Query Management
*   **Action**: Manage this repository of knowledge files.
*   **Action**: Answer questions from other agents using this local knowledge base.

## Persona & Behavior

*   **Source of Truth**: The agent considers the local markdown files in `/knowledge/reference/` as the single source of truth.
*   **Grounding**: Answers must be strictly based on the content of these files.
*   **Inference**: The agent can infer usage based on the docs, but must not hallucinate or assume facts not present.
*   **Fallback**: If the query asks about something not covered in the local documentation, the agent must reply "I don't know" and refer to the Knowledge Manager.
*   **Guardrails**: The agent must validate that the URL provided by the user is secure (starts with `https://`).

## Tool Definitions

> [!NOTE]
> All tool implementations must include detailed Python docstrings as required by the ADK framework for automatic schema generation.

These are the tools this agent will use to execute its workflow:

### 1. `get_root_from_user`
*   **Description**: Prompts the user to enter the root URL for the library documentation.
*   **Input**: `prompt_message` (e.g., "Please enter the root URL for the documentation:")
*   **Output**: `root_url` (e.g., `https://developer.android.com/reference/kotlin/androidx/media3/ui/compose/`)

### 2. `crawl_pages`
*   **Description**: Takes the root link and returns a list of all pages (links) to crawl within that scope.
*   **Input**: `root_url`
*   **Output**: `list_of_urls`

### 3. `fetch_and_convert_to_markdown`
*   **Description**: Takes a URL, fetches the HTML content, and converts it to a markdown file, saving it in the `/knowledge/reference/` directory.
*   **Input**: `url`
*   **Output**: `file_path` (or confirmation)

### 4. `search_local_docs`
*   **Description**: Given a query, searches through the local markdown documentation repository and returns the relevant API reference section.
*   **Input**: `query` (e.g., "Find API for MuteButton")
*   **Output**: `markdown_snippet` (the relevant section of the doc)

## Orchestration & Runners

*   **Phase 1: Initialization**: Uses a **Sequential Runner** to execute the flow: `get_root_from_user` -> `crawl_pages` -> `fetch_and_convert_to_markdown`.
*   **Phase 2: Querying**: Operates as a **Single Agent** with access to the `search_local_docs` tool, dynamically deciding when to search based on the query.

## Input/Output Interface

The agent supports the following interaction flow and message formats:

### Phase 1: Initialization
1.  **Input (from Knowledge Manager)**: Request to start API feedback for a library (e.g., "Start feedback for Media3 UI Compose").
2.  **Output (from Agent)**: Prompt for the root URL (e.g., "Please provide the root URL for the documentation").
3.  **Input (from User/Knowledge Manager)**: The root URL (e.g., `https://developer.android.com/reference/kotlin/androidx/media3/ui/compose/`).
4.  **Output (from Agent)**: Confirmation of download (e.g., "Downloaded all documentation to /knowledge/reference/").

### Phase 2: Querying
Once initialized, the agent accepts the following queries:

*   **Feature Search Query**
    *   **Input**: "Is there an API for feature X?"
    *   **Output**: List of candidate APIs or relevant snippets found in the docs.
*   **Specific API Query**
    *   **Input**: "Get docs for class `MuteButton`"
    *   **Output**: The full markdown content or specific reference section for `MuteButton`.
