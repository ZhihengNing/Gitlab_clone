from util import read_json

gitlab = read_json('../config/config.json')

# gitlab上的token
GITLAB_TOKEN = gitlab['gitlabToken']
# 项目地址
GITLAB_ADDR = gitlab['gitlabAddress']
