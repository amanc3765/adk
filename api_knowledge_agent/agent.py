import os
from google.adk.agents import Agent

def list_files(folder_path: str) -> dict:
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

def read_file(folder_path: str, file_path: str) -> dict:
    """Reads the content of a specific file within the folder.
    
    Args:
        folder_path (str): The base folder path.
        file_path (str): The relative path to the file from the folder path.
        
    Returns:
        dict: status and file content or error message.
    """
    try:
        full_path = os.path.join(folder_path, file_path)
        if not os.path.exists(full_path):
            return {"status": "error", "message": f"File does not exist: {full_path}"}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_files(folder_path: str, query: str) -> dict:
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

root_agent = Agent(
    name="api_knowledge_agent",
    model="gemini-2.5-flash",
    description="An agent that answers questions based on API documentation in a local folder.",
    instruction="""You are a helpful agent designed to answer questions about an API by reading documentation and library code from multiple locations.
You will be provided with a list of folder paths containing relevant information.

Your goal is to use the available tools to find information in all provided folders and answer user questions.

Workflow:
1. At the very beginning of the conversation, ask the user to provide the list of all folder paths they want you to use as the source of truth.
2. Use `list_files` to see what files are available in the provided folders.
3. Use `search_files` to find files containing specific keywords in all sources.
4. Use `read_file` to read the content of relevant files to extract the answer.

Always adhere strictly to the content in the provided folders. Do not make assumptions or provide answers not supported by these sources. The provided paths are the absolute source of truth.

Read the skill guide at `/usr/local/google/home/amanchoudharyg/aman-adk/agent/api_knowledge_agent/skills/search_skill.md` by using `read_file` with folder path `/usr/local/google/home/amanchoudharyg/aman-adk/agent/api_knowledge_agent/skills` and file path `search_skill.md` to understand how to use your tools effectively.
""",
    tools=[list_files, read_file, search_files],
)
