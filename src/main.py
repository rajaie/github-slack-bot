import os
from utils import slack
from utils import git

if __name__ == "__main__":
    # TODO: add config system to grab values from a standard chain (e.g. cli params, env vars, .yml file)
    slack_api_token = os.environ.get('SLACK_API_TOKEN')
    github_repo = os.environ.get('GITHUB_REPO')
    github_api_token = os.environ.get('GITHUB_REPO')

    git_client = git.GitClient()
    slack_bot = slack.SlackBot(slack_api_token, git_client)

    slack_bot.start_bot()
