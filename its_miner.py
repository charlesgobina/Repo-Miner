"""Mines the issue data for a github repo"""

from github import Auth, Github


class ITSMiner:
    """
    Represents the issue data miner for github

    Attributes:
    ----------

    __issue_data (dict): Class variable that stores all the issue data for a repo

    Methods:
    --------

    get_issue_data(): Class method to get all the issue data for a repo
    """

    __issue_data: dict = {}

    @classmethod
    def mine_issue_data(repo: str) -> dict:
        """
        Mines all the issue data for a github repository

        Parameter:
        --------

        repo (str): Name of the repository. Has to be of the format `Owner/Repository`

        Returns:
        -------

        Returns a dictionary with all issue data
        """

        pass
