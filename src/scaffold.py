import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from src.repository import (
    clone_git_repository,
    get_author,
    create_git_repository,
    is_git_repo,
    update_git_repository,
    get_git_origin,
)
from src.licenses import create_license
from src.templates import Template
from utils.file_utils import (
    find_and_replace_in_directory,
)
from utils.str_utils import check_str_or_int
from utils.parser import *
from src.constants import *
import shutil


def create_from_template(
    template_directory: str = template_directory,
    destination_directory: str = destination_directory,
    store_template: bool = store_template,
):
    if not destination_directory:
        destination_directory = os.path.join(
            os.getcwd(), os.path.basename(template_directory)
        )

    templ = Template.get_template(template_directory)
    templ: Template

    if templ is None:
        raise ValueError(f"Template '{template_directory}' does not exist.")

    # add newly created template to db if store_template is true
    if store_template:
        templ.add_template(destination_directory)
    else:
        templ.copy_template(destination_directory)

    return destination_directory, templ.template_name


def scaffold_repository(
    git_origin: str,
    create_repository: bool = create_repository,
    repository_visibility: int = repository_visibility,
):
    if not create_repository:
        return

    # initialize project directory
    is_git_repo = is_git_repo(destination_directory)
    if not is_git_repo:
        create_git_repository(git_origin, repository_visibility)
    else:
        update_git_repository(git_origin, repository_visibility, destination_directory)

    return is_git_repo


def scaffold(
    template_directory: str = template_directory,
    destination_directory: str = destination_directory,
    repository_name: str = repository_name,
    license: str = license,
    author: str = author,
    year: str = year,
    create_repository: bool = create_repository,
    clone_repository: bool = clone_git_repository,
    store_template: bool = store_template,
    repository_visibility: str = repository_visibility,
):

    if not repository_name:
        repository_name = os.path.basename(destination_directory)

    destination_directory, template_name = create_from_template(
        template_directory,
        destination_directory,
        store_template,
    )

    print(f"Replacing all instances of '{template_name}' with '{repository_name}'.")
    find_and_replace_in_directory(
        destination_directory, template_name, repository_name, removed_dirs=[".git"]
    )

    create_license(license, destination_directory, author, year)

    author = get_author(author)
    git_origin = get_git_origin(author, repository_name)

    scaffold_repository(
        git_origin,
        create_repository,
        repository_visibility,
    )

    # clone repository
    if clone_repository:
        shutil.rmtree(destination_directory, ignore_errors=True)
        clone_repository(git_origin, cwd=os.getcwd())


def main():

    parser_arguments = [
        Argument(name=("-t", "--template_directory"), default=template_directory),
        DirectoryArgument(
            name=("-d", "--destination_directory"), default=destination_directory
        ),
        Argument(name=("-n", "--repository_name"), default=repository_name),
        BoolArgument(name=("-c", "--create_repository"), default=create_repository),
        BoolArgument(name=("-cl", "--clone_repository"), default=clone_repository),
        BoolArgument(name=("-s", "--store_template"), default=store_template),
        Argument(name=("-l", "--license"), default=license),
        Argument(name=("-a", "--author"), default=author),
        Argument(name=("-y", "--year"), default=year),
        Argument(
            name=("-v", "--repository_visibility"),
            type=check_str_or_int,
            choices=[0, 1, 2, "private", "public", "internal"],
            default=repository_visibility,
        ),
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()
    # scaffold(**args)


if __name__ == "__main__":
    main()
