import os
import time
from github import Github
import shutil
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables
load_dotenv()

# GitHub API token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("Please set the GITHUB_TOKEN in .env file")

# Initialize GitHub API
g = Github(GITHUB_TOKEN)

def create_repo_folder(repo_name):
    safe_name = repo_name.replace('/', '_').replace('\\', '_').lower()
    safe_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in safe_name)
    return safe_name

def save_repo_info(folder_name, repo_url, repo_description):
    with open(f"{folder_name}/info.txt", "w", encoding="utf-8") as f:
        f.write(f"Repository URL: {repo_url}\n")
        f.write(f"Description: {repo_description if repo_description else 'No description available'}")

def process_repository(repo):
    try:
        print(f"\nProcessing: {repo.full_name}")
        
        if repo.fork:
            return None
        
        folder_name = create_repo_folder(repo.full_name)
        if os.path.exists(folder_name):
            print(f"Repository {repo.full_name} already processed, skipping...")
            return None
        
        os.makedirs(folder_name)
        save_repo_info(folder_name, repo.html_url, repo.description)
        
        print(f"Successfully processed: {repo.full_name}")
        return repo.full_name
        
    except Exception as e:
        print(f"Error processing repository {repo.full_name}: {str(e)}")
        return None

def remove_all_folders():
    current_dir = os.getcwd()
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "info.txt")):
            try:
                shutil.rmtree(item_path)
                print(f"Removed folder: {item}")
            except Exception as e:
                print(f"Error removing folder {item}: {str(e)}")

def main(limit=None, clean=False):
    if clean:
        remove_all_folders()
        if not limit:
            return
    
    with ThreadPoolExecutor() as executor:
        try:
            query = "topic:security topic:cybersecurity stars:>50 fork:false"
            repositories = list(g.search_repositories(query=query)[:limit if limit else None])
            
            print(f"Starting to process {len(repositories)} repositories...")
            
            futures = [executor.submit(process_repository, repo) for repo in repositories]
            processed = [f.result() for f in as_completed(futures) if f.result()]
            print(f"\nTotal repositories processed: {len(processed)}")
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("1. Process repositories")
    print("2. Remove all existing folders")
    print("3. Remove existing folders and process new repositories")
    
    try:
        operation = input("Select operation (1-3): ").strip()
        
        if operation == "1":
            user_input = input("Enter the number of repositories to process (press Enter for no limit): ").strip()
            limit = int(user_input) if user_input else None
            main(limit=limit, clean=False)
        elif operation == "2":
            main(limit=None, clean=True)
        elif operation == "3":
            user_input = input("Enter the number of repositories to process (press Enter for no limit): ").strip()
            limit = int(user_input) if user_input else None
            main(limit=limit, clean=True)
        else:
            print("Invalid operation selected.")
            exit(1)
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        exit(1)
