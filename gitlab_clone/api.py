from .gitlab import ProjectGitLabInfo, GroupGitLabInfo


class GitlabClient:
    def __init__(self, address: str, token: str):
        self.path = None
        if address is None or token is None:
            raise ValueError('address and token must be specified')
        self.address = address
        self.token = token

    def set_store_path(self, path: str):
        self.path = path

    # clone所有根目录下的项目
    def clone_all_projects(self, path: str | None = None):
        ProjectGitLabInfo(address=self.address, token=self.token, store_path=path).clone()

    # clone某个组下的项目
    def clone_group_projects(self, group_ids: list[int], path: str | None = None):
        if group_ids is None:
            raise ValueError('group_ids must be specified')

        gitlab = GroupGitLabInfo(address=self.address, token=self.token, store_path=path)
        for group_id in group_ids:
            gitlab.clone(group_id)

    # 根据id clone所有项目
    def clone_projects_by_ids(self, project_ids: list[int], path: str | None = None):
        if project_ids is None:
            raise ValueError('project_ids must be specified')

        gitlab = ProjectGitLabInfo(address=self.address, token=self.token, store_path=path)
        for project_id in project_ids:
            gitlab.clone(project_id)
