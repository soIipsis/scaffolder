import unittest
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parent_directory) 

from templates.python_template.tests.test_base import TestBase, run_test_methods

from src.scaffold import *
from src.update import *
from src.settings import *
from src.licenses import *
from src.constants import *

from templates.python_template.utils.file_operations import overwrite_file

licenses = ['mit', 'afl-3.0']
target_directory = os.getcwd()
author = 'soIipsis'

class TestScaffolder(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.template_directory = template_directory
        self.project_directory = project_directory
        self.license = license
        self.author = author
        self.git_username = git_username
        self.create_repository = create_repository
        self.repository_visibility = repository_visibility
        self.parameters = ['template_directory', 'license']

        self.update_source_directory = update_source_directory
        self.update_destination_directory = update_destination_directory
        self.update_files = update_files

        self.test_files_dir = self.get_test_files_dir()
        self.test_files_dir_2 = self.get_test_files_2_dir()

    def get_test_files_dir(self):
        return os.path.join(os.getcwd(), 'test_files')
    
    def get_test_files_2_dir(self):
        return os.path.join(os.getcwd(), 'test_files2')

    def test_get_licenses(self):
        paths = get_licenses(licenses)
        self.assertTrue(len(paths) > 0)

        new_licenses = ['red']
        with self.assertRaises(FileNotFoundError):
            paths = get_licenses(new_licenses)

    def test_view_license(self):
        # test singular
        paths = view_license('mit')
        self.assertTrue(len(paths) > 0)

        # test multiple
        paths = view_license(licenses)
        self.assertTrue(len(paths) > 0)

        # test invalid license
        paths = view_license(['no'])
        self.assertTrue(len(paths) == 0)

    def test_create_license(self):
        license = 'mit'
        path = create_license(license=license, target_directory=target_directory, author=author)
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))

    def test_scaffold_local(self):
        self.create_repository = False
        self.repository_visibility = 0
        scaffold(self.template_directory, self.project_directory, self.license, self.author, self.git_username, self.create_repository, self.repository_visibility)
        self.assertTrue(os.path.exists(self.project_directory))

    def test_scaffold(self):
        self.create_repository = True
        self.repository_visibility = 1
        scaffold(self.template_directory, self.project_directory, self.license, self.author, self.git_username, self.create_repository, self.repository_visibility)

    def test_update(self):
        update(self.update_files, self.update_source_directory, self.update_destination_directory)

    def test_find_and_replace_in_directory(self):
        # create a file called red.txt with some text
        file_path = os.path.join(self.test_files_dir, "red.txt")
        file_content =  "hello red"
        overwrite_file(file_path, file_content)

        content = read_file(file_path)
        self.assertTrue(file_content == content)
        find_and_replace_in_directory(self.test_files_dir, "red", "blue")


    def test_settings(self):
        settings = list_settings(self.parameters)
        self.assertIsNotNone(settings)
        self.assertListEqual(list(settings.keys()), self.parameters)

if __name__ == "__main__":
    run_test_methods(TestScaffolder.test_find_and_replace_in_directory)