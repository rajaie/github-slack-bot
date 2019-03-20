import logging
import github
from github import Github

logger = logging.getLogger()

class GitClient:  
    """GitClient is the client that our SlackBot uses to create GitHub issues.
    """
    def __init__(self, github_api_token, github_repo):        
        # TODO: add support for username/password authentication
        # TODO: add some basic error checking for the constructor params
        self.gc = Github(github_api_token)
        self.github_repo = self.gc.get_repo(github_repo)

        logger.info("GitHub client initialized")

    # TODO: allow passing in the GitHub repo as a parameter
    def create_issue(self, issue_title, issue_body):
        """Create an Issue on GitHub for the repo associated with this GitClient
        :param issue_title: title of the GitHub issue
        :param issue_body: body of the GitHub issue
        :return: A dict with a link to the issue if it was created successfully,
        a dict with an error message otherwise.
                Example:
                {"ok": True, "link": "http://github.com/owner/repo/issue/1"}
                    or
                {"ok": False, "error": "Error message goes here"}
        """
        try:
            issue = self.github_repo.create_issue(issue_title, issue_body)

            res = {
                "ok": True,
                "link": issue.html_url
            }

            return res
        except github.GithubException as e:
            res = {
                "ok": False,
                "error": "Failed to create GitHub issue due to: *{}*. The following errors occurred: {}"
                         .format(e.data.get("message", "Unknown reason"), e.data.get("errors", "Unknown error"))
            }

            return res
        except Exception as e:
            raise e


