import json
import os
import shlex
import subprocess
import time
from abc import abstractmethod

from gitlab_clone.util import get_json_by_url


class GitLabProjectBasicInfo:
    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path

    def clone(self):
        if os.path.exists(self.path):
            return shlex.split('git -C "%s" pull' % self.path)
        else:
            return shlex.split('git clone %s %s ' % (self.url, self.path))

    def run_async(self):
        return subprocess.Popen(self.clone())

    def run(self):
        return subprocess.run(self.clone())


class GitLabInfo:
    PER_PAGE = 100

    def __init__(self, address: str, token: str, store_path: str | None = "../project/"):
        self.address = address
        self.token = token
        self.store_path = store_path

    @abstractmethod
    def get_all_project_json(self, id: int | None = None) -> list:
        pass

    @abstractmethod
    def url(self, id: int | None = None, page_index: int | None = None) -> str:
        pass

    def clone(self, id: int | None = None):
        gitlab_infos = self.get_gitlab_infos(id)
        processes = []
        for index, project in enumerate(gitlab_infos):
            process = project.run_async()
            processes.append(process)

        time.sleep(10)
        # for process in processes:
        #     process.wait()
        print(f"下载完成，项目数量为{len(gitlab_infos)}")

    def get_gitlab_infos(self, id: int | None = None) -> list[GitLabProjectBasicInfo]:
        gitlab_infos = []
        all_projects_json = self.get_all_project_json(id)
        for project in all_projects_json:
            if not project['archived']:
                url = project['http_url_to_repo']
                path = project['path_with_namespace']
                store_path = self.store_path + path
                gitlab_info = GitLabProjectBasicInfo(url, store_path)
                gitlab_infos.append(gitlab_info)
        return gitlab_infos


class GroupGitLabInfo(GitLabInfo):
    def __init__(self, address: str, token: str, store_path: str | None = None):
        super().__init__(address, token, store_path)

    def get_sub_groups_json(self, id: int | None) -> list:
        all_projects_json = []
        if id is None:
            raise Exception("index不能为空")
        page_index = 1
        while True:
            page_projects_json = get_json_by_url(self.sub_group_url(page_index=page_index, id=id))
            all_projects_json += page_projects_json
            if len(page_projects_json) == 0:
                break
            else:
                page_index += 1
        return all_projects_json

    def get_sub_projects_json(self, id: int | None) -> list:
        if id is None:
            raise Exception("index不能为空")
        all_projects_json = get_json_by_url(self.url(id=id, page_index=None))
        return all_projects_json

    def get_all_project_json(self, id: int | None = None) -> list:
        if id is None:
            raise Exception("group_id不允许为空")
        all_sub_groups_json = self.get_sub_groups_json(id)
        all_sub_projects_json = self.get_sub_projects_json(id)
        if len(all_sub_projects_json) == 0:
            return []

        for group in all_sub_groups_json:
            group_id = group['id']
            all_sub_projects_json += self.get_all_project_json(group_id)
        return all_sub_projects_json

    def url(self, id: int | None = None, page_index: int | None = None) -> str:
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
    def __init__(self, address: str, token: str, store_path: str | None = None):
        super().__init__(address, token, store_path)

    def get_all_project_json(self, id: int | None = None) -> list:
        all_projects_json = []
        if id is None:
            page_index = 1
            while True:
                page_projects_json = get_json_by_url(self.url(page_index=page_index, id=id))
                all_projects_json += page_projects_json
                if len(page_projects_json) == 0:
                    break
                else:
                    page_index += 1
            return all_projects_json
        else:
            page_projects_json = get_json_by_url(self.url(page_index=None, id=id))
            all_projects_json += page_projects_json
            return all_projects_json

    def url(self, id: int | None = None, page_index: int | None = None) -> str:
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
