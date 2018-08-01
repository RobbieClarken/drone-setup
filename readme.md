# Drone-setup

With Drone CI, you define your pipelines in `.drone.yml`.

But to read your pipeline, your repo needs to be enabled and configured on your Drone server.

Let's define this configuration in `drone.setup.yml`, and version track this config.

# Install
```
pip install .
```

Setup your `DRONE_SERVER` and `DRONE_TOKEN` environment variables from:

https://your-drone-server/account/token

# Example
Write a `.drone.setup.yaml` file:
```
owner: MYORG
repo: MYREPO
settings:
    allow_pr: false
    allow_push: true
    allow_deploys: false
    allow_tags: false
    trusted: true
secrets:
    slack_webhook: https://hooks.slack.com/services/kdjfhgdf8g7dfigj8fdg/dfgjndfg87dfg787
```

Apply this configuration:
```
drone-setup [.drone.setup.yml]
```

# Encryption
Use [sops](https://github.com/mozilla/sops) to encrypt your sensitive .drone.setup.yml.

Edit your encrypted file:
```
sops .drone.setup.yml
```

Apply this configuration:
```
drone-setup <( sops -d {.drone.setup.yml} )
```
