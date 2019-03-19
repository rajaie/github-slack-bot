import logging
import os
import sys
from utils import slack
from utils import git

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d:%(funcName)s] %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    # TODO: add config system to grab values from a standard chain (e.g. cli params, env vars, .yml file)
    slack_api_token = os.environ.get('SLACK_API_TOKEN')
    github_repo = os.environ.get('GITHUB_REPO')
    github_api_token = os.environ.get('GITHUB_REPO')

    git_client = git.GitClient()

    try:
        slack_bot = slack.SlackBot(slack_api_token, git_client)
    except Exception as e:
        logger.error("Failed to initialize Slack bot due to: {}. Make sure your Slack API token is correct, "
                     "or check your internet connection.".format(e.__class__.__name__))
        return 1

    try:
        slack_bot.start_bot()
    except Exception as e:
        logger.error("An unexpected error occurred: {}. Shutting down Slack bot."
                     .format(e.__class__.__name__), exc_info=True)
        return 1
    except KeyboardInterrupt as e:
        logger.info("Received stop signal from user, shutting down Slack bot.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
