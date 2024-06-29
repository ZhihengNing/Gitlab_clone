from git_clone_test.util import read_json
from gitlab_clone import GitlabClient

gitlab = read_json('./config/config.json')

# gitlab上的token
GITLAB_TOKEN = gitlab['gitlabToken']
# 项目地址
GITLAB_ADDR = gitlab['gitlabAddress']

if __name__ == '__main__':
    gitlab_client = GitlabClient(token=GITLAB_TOKEN, address=GITLAB_ADDR)
    # clone全部项目到../project/文件夹中
    gitlab_client.clone_all_projects("../project/")
