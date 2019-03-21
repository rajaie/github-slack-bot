import unittest
from unittest import mock
from github_slack_bot.utils.slack import SlackBot
import logging
logging.disable(logging.CRITICAL)


class TestSlackBot(unittest.TestCase):
    def test_is_bot_mention(self):
        """Is a message mentioning our bot's user_id correctly detected?"""
        bot_user_id = "UH17NTLPP"

        message = "<@UH17NTLPP> Hello bot here is a message"
        self.assertTrue(SlackBot.is_bot_mention(bot_user_id, message))

    def test_is_bot_mention_different_user_id(self):
        """Is mentioning a different user_id detected as a mention of our bot?"""
        bot_user_id = "UH17NTLPP"
        message = "<@XI384LOEL> Hello bot here is a message"
        self.assertFalse(SlackBot.is_bot_mention(bot_user_id, message),
                         "This message mentions another Slack user_id")

    def test_is_bot_mention_no_user_id(self):
        """Make sure a mention of our bot's user_id is followed by a space"""
        bot_user_id = "UH17NTLPP"
        message = "<@UH17NTLPP>Hello bot here is a message"
        self.assertFalse(SlackBot.is_bot_mention(bot_user_id, message),
                         "Bot user_id must be followed by a space")

    def test_parse_bot_message(self):
        message = "<@XI384LOEL> Issue title here__Issue body here"
        self.assertDictEqual(SlackBot.parse_bot_message(message), {
            "ok": True,
            "issue_title": "Issue title here",
            "issue_body": "Issue body here"
        })

    def test_parse_bot_message_empty_body(self):
        message = "<@XI384LOEL> Issue title here__"
        self.assertDictEqual(SlackBot.parse_bot_message(message), {
            "ok": True,
            "issue_title": "Issue title here",
            "issue_body": ""
        })

    def test_parse_bot_message_malformed_body(self):
        message = "random text here"
        res = SlackBot.parse_bot_message(message)
        self.assertFalse(res["ok"], "Failed parse must set 'ok' key of result to False")
        self.assertTrue("error" in res, "Failed parse must return an error message")

    @mock.patch('github_slack_bot.utils.slack.SlackClient')
    def test_slack_bot_constructor(self, sc):
        bot_user_id = "UH17NTLPP"
        sc.return_value.api_call.return_value = {"ok": True, "user_id": bot_user_id}

        slackbot = SlackBot("slack_api_token", "git_client")

        sc.return_value.api_call.assert_called_once_with("auth.test")
        self.assertEqual(bot_user_id, slackbot.bot_user_id)


if __name__ == "__main__":
    unittest.main()
