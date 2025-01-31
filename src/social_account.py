from abc import ABC, abstractmethod
import json
import os
import uuid


class SocialAccountRegistry:

    REGISTRY_DIR = '../social_account_registry'

    @staticmethod
    def get_all_accounts():
        account_files = [x for x in os.listdir(SocialAccountRegistry.REGISTRY_DIR) if x.endswith('.json')]
        return [SocialAccountFactory.build(os.path.join(SocialAccountRegistry.REGISTRY_DIR, x)) for x in account_files]


class SocialAccount(ABC):

    @staticmethod
    def register_account(account_info: dict):
        account_file = '.'.join([uuid.uuid4(), 'json'])
        account_info['posts'] = []
        with open(os.path.join(SocialAccountRegistry.REGISTRY_DIR, account_file), 'w') as f:
            json.dump(account_info, f)

    @abstractmethod
    def test_connection(self):
        pass

    @abstractmethod
    def get_new_posts(self, since_timestamp: int):
        pass


class SocialAccountFactory:

    @staticmethod
    def build(account_file_path):
        with open(account_file_path, 'r') as f:
            data = json.load(f)
            data = data.get('account_info', None)
            if None:
                raise Exception('Account info not found for account at path {}'.format(account_file_path))
            else:
                channel = data.get('channel', None)
                if channel is None:
                    raise Exception('Channel is null for account at path {}'.format(account_file_path))
                elif channel == 'linkedin':
                    return LinkedInAccount(data)
                elif channel == 'instagram':
                    return InstagramAccount(data)
                elif channel == 'facebook':
                    return FacebookAccount(data)
                elif channel == 'twitter':
                    return TwitterAccount(data)
                else:
                    raise Exception('Valid channel not found for account at path {}'.format(account_file_path))


class LinkedInAccount(SocialAccount):
    def __init__(self, account_info):
        self.channel = 'linkedin'
        self.name = account_info.get('name')


class FacebookAccount(SocialAccount):
    pass


class InstagramAccount(SocialAccount):
    pass


class TwitterAccount(SocialAccount):
    pass