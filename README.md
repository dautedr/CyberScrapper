# GitHub Security Projects Scanner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/dautedr/CyberScrapper?style=social)](https://github.com/dautedr/CyberScrapper)

A Python script that automatically discovers and documents popular cybersecurity projects on GitHub. The script searches for repositories with 50+ stars in the cybersecurity category, and saves relevant information locally.

## Features

- 🔍 Searches for cybersecurity repositories with 50+ stars
- 🚫 Excludes forked repositories
- 📁 Creates organized folders for each repository
- 📝 Saves repository URLs and descriptions
- 🔢 Configurable number of repositories to process

## Requirements

- Python 3.8+
- Chrome browser installed
- GitHub Personal Access Token

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your GitHub token:

```bash
GITHUB_TOKEN=your_github_token_here
```

## Getting a GitHub Token

1. Go to GitHub.com → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Generate new token with these permissions:
   - `public_repo`
   - `read:org`
3. Copy the token to your `.env` file

## Usage

Run the script:

```bash
python main.py
```

You'll be prompted to:

1. Process repositories
2. Remove all existing folders
3. Remove existing folders and process new repositories

When processing repositories, you can specify how many to scan or press Enter for no limit.

## Output

For each repository, the script creates:

- A folder named after the repository
- `info.txt` containing the repository URL and description

## Security Note

- Never commit your `.env` file
- Keep your GitHub token secure
- Revoke tokens if accidentally exposed

## License

MIT License

This project is licensed under the MIT License - a permissive license that allows you to:

- Use the code commercially
- Modify the code
- Distribute the code
- Use the code privately
- Sublicense the code

The only requirement is that you include the original copyright notice and license disclaimer in any copy of the software/source.

See the [MIT License](https://opensource.org/licenses/MIT) for full details.
