"""Mines the issue data for a github repo"""

from github import Auth, Github
from github.Issue import Issue


class ITSMiner:
    """
    Represents the issue data miner for github

    Attributes:
    ----------

    __issue_data (dict): Class variable that stores all the issue data for a repo

    Methods:
    --------

    mine_issue_data(): Class method to get all the issue data for a repo
    """

    __issue_data: dict = {}

    @classmethod
    def mine_issue_data(cls, repo: str) -> dict:
        """
        Mines all the issue data for a github repository

        Parameter:
        --------

        repo (str): Name of the repository. Has to be of the format `Owner/Repository`

        Returns:
        -------

        Returns a dictionary with all issue data
        """

        auth = Auth.Token("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")
        github = Github(auth=auth)
        repo = github.get_repo(repo)
        issues = repo.get_issues()

        # for each issue get required data
        for issue in issues:
            pass

        return cls.__issue_datas

    @classmethod
    def __get_issue_number(cls, issue: Issue):
        """
        Get the number of the issue

        Parameters:
        --------

        issue (Issue): Issue instance of the repo
        """

        pass

    @classmethod
    def __get_issue_title(cls, issue: Issue):
        """
        Get the title of the issue

        Parameters:
        --------

        issue (Issue): Issue instance of the repo
        """

        pass

    @classmethod
    def __get_issue_body(cls, issue: Issue):
        """
        Extract the issue body

        Parameters:
        --------

        issue (Issue): Issue instance of the repo
        """

        pass

    @classmethod
    def __get_issue_status(cls, issue: Issue):
        """
        Extract the status of the issue

        Parameters:
        --------

        issue (Issue): Issue instance of the repo
        """

        pass

    @classmethod
    def __get_issue_date_created(cls, issue: Issue):
        """
        Extract the date at which the issue was created

        Parameters:
        --------

        issue (Issue): Issue instance of the repo
        """

        pass

    @classmethod
    def __get_issue_comments(cls, issue: Issue):
        """
        Extract the comments of the issue

        Parameters:
        --------

        issue (Issue): Issue instance of the repo
        """

        pass

    @classmethod
    def __get_issue_date_closed(cls, issue: Issue):
        """
        Extract the date at which the issue was closed

        Parameters:
        --------

        issue (Issue): Issue instance of the repo
        """

        pass
