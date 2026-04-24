import sys
import os

# Add parent directory to path to import api_knowledge_agent
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from api_knowledge_agent.agent import root_agent as api_knowledge_agent
from google.adk.tools import AgentTool
from google.adk.agents import Agent

def write_file(filepath: str, content: str) -> str:
    """
    Writes content to a file at the specified filepath.
    The filepath should be within the project directory.
    
    Args:
        filepath: The path to the file to create or overwrite.
        content: The content to write to the file.
        
    Returns:
        A message indicating success or failure.
    """
    try:
        # Ensure directories exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Failed to write to {filepath}: {str(e)}"

def modify_file(filepath: str, content: str, search_text: str) -> str:
    """
    Modifies a file by replacing a specific search_text with new content.
    The filepath should be within the project directory.
    
    Args:
        filepath: The path to the file to modify.
        content: The new content to insert.
        search_text: The text in the file to be replaced.
        
    Returns:
        A message indicating success or failure.
    """
    try:
        if not os.path.exists(filepath):
             return f"File {filepath} not found."
        with open(filepath, 'r') as f:
             file_content = f.read()
        
        if search_text not in file_content:
             return f"Search text not found in {filepath}."
             
        new_content = file_content.replace(search_text, content)
        
        with open(filepath, 'w') as f:
            f.write(new_content)
        return f"Successfully modified {filepath}"
    except Exception as e:
        return f"Failed to modify {filepath}: {str(e)}"

def read_project_file(filepath: str) -> str:
    """
    Reads the content of a file within the project directory.
    
    Args:
        filepath: The path to the file to read.
        
    Returns:
        The content of the file or an error message.
    """
    try:
        if not os.path.exists(filepath):
             return f"File {filepath} not found."
        with open(filepath, 'r') as f:
             return f.read()
    except Exception as e:
        return f"Failed to read {filepath}: {str(e)}"

def list_project_files(folder_path: str) -> dict:
    """Lists all files in the specified folder recursively.
    
    Args:
        folder_path (str): The path to the folder to list files from.
        
    Returns:
        dict: status and list of files or error message.
    """
    try:
        if not os.path.exists(folder_path):
            return {"status": "error", "message": f"Folder does not exist: {folder_path}"}
        
        files = []
        for root, dirs, filenames in os.walk(folder_path):
            for filename in filenames:
                files.append(os.path.relpath(os.path.join(root, filename), folder_path))
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_project_files(folder_path: str, query: str) -> dict:
    """Searches for a query string within files in the folder.
    
    Args:
        folder_path (str): The path to the folder to search in.
        query (str): The string to search for.
        
    Returns:
        dict: status and matching files with snippets or error message.
    """
    try:
        if not os.path.exists(folder_path):
            return {"status": "error", "message": f"Folder does not exist: {folder_path}"}
        
        matches = []
        for root, dirs, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            idx = content.lower().find(query.lower())
                            start = max(0, idx - 50)
                            end = min(len(content), idx + len(query) + 50)
                            snippet = content[start:end]
                            matches.append({
                                "file": os.path.relpath(file_path, folder_path),
                                "snippet": snippet
                            })
                except Exception as e:
                    continue
        return {"status": "success", "matches": matches}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute_project_command(command: str, working_dir: str) -> str:
    """
    Executes a terminal command in the specified working directory.
    
    Args:
        command: The command to execute (e.g., "./gradlew build").
        working_dir: The directory to run the command in.
        
    Returns:
        The output of the command or an error message.
    """
    import subprocess
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nExit Code: {result.returncode}"
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Failed to execute command: {str(e)}"

# Wrap the api_knowledge_agent in AgentTool
api_tool = AgentTool(agent=api_knowledge_agent)

root_agent = Agent(
    name="app_developer_agent",
    model="gemini-2.5-flash",
    description="An agent that creates Android apps using Compose and refers to the API Knowledge Agent.",
    instruction="""You are a senior Android developer using Jetpack Compose.
    Your goal is to create a demo app based on the user's request.
    
    Follow this workflow:
    1. Start by asking the user for the path to the initialized empty Android project and a description of the app they want to build.
    2. Discuss the design with the user. Do not write any code until the user explicitly approves the design.
    3. Once approved, create the app by writing code to the provided project folder using your tools.
    4. Allow the user to refine the app by talking to you.
    
    You MUST talk to the `api_knowledge_agent` tool for any information regarding the library or API. You MUST NOT make assumptions about the API. If you need to know how to use a class, method, or feature of the library, ask the `api_knowledge_agent`.
    
    Use `read_project_file` to read files, `list_project_files` to list files, and `search_project_files` to search for files in the project folder to understand state or locate files like build scripts.
    Use `execute_project_command` to run build commands like `./gradlew build` to verify your changes.
    
    Read the skill guide at `/usr/local/google/home/amanchoudharyg/aman-adk/agent/app_developer_agent/skills/android_app_skill.md` using `read_project_file` to understand Android project structure and conventions.
    """,
    tools=[api_tool, write_file, modify_file, read_project_file, list_project_files, search_project_files, execute_project_command],
)
