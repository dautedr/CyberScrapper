import os
import time
import random
from github import Github
import shutil
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

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
        if repo.fork:
            return None
        
        folder_name = create_repo_folder(repo.full_name)
        if os.path.exists(folder_name):
            return None
        
        os.makedirs(folder_name)
        save_repo_info(folder_name, repo.html_url, repo.description)
        
        return repo.full_name
        
    except Exception as e:
        print(f"Error processing repository {repo.full_name}: {str(e)}")
        return None

def remove_all_folders():
    current_dir = os.getcwd()
    folders_to_remove = [item for item in os.listdir(current_dir) 
                        if os.path.isdir(item) and os.path.exists(os.path.join(item, "info.txt"))]
    
    if folders_to_remove:
        for item in tqdm(folders_to_remove, desc="Removing folders"):
            try:
                shutil.rmtree(item)
            except Exception as e:
                print(f"Error removing folder {item}: {str(e)}")

def main(limit=None, clean=False):
    if clean:
        remove_all_folders()
        if not limit:
            return
    
    with ThreadPoolExecutor() as executor:
        try:
            print("Searching for repositories...")
            query = "topic:security topic:cybersecurity stars:>50 fork:false"
            all_repositories = list(g.search_repositories(query=query))
            
            # Randomly shuffle the repositories
            random.shuffle(all_repositories)
            
            # Take the requested number of repositories after shuffling
            repositories = all_repositories[:limit] if limit else all_repositories
            
            print(f"Found {len(repositories)} repositories to process")
            
            # Create progress bar
            with tqdm(total=len(repositories), desc="Processing repositories") as pbar:
                futures = []
                for repo in repositories:
                    future = executor.submit(process_repository, repo)
                    future.add_done_callback(lambda p: pbar.update(1))
                    futures.append(future)
                
                processed = [f.result() for f in as_completed(futures) if f.result()]
            
            print(f"\nSuccessfully processed {len(processed)} repositories")
                
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
