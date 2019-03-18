import logging
import re
from slackclient import SlackClient
from slackclient.client import SlackNotConnected

# TODO: Allow log level to be passed in as an application parameter
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d:%(funcName)s] %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

RTM_READ_INTERVAL = 1  # Number of seconds to wait between each rtm_read() call
EXCEPTION_DEFAULT_MSG = "Something unexpected occurred, see ERROR log and Traceback above"


class SlackBot:
    """The SlackBot listens to events from the Slack RTM API and creates GitHub issues
    from messages that mention the bot's username.
    """

    # TODO: extend is_bot_message() to allow bot mentions anywhere in the message
    @staticmethod
    def is_bot_message(bot_user_id, message):
        """Check if the message mentions the bot_user_id at
        the start of the message and includes a body
        :param bot_user_id: bot's user ID to search for
        :param message: message sent by user
        :return: True if bot is mentioned and message contains body, False otherwise
        """
        message_stripped = message.strip()
        logger.debug("Checking if bot '{}' is mentioned in message: '{}'"
                     .format(bot_user_id, message_stripped))
        return message_stripped.startswith("<@{}> ".format(bot_user_id))

    # TODO: give user ability to provide a GitHub repo in their message body
    # TODO: add ability to add assignees,labels, projects, milestones to Issues
    @staticmethod
    def parse_bot_message(msg):
        """Parse a message mentioning our bot
        :param msg: message sent by user
        :return: A dict with the issue title and body if they exist,
        a dict with an error message otherwise
                Example:
                {"ok": True, "issue_title": "Issue title here", "issue_body": "Issue body here"}
                {"ok": False, "error": "Error message goes here"}
        """
        msg_regex = "^<@(.+?)> (.*)"
        matches = re.search(msg_regex, msg)
        msg_body = matches.group(2).strip()
        msg_body_split = msg_body.split("__")
        logger.debug("Split message into {}".format(msg_body_split))

        if len(msg_body_split) == 2:
            issue_title = msg_body_split[0]
            issue_body = msg_body_split[1]
            res = {
                "ok": True,
                "issue_title": "{}".format(issue_title),
                "issue_body": "{}".format(issue_body)
            }
        else:
            res = {
                "ok": False,
                "error": "Failed to parse message. Issue title and issue body should be "
                         "separated by a double underscore (__)"
            }

        logger.info(res)
        return res

    def __init__(self, slack_api_token=None, git_client=None):
        self.git_client = git_client
        self.slack_api_token = slack_api_token
        self.bot_user_id = None
        self.sc = None

        logger.info("Slack bot initialized")

    def set_bot_user_id(self):
        """Make an auth.test Slack API call to retrieve the bot's user_id.
        Stores the user_id in the "bot_user_id" instance attribute
        :return: None
        """
        auth_test_res = self.sc.api_call("auth.test")
        if auth_test_res["ok"]:
            self.bot_user_id = auth_test_res['user_id']
            logger.info("Found bot's user_id: {}".format(self.bot_user_id))
        else:
            auth_test_error = auth_test_res["error"]
            logger.error("Failed to retrieve bot's user_id due to: {}"
                         .format(auth_test_error))
            raise Exception(EXCEPTION_DEFAULT_MSG)

    # TODO: extend handle_rtm_event() to handle different commands, such as "update-issue", "open-pr"
    def handle_rtm_event(self, event):
        """Processes and handles RTM events
        :param event: Slack RTM event
        :return: None
        """
        if "type" in event and event["type"] == "message" and "subtype" not in event:
            msg = event['text']
            channel = event["channel"]

            if SlackBot.is_bot_message(self.bot_user_id, msg):
                logger.info("Received a message "
                            "mentioning our bot: '{}'".format(msg))
                parsed_msg = SlackBot.parse_bot_message(msg)

                if parsed_msg["ok"]:
                    git_res = self.git_client.create_issue(parsed_msg["issue_title"],
                                                           parsed_msg["issue_body"])
                    if git_res["ok"]:
                        res = "GitHub issue created successfully: {}".format(git_res["link"])
                    else:
                        res = "Failed to create issue: {}".format(git_res["error"])
                else:
                    res = parsed_msg["error"]

                self.sc.rtm_send_message(channel, res)

    # TODO: change bot implementation to use events API so we can scale horizontally
    def start_bot(self):
        """Creates a connection to the RTM API and listens for events in an infinite loop
        :return: None
        """
        self.sc = SlackClient(self.slack_api_token)
        self.set_bot_user_id()

        if self.sc.rtm_connect(auto_reconnect=True):
            logger.info("Slack client connected to RTM API")
            while True:
                try:
                    slack_events = self.sc.rtm_read()
                except SlackNotConnected:
                    logger.error("Failed to read from RTM API, the connection "
                                 "may have been dropped")
                    raise

                for event in slack_events:
                    self.handle_rtm_event(event)
        else:
            logger.error("Slack client failed to connect to RTM API, this might"
                         "be due to an invalid API token or a connection issue")
            raise Exception(EXCEPTION_DEFAULT_MSG)
