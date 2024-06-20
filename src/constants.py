import datetime
import os
import pprint

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from utils.json_utils import read_json_file

scaffolder_data_path = f"{parent_directory}/data/scaffolder.json"
scaffolder_metadata = read_json_file(scaffolder_data_path)
scaffolder_metadata: dict


languages_path = f"{parent_directory}/data/languages.json"
languages_metadata = read_json_file(languages_path)
languages_metadata: dict

# scaffolder metadata
template_directory = scaffolder_metadata.get("template_directory")
destination_directory = scaffolder_metadata.get("destination_directory")
project_name = scaffolder_metadata.get(
    "project_name", os.path.basename(destination_directory)
)
update_source_directory = scaffolder_metadata.get("update_source_directory")
update_destination_directory = scaffolder_metadata.get("update_destination_directory")
update_files = scaffolder_metadata.get("update_files")
license = scaffolder_metadata.get("license")
author = scaffolder_metadata.get("author")
year = scaffolder_metadata.get("year", str(datetime.datetime.now().year))
git_username = scaffolder_metadata.get("git_username")
create_repository = scaffolder_metadata.get("create_repository")
repository_visibility = scaffolder_metadata.get("repository_visibility")
gh_check = scaffolder_metadata.get("gh_check")
licenses_directory = f"{parent_directory}/data/licenses"
pp = pprint.PrettyPrinter(indent="3")
