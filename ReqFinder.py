import os
import requests
import git
from git.exc import GitCommandError

# Function to search for Python repositories on GitHub
def search_python_repositories(query, num_results=10):
    url = f"https://api.github.com/search/repositories?q={query}&per_page={num_results}"
    response = requests.get(url)
    data = response.json()
    return data['items']

# Function to clone a repository
def clone_repository(repo_url, destination):
    try:
        git.Repo.clone_from(repo_url, destination)
        return True
    except GitCommandError:
        print(f"Failed to clone {repo_url}")
        return False

# Function to find requirements.txt files and extract dependencies
def find_dependencies(repo_dir):
    dependencies = []
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.lower() == 'requirements.txt':
                with open(os.path.join(root, file), 'r') as f:
                    dependencies.extend(f.read().splitlines())
    return dependencies

# Main function
def main():
    # Prompt user for repository
    repo_name = input("Enter the GitHub repository (in the format 'username/repository'): ")

    # Clone repository and gather dependencies
    repo_url = f"https://github.com/{repo_name}.git"
    destination = os.path.join('repositories', repo_name.split('/')[1])
    print(f"Cloning {repo_name}...")
    if clone_repository(repo_url, destination):
        dependencies = find_dependencies(destination)
        if dependencies:
            # Write dependencies to requirements.txt file
            with open('requirements.txt', 'w') as f:
                for dependency in dependencies:
                    f.write(dependency + '\n')
            print("Dependencies saved to requirements.txt file.")
        else:
            print("No dependencies found.")
    else:
        print("Failed to clone repository.")

if __name__ == "__main__":
    main()
