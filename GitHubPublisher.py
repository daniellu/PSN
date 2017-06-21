# Author DL

from github import Github
from github import InputGitTreeElement

class GitHubPublisher(object):
    def __init__(self, username, password, repo):
        self.username = username
        self.password = password
        self.repo = repo

    def publish(self, filename):
        g = Github(self.username, self.password)
        repo = g.get_user().get_repo(self.repo)
        file_list = [filename]
        commit_message = 'Add spider result'
        master_ref = repo.get_git_ref('heads/master')
        master_sha = master_ref.object.sha
        base_tree = repo.get_git_tree(master_sha)
        element_list = list()
        for entry in file_list:
            with open(entry, 'r') as input_file:
                data = input_file.read()
            element = InputGitTreeElement(entry, '100644', 'blob', data)
            element_list.append(element)
        tree = repo.create_git_tree(element_list, base_tree)
        parent = repo.get_git_commit(master_sha)
        commit = repo.create_git_commit(commit_message, tree, [parent])
        master_ref.edit(commit.sha)
        """ An egregious hack to change the PNG contents after the commit """
        for entry in file_list:
            with open(entry, 'rb') as input_file:
                data = input_file.read()
            if entry.endswith('.png'):
                old_file = repo.get_contents(entry)
                commit = repo.update_file('/' + entry, 'Update PNG content', data, old_file.sha)