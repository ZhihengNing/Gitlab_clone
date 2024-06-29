# git-clone

本项目提供Python脚本用于下载gitlab中的项目资源文件

## 要求

python版本大于等于3.10

## 运行

在`git_clone_test`包下找到`config`文件夹，在`config-template.json`中填写Gitlab的token和address字段（其中token可以在访问令牌中添加），并将其重命名为`config.json`

![image-20240604171025245](./README.assets/image-20240604171025245.png)

```json
{
  "gitlabToken": "xxxxxxxxxxxxxxx",
  "gitlabAddress":"127.0.0.1:8080"
}
```

根据项目需求在`main.py`里调用相应函数

下面是clone根目录下所有项目的代码示例：

```python
gitlab = read_json('./config/config.json')

# gitlab上的token
GITLAB_TOKEN = gitlab['gitlabToken']
# 项目地址
GITLAB_ADDR = gitlab['gitlabAddress']

if __name__ == '__main__':
    gitlab_client = GitlabClient(token=GITLAB_TOKEN, address=GITLAB_ADDR)
    # clone全部项目到../project/文件夹中
    gitlab_client.clone_all_projects("../project/")

```

ps：根据id clone（clone_projects_by_ids）项目能有效节约计算机的进程资源，建议不要使用clone_all_projects方法

运行`main.py`

```python
cd git_clone_test
python main.py
```

