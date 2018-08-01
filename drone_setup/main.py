#!/usr/bin/env python3

import os
import yaml
import click
from os.path import abspath, expanduser
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DroneSetup():

    def __init__(self, config, server, token):

        self.config = config
        self.server = server
        self.token = token

        self.owner = self.config["owner"]
        self.repo = self.config["repo"]
        self.settings = self.config.get("settings", {})
        self.secrets = self.config.get("secrets", {})


    def api(self, method, path, **kwargs):
        return requests.request(method, f'{self.server}{path}',
                                params=dict(access_token=self.token),
                                **kwargs)


    def configure(self):
        owner = self.owner
        repo = self.repo

        logger.info(f"Update settings: {self.settings}")
        self.api("PATCH", f"/api/repos/{owner}/{repo}", json=self.settings)

        #Flush all secrets
        for secret in self.api("GET", f"/api/repos/{owner}/{repo}/secrets").json():
            secret = secret['name']
            logger.info(f"delete secret {secret}")
            self.api("DELETE", f"/api/repos/{owner}/{repo}/secrets/{secret}")

        # Inject secrets
        for name, value in self.secrets.items():
            logger.info(f"create secret {name}")
            result = self.api("POST", f"/api/repos/{owner}/{repo}/secrets",
                              json=dict(name=name, value=value))


def load_config(config_file):
    with open(expanduser(config_file), 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config


@click.command()
@click.argument('config_file', default=".drone.setup.yml")
def main(config_file):

    server = os.getenv("DRONE_SERVER")
    token = os.getenv("DRONE_TOKEN")
    dronesetup = DroneSetup(config=load_config(config_file), server=server, token=token)

    dronesetup.configure()

main()