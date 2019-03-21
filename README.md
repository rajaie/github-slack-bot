# GitHub Slack Bot
A Slack bot for creating GitHub issues.

Example:

```
@ticketbot My issue title__My issue body here
```

Makes use of the Slack RTM API and Bots integration to make it easier for your team to document issues through Slack.

At this moment, the bot will only be able to create issues for a single GitHub repo that is configured at run time.

## Getting Started
Before running the Slack bot, there are a few steps you need to complete.

**GitHub API Token**

[Generate](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) a Personal Access Token for a GitHub user that has read permissions to the repo you want to create issues for.

**Slack "Bots" Integration**

Add a bot integration to your Slack workspace [here](http://my.slack.com/apps/A0F7YS25R-bots). (Click "Add Configuration" and go through the following screens.)

**Invite Bot to Channels**

Invite the bot user created above to any channels you would like to interact with it from.

## Setup
We will run the Slackbot in a Docker container, so make sure you have Docker installed on your machine.

1. Clone this repo on to your local machine
2. `cd` into the root folder for this repo and run `docker build -t slackbot -f build/Dockerfile .` to build the Docker image

## Usage

1. Run the Slack bot, making sure to set the environment variables: 
    ```
    docker run \
    -e GITHUB_REPO="REPO/HERE" \
    -e GITHUB_API_TOKEN=XXXXXXXXXXXXXXXX \
    -e SLACK_API_TOKEN=XXXXXXXXXXXXXXXX \
    slackbot github_slack_bot/main.py
    ```
2. In Slack, go to a channel that has the bot user and mention it in a message as below:
```
@ticketbot Build breaking__Fix typo in build script!
```

If everything is setup correctly, the Slack bot should reply with a link to the GitHub issue it created, otherwise it will send a message with the error.

## Testing
To run all tests:

`docker run slackbot -m unittest discover tests/`

To run an individual test:

`docker run slackbot -m unittest tests/test_slack.py`

## Style Guidelines
The code in this repo follows the [PEP 8 Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).