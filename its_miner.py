"""Mines the issue data for a github repo"""

from datetime import datetime

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

    # TODO: clear the variable of issue data once its called.
    __issue_data: dict = {"issues": []}

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

        # TODO: need to improve this
        # clear previous issues
        cls.__issue_data["issues"] = []

        # for each issue get required data
        for issue in issues:
            issue_number = cls.__get_issue_number(issue)
            issue_title = cls.__get_issue_title(issue)
            issue_body = cls.__get_issue_body(issue)
            issue_status = cls.__get_issue_status(issue)
            issue_date_created = cls.__get_issue_date_created(issue)
            issue_user_data = cls.__get_issue_user_data(issue)

            issue_data = {
                "number": issue_number,
                "title": issue_title,
                "body": issue_body,
                "status": issue_status,
                "date_created": issue_date_created,
                "user": issue_user_data
            }

            # TODO: this provides all the data
            # but seems to take alot of time in processing
            # issue_data = issue.raw_data

            cls.__issue_data.get("issues").append(issue_data)

        return cls.__issue_data

    @classmethod
    def __get_issue_number(cls, issue: Issue) -> int:
        """
        Get the number of the issue

        Parameters:
        --------

        issue (Issue): Issue instance of the repo

        Returns:
        -------

        An int representing the issue number
        """

        issue_number = issue.number
        return issue_number

    @classmethod
    def __get_issue_title(cls, issue: Issue) -> str:
        """
        Get the title of the issue

        Parameters:
        --------

        issue (Issue): Issue instance of the repo

        Returns:
        -------

        A string representing the issue title
        """

        issue_title = issue.title
        return issue_title

    @classmethod
    def __get_issue_body(cls, issue: Issue) -> str:
        """
        Extract the issue body

        Parameters:
        --------

        issue (Issue): Issue instance of the repo

        Returns:
        -------

        A string representing the issue body
        """

        issue_body = issue.body
        return issue_body

    @classmethod
    def __get_issue_status(cls, issue: Issue) -> str:
        """
        Extract the status of the issue

        Parameters:
        --------

        issue (Issue): Issue instance of the repo
        """

        status = issue.state
        return status

    @classmethod
    def __get_issue_date_created(cls, issue: Issue) -> str:
        """
        Extract the date at which the issue was created.

        Formats the date to a string.

        Parameters:
        --------

        issue (Issue): Issue instance of the repo
        """

        date_created = issue.created_at
        formatted_date = datetime.strftime(date_created, "%d.%m.%y-%H.%M.%S")
        return formatted_date

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

    @classmethod
    def __get_issue_labels(cls, issue: Issue):
        """
        Extract the labels asociated with the issue

        Parameters:
        --------

        issue (Issue): Issue instance of the repo
        """

        pass

    @classmethod
    def __get_issue_user_data(cls, issue: Issue) -> dict:
        """
        Extract the user details

        Extract the details of the user that created the issue

        ## Parameters:

        issue (Issue): Issue instance of the repo

        ## Returns

        Dictionary with user data
        """

        user_data = {}
        user_data.update({
            "username": issue.user.login,
            "id": issue.user.id,
            "url": issue.user.url,
            "repos_url": issue.user.repos_url,
            "type": issue.user.type
        })

        return user_data

        