from github import Github

g = Github("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")
repo = g.get_user().get_repo("Discord")


def new_commit(file):
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))
    with open(file, 'r') as _file:
        content = _file.read()
    git_file = file
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED')