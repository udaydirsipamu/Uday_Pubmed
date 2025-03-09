# PubMed Research Paper Fetcher

This project fetches research papers from PubMed based on a user query, filters authors affiliated with pharmaceutical or biotech companies, and exports the results to a CSV file.

## Installation

### Prerequisites
Ensure you have Python 3.7+ installed on your system.

### Installing Poetry
Poetry is used for dependency management. Install it using the following commands:

#### Windows (PowerShell)
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
Restart your terminal after installation.


### Verify Poetry Installation
Run the following command to ensure Poetry is installed correctly:
```sh
poetry --version
```

## Setting Up the Project

1. Install Dependencies
   
   poetry install

## Running the Script
You can fetch PubMed papers using the following command:
poetry run python fetch_papers.py "AI in healthcare" -f papers.csv

- Replace `"AI in healthcare"` with your desired search query.
- The `-f papers.csv` flag saves the output to a CSV file.

## Debug Mode
To print results in the console for debugging, run:
poetry run python fetch_papers.py "AI in healthcare" -d

## Output Format
The script generates a CSV file with the following fields:
- PubMedID
- Title
- Publication Date
- Non-academic Author(s)
- Company Affiliation(s)
- Corresponding Author Email

## Contributing
Feel free to fork this repository and submit pull requests with improvements.

## License
This project is licensed under the MIT License.

