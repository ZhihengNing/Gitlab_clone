# git-clone

本项目提供Python脚本用于下载gitlab中的项目资源文件

## 要求

python版本大于等于3.10

## 运行

在`common.py`自定义Gitlab的token和address信息

```
# gitlab上的token
GITLAB_TOKEN = 'xxxxxxxxxxxxxxx'
# 项目地址
GITLAB_ADDR = '127.0.0.1:8080/root'
```

用户可根据项目需求在`main.py`里调用相应函数（下面是clone根目录下所有项目的代码示例）

```python
# clone根目录下所有项目
def clone_all_projects():
    gitlab = ProjectGitLabInfo(address=GITLAB_ADDR, token=GITLAB_TOKEN)
    gitlab.clone()


# clone某个组下所有项目
def clone_group_projects(group_id: int):
    gitlab = GroupGitLabInfo(address=GITLAB_ADDR, token=GITLAB_TOKEN)
    gitlab.clone(group_id)


# 根据id clone所有项目
def clone_projects_by_ids(project_ids: list[int]):
    gitlab = ProjectGitLabInfo(address=GITLAB_ADDR, token=GITLAB_TOKEN)
    for project_id in project_ids:
        gitlab.clone(project_id)
        
clone_all_projects()

```

```shell
python main.py
```

