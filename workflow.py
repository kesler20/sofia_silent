from mimetypes import init
import sys
import os
import time
import json
from interfaces.os_interface import OperatingSystemInterface

osi = OperatingSystemInterface()
user_directory = osi.gcu()

class AmplifyApplication(object):

    def __init__(self) -> None:
        self.credential_location = os.path.join(osi.gcu(),"Onedrive","Documents", "new_user_credentials.csv") 
        self.categories = ["notifications", 'api', 'auth', 'custom', 'storage', 'analytics', 'function', 'geo', 'hosting', 'interactions', 'predictions', 'xr']
    
    def modify_amplify_application(self,categoryID):
        category = self.categories[int(categoryID)]
        os.system(
            r"start excel {}".format(self.credential_location))
        os.system(f"amplify add {category}")
        os.system("amplify status")
        os.system("amplify push")
        os.system("amplify publish")
        os.system("amplify pull")
    
    def import_amplify_application(self):
        pass

    def initialize_amplify_application(self, categoryID: int):
        category = self.categories[int(categoryID)]
        os.system(
            r"start excel {}".format(self.credential_location))
        os.system("amplify init")
        os.system(f"amplify add {category}")
        os.system("amplify status")
        os.system("amplify push")
        os.system("amplify publish")
        os.system("amplify pull")

    def sync_env_variable_to_aws_exports(self):
        AWS_CONFIG_DATA = []

        source_dir = os.path.join(os.getcwd(), "src")
        print(f"----------- looking for the aws-exports.js in {source_dir} 🔎")
        time.sleep(1)
        with open(f"{source_dir}/aws-exports.js", "r") as aws_config_file, open(f"{os.getcwd()}/aws-exports.json", "w") as write_file:
            content = aws_config_file.readlines()

            print("-------------------------- aws-export.js found ✅")
            print(aws_config_file.read())
            time.sleep(1)
            # filter the first three lines
            clean_content = list(
                filter(lambda line: content.index(line) > 3, content))
            clean_content.insert(0, "[{")

            # filter the last two lines
            clean_content = list(filter(lambda line: clean_content.index(
                line) < len(clean_content) - 2, clean_content))
            clean_content.append("}]")

            print("--------------------- cleaning up the file to make a json 🧹")
            time.sleep(1)

            for index, line in enumerate(clean_content):
                write_file.write(line)

        with open(f"{os.getcwd()}/aws-exports.json", "r") as read_config_file:
            content: 'list[dict]' = json.loads(read_config_file.read())
            keys = list(content[0].keys())

            print(
                f"----------------------- converting the parsed dictionary to .env variables ⚙️")
            time.sleep(1)
            print(content[0])

            print("------------------------  ---> ")
            for k in keys:
                upper_k = k.upper()
                AWS_CONFIG_DATA.append(f'REACT_APP_{upper_k} = "{content[0][k]}"')
            print(f'REACT_APP_{upper_k} = "{content[0][k]}"')

        print("------------------------------- getting the current .env file ✅")
        time.sleep(1)
        with open(".env", "r+") as env_file:
            content = env_file.readlines()
            clean_content = list(
                filter(lambda line: line.find("REACT_APP_AWS") == -1, content))
            for line in clean_content:
                print(line)

            for variable in AWS_CONFIG_DATA:
                clean_content.append(variable)

        print("---------------------------- writing to the final .env file ✏️")
        time.sleep(1)
        with open(".env", "w") as write_to_env_file:
            clean_content = list(set(clean_content))
            for line in clean_content:
                line = line.replace("\n", "")
                print(line)
                write_to_env_file.write(f'{line}\n')
            os.remove("aws-exports.json")
    
    def push_to_amplify(target_directory: str):
        '''
        In order to publish to amplify make sure that you have initialised the correct application
        and that the repository is bering configure

        According to the documentation after adding the hosting category you can commit by running amplify push
        ---
        ```cmd
        amplify push
        ```
        '''
        print(f"------------- cd into --> {target_directory} 🚕")
        os.chdir(target_directory)
        print("------------ running tests using npm 🧪")
        os.system("npm test")
        time.sleep(1)
        print("------------ formatting code using prettier ✨")
        os.system("prettier -w .")
        time.sleep(1)
        print("------------ the tests have passed so we can push to github ✅")
        time.sleep(1)
        os.system("git pull")
        os.system("git add . ")
        os.system('git commit -m "make it better"')
        time.sleep(1)
        os.system("git push ")
        print("------------ publishing the application to amplify ✅")
        os.system("amplify publish")
        os.system("------------ workflow completed successfully ✅")
    
class ReactApplication(object):

    def __init__(self) -> None:
        pass

    def initialise_env_file(self):
        pass

    def add_mqtt_library(self):
        pass

def push_to_heroku(backend_directory: str, commit_message: str):
    '''
    This script can be used to deploy the backend to heroku automatically

    from the documentation we need the following commands to push 
    see the documentation here https://dashboard.heroku.com/apps/journal-back-end/deploy/heroku-git
    -----
    ```git
    $ git add .
    $ git commit -am "make it better"
    $ git push heroku master
    ```
    '''
    os.chdir(backend_directory)
    os.system("python -m pytest")
    os.system("prettier -w .")
    os.system("git pull")
    os.system("git add . ")
    os.system('git commit -m "make it better"')
    os.system("git push ")
    os.system("git add .")
    os.system(f"git commit -am {commit_message}")
    os.system("git push heroku master")


def push_to_github(target_directory):
    print(f"------------- cd into --> {target_directory} 🚕")
    os.chdir(target_directory)
    print("------------ running tests using npm 🧪")
    os.system("npm test")
    print("------------ the tests have passed so we can push to github ✅")
    os.system("git pull")
    os.system("git add . ")
    os.system('git commit -m "make it better"')
    os.system("git push ")
    print("------------ publishing the application to amplify ✅")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "publish":
            push_to_amplify(os.getcwd())
        if sys.argv[1] == "sync":
            sync_env_variable_to_aws_exports()
        if sys.argv[1] == "init amplify":
            initialize_amplify_application(sys.argv[2])

    else:
        push_to_github(os.getcwd())
