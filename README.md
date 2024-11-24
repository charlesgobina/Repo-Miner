# GitHub Repository Analysis

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
    pip install -r requirements.txt
    ```

## Usage

1. Prepare the CSV file with the project data and place it in the `data` directory. The default file name is `sonar_measures.csv`.

2. Run the main script to start the analysis:

    ```sh
    python index.py
    ```

3. The results will be stored in the `output` directory.

## Project Structure

- `developers_effort.py`: Contains the `DevEffort` class for analyzing developer effort.
- `get_commit_diff.py`: Contains the `ProjectInfo` class for storing project information.
- `get_github_url.py`: Contains the `CSVHandler` class for handling CSV files and cloning repositories.
- `index.py`: Main script to run the analysis.
- `refactoring_miner.py`: Contains the `RefactoringMiner` class for mining refactoring data.
- `utility.py`: Utility functions used across the project.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.