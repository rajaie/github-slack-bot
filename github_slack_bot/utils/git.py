import logging
import github
from github import Github

logger = logging.getLogger()

# TODO: implement methods for GitClient
class GitClient():
    def __init__(self, github_api_token, github_repo):
        self.gc = Github(github_api_token)
        self.github_repo = self.gc.get_repo(github_repo)

        logger.info("GitHub client intialized")

    def create_issue(self, issue_title, issue_body):
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


