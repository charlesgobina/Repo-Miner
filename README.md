# REPO-MINER

This project is designed to analyze GitHub repositories by mining refactoring data, commit details, and other relevant metrics. The analysis includes cloning repositories, extracting commit information, and calculating various statistics.

## Table of Contents

- [GitHub Repository Analysis](#github-repository-analysis)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```sh
    pip3 install -r requirements.txt
    ```

## Usage

The recommended way to start the application is using docker. First the environment variables need to be set

|  Varible   | Description    |
| :---: | :---: |
| API_KEY  | Github token to use for the Github API     |
|LOGGING_LEVEL| The logging level to set|
|INPUT_FILE|Input csv file with the project names to mine. This needs to be mounted as a volume in the `input` directory|

The miner outputs are stored in different directories. They can be accessed by mounting them as volumes. 

To start the application run:
    
```bash
sudo docker compose up
```

## Project Structure

- `developers_effort.py`: Contains the `DevEffort` class for analyzing developer effort.
- `get_commit_diff.py`: Contains the `ProjectInfo` class for storing project information.
- `get_github_url.py`: Contains the `CSVHandler` class for handling CSV files and cloning repositories.
- `main.py`: Main script to run the analysis.
- `refactoring_miner.py`: Contains the `RefactoringMiner` class for mining refactoring data.
- `utility.py`: Utility functions used across the project.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.