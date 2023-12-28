from __future__ import print_function # Python 2/3 compatibility
import abc
import os


class MyEnvironment(object):

    """
    Environment Setting provider
    ~~~~~~~~~~~~~~~~~~~~~
    :SkillName

    :TwilioSid
    :TwilioToken
    :TwilioCID
    :AdminTwilioSid
    :AdminTwilioToken
    :AdminTwilioCID

    :SlackToken
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._environment_value = ''
        if 'Environment' in os.environ:
            self._environment_value = os.environ['Environment']

    def get_environment(self):
        return self._environment_value

    def get_environment_variable(self, _name, _default):
        # type: (object, object) -> object
        return os.environ[_name] if _name in os.environ else _default

    def get_skill_name(self):
        return os.environ['SkillName'] if 'SkillName' in os.environ else 'Alexa Skill'

    def get_twilio_account_sid(self):
        return os.environ['TwilioSid'] if 'TwilioSid' in os.environ else ''

    def get_twilio_auth_token(self):
        return os.environ['TwilioToken'] if 'TwilioToken' in os.environ else ''

    def get_twilio_cid_number(self):
        return os.environ['TwilioCID'] if 'TwilioCID' in os.environ else ''

    def get_admin_twilio_account_sid(self):
        return os.environ['AdminTwilioSid'] if 'AdminTwilioSid' in os.environ else self.get_twilio_account_sid()

    def get_admin_twilio_auth_token(self):
        return os.environ['AdminTwilioToken'] if 'AdminTwilioToken' in os.environ else self.get_twilio_auth_token()

    def get_admin_twilio_cid_number(self):
        return os.environ['AdminTwilioCID'] if 'AdminTwilioCID' in os.environ else self.get_twilio_cid_number()

    def get_slack_token(self):
        return os.environ['SlackToken'] if 'SlackToken' in os.environ else ''

    def get_voicelabs_token(self):
        return os.environ['VoicelabsToken'] if 'VoicelabsToken' in os.environ else None

    def get_fb_page_access_token(self):
        return os.environ['FBPageAccessToken'] if 'FBPageAccessToken' in os.environ else None

    def get_fb_verify_token(self):
        return os.environ['FBVerifyToken'] if 'FBVerifyToken' in os.environ else None

    def get_log_level(self):
        return os.environ['LogLevel'].lower() if 'LogLevel' in os.environ else 'notset'
