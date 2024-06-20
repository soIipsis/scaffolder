import os
import subprocess

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from src.repository import (
    get_repository_visibility,
    create_git_repository,
    git_repo_exists,
    update_git_repository,
    rename_repo,
)
from src.licenses import create_license
from src.templates import get_template_directory
from utils.file_utils import (
    find_and_replace_in_directory,
)
from utils.parser import *
from src.constants import *


def scaffold(
    template: str = template_directory,
    destination_directory: str = destination_directory,
    project_name: str = project_name,
    license: str = license,
    author: str = author,
    year: str = year,
    git_username: str = git_username,
    create_repository: bool = create_repository,
    repository_visibility: str = repository_visibility,
):
    template_directory = get_template_directory(template)

    if not os.path.exists(destination_directory):
        subprocess.run(["mkdir", destination_directory], errors=None)
        create_license(license, destination_directory, author, year)
        create_template(template_directory, destination_directory)
    else:
        # path already exists, so update based on metadata
        create_license(license, destination_directory, author, year)

        if project_name:
            original_name = os.path.basename(destination_directory)
            rename_repo(destination_directory, project_name, git_username)
            find_and_replace_in_directory(
                destination_directory, original_name, project_name, [".git"]
            )

    if not create_repository:
        return

    repository_visibility = get_repository_visibility(repository_visibility)
    git_username = (
        git_username
        or subprocess.run(
            ["git", "config", "user.name"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()
    )

    # initialize project directory
    if not (git_repo_exists(destination_directory)):
        create_git_repository(
            destination_directory, repository_visibility, git_username
        )
    else:
        print("Project already exists. Updating...")
        update_git_repository(
            destination_directory, repository_visibility, git_username
        )


def create_template(template_directory: str, destination_directory: str):

    project_name = os.path.basename(destination_directory)

    # copy template directory to project directory
    print(
        "Copying template files from {0} to {1}".format(
            template_directory, destination_directory
        )
    )

    command = f"cp -r {template_directory}/* {destination_directory}/"
    subprocess.run(command, shell=True)

    # get template project name
    template_name = os.path.split(template_directory)[-1]

    # find and replace all instances of template_name
    find_and_replace_in_directory(
        destination_directory, template_name, project_name, removed_dirs=[".git"]
    )


def main():

    parser_arguments = [
        Argument(name=("-t", "--template")),
        DirectoryArgument(name=("-d", "--destination_directory")),
        Argument(name=("-n", "--project_name")),
        BoolArgument(name=("-c", "--create_repository")),
        Argument(name=("-l", "--license")),
        Argument(name=("-a", "--author")),
        Argument(name=("-y", "--year")),
        Argument(name=("-g", "--git_username")),
        Argument(name=("-v", "--repository_visibility"), type=int, choices=[0, 1, 2]),
    ]
    parser = Parser(parser_arguments)

    args = parser.get_command_args()

    scaffold(**args)


if __name__ == "__main__":
    main()
