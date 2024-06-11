from common import *
from gitlab import ProjectGitLabInfo, GroupGitLabInfo


# clone所有根目录下的项目
def clone_all_projects():
    gitlab = ProjectGitLabInfo(address=GITLAB_ADDR, token=GITLAB_TOKEN)
    gitlab.clone()


# clone某个组下的项目
def clone_group_projects(group_id: int):
    gitlab = GroupGitLabInfo(address=GITLAB_ADDR, token=GITLAB_TOKEN)
    gitlab.clone(group_id)


# 根据id clone所有项目
def clone_projects_by_ids(project_ids: list[int]):
    gitlab = ProjectGitLabInfo(address=GITLAB_ADDR, token=GITLAB_TOKEN)
    for project_id in project_ids:
        gitlab.clone(project_id)


clone_all_projects()

