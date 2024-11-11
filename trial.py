import subprocess
import json
from pathlib import Path
import os
import logging
from datetime import datetime
from typing import List, Tuple
import time


class IncrementalRefactoringMiner:
    def __init__(self, repo_path: str, output_dir: str, batch_size: int = 1000):
        """
        Initialize the incremental mining process

        Args:
            repo_path: Path to the git repository
            output_dir: Directory to store output JSON files
            batch_size: Number of commits to process in each batch
        """
        self.repo_path = Path(repo_path)
        self.output_dir = Path(output_dir)
        self.batch_size = batch_size
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.setup_logging()

    def setup_logging(self):
        """Configure logging"""
        log_file = self.output_dir / 'mining_log.txt'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_all_commits(self) -> List[str]:
        """Get list of all commit hashes in chronological order"""
        try:
            result = subprocess.run(
                ['git', 'log', '--reverse', '--format=%H'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n')
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get commits: {e}")
            return []

    def split_commits_into_batches(self, commits: List[str]) -> List[Tuple[str, str]]:
        """Split commits into batches of specified size"""
        batches = []
        for i in range(0, len(commits), self.batch_size):
            batch_commits = commits[i:i + self.batch_size]
            if batch_commits:
                batches.append((batch_commits[0], batch_commits[-1]))
        return batches

    def run_refactoring_miner(self, start_commit: str, end_commit: str, output_file: Path) -> bool:
        """Run RefactoringMiner for a specific commit range"""
        try:
            # Adjust this command based on your RefactoringMiner installation
            cmd = [
                'RefactoringMiner',
                '-bc',
                str(self.repo_path),
                start_commit,
                end_commit,
                str(output_file)
            ]

            self.logger.info(
                f"Running RefactoringMiner for commits {start_commit[:7]} to {end_commit[:7]}")
            process = subprocess.run(cmd, capture_output=True, text=True)

            if process.returncode != 0:
                self.logger.error(f"RefactoringMiner failed: {process.stderr}")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Error running RefactoringMiner: {e}")
            return False

    def merge_json_files(self, json_files: List[Path], final_output: Path):
        """Merge multiple JSON files into one"""
        try:
            merged_data = []
            for file in json_files:
                with open(file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        merged_data.extend(data)
                    else:
                        merged_data.append(data)

            with open(final_output, 'w') as f:
                json.dump(merged_data, f, indent=2)

            self.logger.info(f"Successfully merged files into {final_output}")

        except Exception as e:
            self.logger.error(f"Error merging JSON files: {e}")

    def process_repository(self):
        """Process the entire repository in batches"""
        try:
            # Get all commits
            self.logger.info(f"Getting commit list for {self.repo_path}")
            commits = self.get_all_commits()
            if not commits:
                self.logger.error("No commits found")
                return

            # Split into batches
            batches = self.split_commits_into_batches(commits)
            self.logger.info(f"Split repository into {len(batches)} batches")

            # Process each batch
            temp_files = []
            for i, (start, end) in enumerate(batches, 1):
                output_file = self.output_dir / f"refactorings_batch_{i}.json"
                temp_files.append(output_file)

                self.logger.info(f"Processing batch {i}/{len(batches)}")
                success = self.run_refactoring_miner(start, end, output_file)

                if not success:
                    self.logger.warning(
                        f"Failed to process batch {i}, continuing with next batch")

                # Add a small delay to prevent overwhelming the system
                time.sleep(2)

            # Merge all valid JSON files
            final_output = self.output_dir / \
                f"all_refactorings_{self.repo_path.name}.json"
            self.merge_json_files(
                [f for f in temp_files if f.exists()], final_output)

            # Cleanup temporary files
            for temp_file in temp_files:
                if temp_file.exists():
                    temp_file.unlink()

        except Exception as e:
            self.logger.error(f"Error processing repository: {e}")


def main():
    # Example usage
    repos = [
        "/path/to/repo1",
        "/path/to/repo2",
        # Add more repositories as needed
    ]

    output_base_dir = Path("refactoring_results")

    for repo_path in repos:
        miner = IncrementalRefactoringMiner(
            repo_path=repo_path,
            output_dir=output_base_dir / Path(repo_path).name,
            batch_size=500  # Adjust based on your needs
        )
        miner.process_repository()


if __name__ == "__main__":
    main()
