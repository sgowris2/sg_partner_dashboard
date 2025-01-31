from typing import List
from social_account import SocialAccount


class Partner:

    def __init__(self, name: str, description: str):
        self.name = name
        self.desc = description
        self.locations = []
        self.social_accounts = []

    def add_location(self, lat, lon):
        if True:    # TODO: Check if the lat, lon is valid
            self.locations.append((lat, lon))

    def add_social_account(self, social_account: SocialAccount):
        if True:    # TODO: Check if the social account is accessible
            self.social_accounts.append(social_account)
