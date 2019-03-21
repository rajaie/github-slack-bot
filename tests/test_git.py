import unittest
from unittest import mock
from github_slack_bot.utils.git import GitClient
from github import GithubException

import logging
logging.disable(logging.CRITICAL)


class TestGitClient(unittest.TestCase):
    @mock.patch('github_slack_bot.utils.git.Github')
    def test_create_issue_success_returns_link(self, github):
        """Check that our function returns a proper response with a link to the issue on success"""
        fake_issue_link = "http://google.com"
        fake_issue = mock.Mock()
        fake_issue.html_url = fake_issue_link

        github.return_value.get_repo.return_value.create_issue.return_value = fake_issue

        gc = GitClient("git_api_token", "git_repo")
        issue_res = gc.create_issue("Issue title", "Issue body")

        self.assertDictEqual(issue_res, {
            "ok": True,
            "link": fake_issue_link
        })

    @mock.patch('github_slack_bot.utils.git.Github')
    def test_create_issue_failure_returns_error(self, github):
        """Check that our Git client returns an error if the underlying Git API library raises an exception"""

        error_message = "Validation failed"
        errors_list = "Errors listed here"
        github.return_value.get_repo.return_value.create_issue.side_effect = GithubException(
            status=-1,
            data={
                "message": error_message,
                "errors": errors_list
            }
        )

        gc = GitClient("git_api_token", "git_repo")
        issue_res = gc.create_issue("Issue title", "Issue body")

        self.assertDictEqual(issue_res, {
            "ok": False,
            "error": "Failed to create GitHub issue due to: *{}*. The following errors occurred: {}".format(
                error_message, errors_list
            )
        })


if __name__ == "__main__":
    unittest.main()
