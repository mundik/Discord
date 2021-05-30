"""
import base64
from github import Github


# First create a Github instance:

# using an access token
g = Github("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")


# Then play with your Github objects:
repo = g.get_user().get_repo("Discord")
contents = repo.get_contents("")
print(contents)
"""
from github import Github

g = Github("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")
repo = g.get_user().get_repo("Discord")


def new_commit(file_path):
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

    with open(file_path, 'r') as file:
        content = file.read()

    # Upload to github
    git_file = file_path
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED')

new_commit('Git_update.py')
