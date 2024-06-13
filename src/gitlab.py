import json
import os
import shlex
import subprocess
import time
from abc import abstractmethod
from urllib.request import urlopen


class GitLabProjectBasicInfo:
    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path
        self.command = None

    def clone(self):
        if os.path.exists(self.path):
            self.command = shlex.split('git -C "%s" pull' % self.path)
        else:
            self.command = shlex.split('git clone %s %s ' % (self.url, self.path))

    @staticmethod
    def create(gitlab_api_json):
        if gitlab_api_json is None:
            raise Exception("")

    def run_async(self):
        self.clone()
        return subprocess.Popen(self.command)

    def run(self):
        self.clone()
        return subprocess.run(self.command)


class GitLabInfo:
    PER_PAGE = 100

    def __init__(self, address: str, token: str):
        self.address = address
        self.token = token

    @abstractmethod
    def get_raw_projects_json(self, id: int | None = None) -> list:
        pass

    @abstractmethod
    def url(self, id: int | None, page_index: int | None) -> str:
        pass

    def clone(self, id: int | None = None):
        gitlab_infos = self.clean_gitlab_infos(id)
        processes = []
        for index, project in enumerate(gitlab_infos):
            process = project.run_async()
            processes.append(process)

        time.sleep(10)
        # for process in processes:
        #     process.wait()
        print(f"下载完成，项目数量为{len(gitlab_infos)}")

    def clean_gitlab_infos(self, id: int | None = None) -> list[GitLabProjectBasicInfo]:
        gitlab_infos = []
        all_projects_json = self.get_raw_projects_json(id)
        for project in all_projects_json:
            if not project['archived']:
                url = project['http_url_to_repo']
                path = project['path_with_namespace']
                path="../project/"+path
                gitlab_info = GitLabProjectBasicInfo(url, path)
                gitlab_infos.append(gitlab_info)
        return gitlab_infos


class GroupGitLabInfo(GitLabInfo):
    def __init__(self, address: str, token: str):
        super().__init__(address, token)

    def get_sub_groups_json(self, id: int | None) -> list:
        all_projects_json = []
        if id is None:
            raise Exception("index不能为空")
        page_index = 1
        while True:
            page_projects = urlopen(self.sub_group_url(page_index=page_index, id=id))
            page_projects_json = json.loads(page_projects.read().decode())
            all_projects_json += page_projects_json
            if len(page_projects_json) == 0:
                break
            else:
                page_index += 1
        return all_projects_json

    def get_sub_projects_json(self, id: int | None) -> list:
        if id is None:
            raise Exception("index不能为空")
        page_group = urlopen(self.url(id=id, page_index=None))
        all_projects_json = json.loads(page_group.read().decode())['projects']
        return all_projects_json

    def get_raw_projects_json(self, id: int | None = None) -> list:
        if id is None:
            raise Exception("group_id不允许为空")
        all_sub_groups_json = self.get_sub_groups_json(id)
        all_sub_projects_json = self.get_sub_projects_json(id)
        if len(all_sub_projects_json) == 0:
            return []

        for group in all_sub_groups_json:
            group_id = group['id']
            all_sub_projects_json += self.get_raw_projects_json(group_id)
        return all_sub_projects_json

    def url(self, id: int | None, page_index: int | None) -> str:
        if id is None:
            raise Exception("group index不能为空")
        return (f"http://{self.address}/api/v4/groups/{id}?"
                f"private_token={self.token}"
                f"&per_page={GitLabInfo.PER_PAGE}")

    def sub_group_url(self, id: int | None, page_index: int | None) -> str:
        if id is None:
            raise Exception("group index不能为空")
        if page_index is None:
            raise Exception("page_index不能为空")
        return (f"http://{self.address}/api/v4/groups/{id}/subgroups?"
                f"private_token={self.token}"
                f"&per_page={GitLabInfo.PER_PAGE}"
                f"&page={page_index}")


class ProjectGitLabInfo(GitLabInfo):
    def __init__(self, address: str, token: str):
        super().__init__(address, token)

    def get_raw_projects_json(self, id: int | None = None) -> list:
        all_projects_json = []
        if id is None:
            page_index = 1
            while True:
                page_projects = urlopen(self.url(page_index=page_index, id=id))
                page_projects_json = json.loads(page_projects.read().decode())
                all_projects_json += page_projects_json
                if len(page_projects_json) == 0:
                    break
                else:
                    page_index += 1
            return all_projects_json
        else:
            page_projects = urlopen(self.url(page_index=None, id=id))
            page_projects_json = json.loads(page_projects.read().decode())
            all_projects_json += page_projects_json
            return all_projects_json

    def url(self, id: int | None, page_index: int | None) -> str:
        if id is None and page_index is not None:
            return (f"http://{self.address}/api/v4/projects?"
                    f"private_token={self.token}"
                    f"&per_page={GitLabInfo.PER_PAGE}"
                    f"&page={page_index}")
        elif id is not None:
            return (f"http://{self.address}/api/v4/projects/{id}?"
                    f"private_token={self.token}"
                    f"&per_page={GitLabInfo.PER_PAGE}")
        else:
            raise Exception("error")
