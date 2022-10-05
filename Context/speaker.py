import json
import pyttsx3
import time
import sys
import os
import datetime
import speech_recognition
import logging
import pyttsx3

logging.basicConfig(
    filename=r"C:\Users\Uchek\Protocol\Sofia\logs_src\main_logs.log",
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s)'
)
# TODO: Remove the GUI functionality by changing the initialis_woerkflow function and the below objects
# in order to incluide the ability to select files to launch programmes from the UI oe by voice command
# if the client is not authorised refresh the token and download a new json file or put scopes on one of the keyvalue pairs
# and to renew credentials go to https://console.cloud.google.com/apis/credentials?authuser=1&project=learned-vault-319419

try:
    from Database.flask_database import FORMAT_SESSION_ID, File, day, month
    from logs_src.main_logging import logger
    from Web_driver.main_driver import WebController
    from Google_Api.gmail_api import gmail_api
    from Gym.training import update_exercises_results, generate_workout, write_generated_workout_to_csv
    from Google_Api.google_task_api import task_api
    from Web_driver.main_driver import WebController

except ModuleNotFoundError:
    def check_directory(path: str):
        if path.startswith('.') or path.startswith('__') or path.endswith('.exe'):
            return False
        else:
            return True
    _modules = list(filter(check_directory, os.listdir(os.getcwd())))
    for module in _modules:
        sys.path.append(os.path.join(os.getcwd(), module))
    logging.info('----------- Moduels in System Path ------------')
    logging.info(sys.path)

    from flask_database import FORMAT_SESSION_ID, File, day, month
    from main_logging import logger
    from main_driver import WebController
    from gmail_api import gmail_api
    from training import update_exercises_results, generate_workout, write_generated_workout_to_csv
    from google_task_api import task_api
    from main_driver import WebController

GOOGLE_TASKS_TASKLISTS = {
    'My Tasks': 0,
    'Daily Tasks': 1,
    'Morning Routine': 2,
    'Night Routine': 3
}


class SoftwareInteligenzaArtificiale(object):

    def __init__(self):

        self.webcontroller = WebController()

    def move_resource(self, source_path: str, destination_path: str):
        os.rename(source_path, destination_path)

    def listen_to_command(self, listener: speech_recognition.Recognizer):
        with speech_recognition.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
        return command

    def get_gym_capacity(self):
        driver = self.webcontroller.driver
        driver.get(url='https://www.thegymgroup.com/login/')
        time.sleep(3)
        cookies_btn = driver.find_element_by_id('onetrust-accept-btn-handler')
        cookies_btn.click()
        email_field = driver.find_element_by_id('login-email')
        email_field.send_keys('kuisoko1@sheffield.ac.uk')

        pin_field = driver.find_element_by_id('pin')
        pin_field.send_keys('17130800')

        login_button = driver.find_element_by_xpath(
            '//*[@id="login-modal"]/section/form/div[2]/div[5]/div/button')
        login_button.click()
        time.sleep(4)

        my_gym_btn = driver.find_element_by_xpath(
            '/html/body/div[1]/main/div/div[2]/div/div[1]/nav/ul/li[1]/a')
        my_gym_btn.click()

        how_busy_is_my_gym_btn = driver.find_element_by_xpath(
            '/html/body/div[1]/main/div/div[2]/div/div[1]/nav/ul/li[1]/ul/li[1]/a')
        how_busy_is_my_gym_btn.click()

        current_capacity = driver.find_element_by_xpath(
            '/html/body/div[1]/main/div/div[2]/div/div[2]/div/div/div/div/section/section[1]/div[1]/div[2]/p')
        time.sleep(3)
        engine = pyttsx3.init()
        engine.say(f' 11  11  {current_capacity.text}')
        engine.runAndWait()

    def routine(self):
        self.webcontroller.initialize_workflow()

    def gym_routine(self):
        print('called')
        update_exercises_results()
        workout = generate_workout()
        write_generated_workout_to_csv(workout)

    def add_tasks(self):
        # TASKS
        # TODO: rename the _TASKAPI file, find a better way to specify your routine
        command = "what is the weather like today"
        os.system(
            f"start https://www.google.co.uk/search?q=={command.replace(' ','+')}")

        dt = task_api.convert_to_RFC_datetime(2022, month, day, 23, 45)
        today = datetime.date.today().weekday()

        gym = ""
        stretching_and_abs = ""
        if today in [0, 2, 4, 5]:
            gym = "gym (30 mins)"
        else:
            stretching_and_abs = "stretching and abs"

        morning_routine = [
            "run sofia weekly schema",
            "run sofia functions",
            "put room in order",
            "put deodorant",
            "wash face",
            stretching_and_abs,
            "use 10 fast fingers (30 mins)"
            "complete 1 hackerank problem (1 hour)",
            "weight and update gymnasium",
            "eat (30 mins)",
            "drink water (1 liter a day)",
            "fill water bottles",
            "brush teeth",
            "put cream on",
            gym,
            "save to database"
        ]

        # filter all the conditional functions
        morning_routine = list(
            filter(lambda task: task != "", morning_routine))

        night_routine = [
            'brush teeth',
            'read',
            'put power bank on charge',
            'put headphones on charge',
            'put earpods on charge',
            'put phone on charge',
            'track calories by filling the diet-track file',
            'clean watch later playlist'
        ]

        daily_tasks = []

        for task in morning_routine:
            task_api.insert_task_to_tasklist(
                task, 2, f'created at : {datetime.datetime.now()}', dt)
        for task in night_routine:
            task_api.insert_task_to_tasklist(
                task, 3, f'created at : {datetime.datetime.now()}', dt)

        for task in daily_tasks:
            task_api.insert_task_to_tasklist(
                task, 1, f'created at : {datetime.datetime.now()}', dt)

    def create_task(self, task):
        dt = task_api.convert_to_RFC_datetime(2022, month, day, 23, 45)
        task_api.insert_task_to_tasklist(
            task, 0, f'created at : {datetime.datetime.now()}', dt)

    def tell_the_time(self):
        engine = pyttsx3.init()
        now_method = datetime.datetime.now()
        currentTime = now_method.strftime("%H past %M")
        engine.say(f'The Current Time is {currentTime}')
        engine.runAndWait()

    def launch_folder_code(self, folder_path: str):
        os.system(r"start code {}".format(folder_path))

    def launch_folder_explorer(self, folder_path: str):
        # the input needs to be a folder because you cannot cd into files
        os.chdir(folder_path)
        os.system("start .")
        os.chdir(os.getcwd())

    def create_file(self, directory, filename):
        os.chdir(r"C:\Users\Uchek\protocol\{}".format(directory))
        os.system(f"echo > {filename}")
        os.system(os.getcwd())

    def give_start_up_instructions(self):
        engine = pyttsx3.init()
        engine.say(
            f'Press the window key, search for run, press enter then type shell:startup and press ok')
        engine.runAndWait()

    def run_context(self, command: str):
        if 'gym capacity' in command:
            self.get_gym_capacity()

        elif 'clone repository' in command:
            # this function should be mostly run on sofia silent mode
            command = command.replace("clone", "")
            command = command.replace(" ", "")
            os.system(f"git clone https://github.com/kesler20/{command}")
            self.move_resource(r"C:\Users\Uchek\protocol\sofia\{}".format(
                command), r"C:\Users\Uchek\protocol\{}".format(command))
            try:
                os.remove(
                    r"C:\Users\Uchek\protocol\sofia\{}".format(command))
            except:
                pass

        elif "git clone" in command:
            command = command.replace("clone", "")
            command = command.replace(" ", "")
            os.system(f"git clone {command}")
            self.move_resource(r"C:\Users\Uchek\protocol\sofia\{}".format(
                command), r"C:\Users\Uchek\protocol\{}".format(command))
            try:
                os.remove(
                    r"C:\Users\Uchek\protocol\sofia\{}".format(command))
            except:
                pass

        elif 'music' in command:
            command = command.replace('music', '')
            os.system(
                f"start https://www.youtube.com/results?search_query={command.replace(' ','+')}")

        elif 'routine' in command:
            self.webcontroller.initialize_workflow()

        elif "open word document" in command:
            os.system("start winword.exe")

        elif "new note" in command:
            os.system(
                r'start code "C:\Users\Uchek\protocol\config_settings\note.md"')

        elif 'push files' in command:
            print(command)
            command = command.replace("push files ", "")
            if command == "sofia" or command == "":
                pass
            else:
                os.chdir(command)
            os.system("git pull")
            os.system("git add .")
            os.system('''git commit -m "make it better"''')
            os.system("git push")
            os.chdir(os.getcwd())

        elif "check journal" in command:
            os.system("start https://github.com/uos-datavisdashboard ")

        elif "open journal" in command:
            os.system(
                r'start code "C:\Users\Uchek\Protocol\github\journal_frontend"')
            os.system(
                r'start code "C:\Users\Uchek\Protocol\github\journal_backend"')

        elif "genetic engineering" in command:
            os.system("start https://github.com/Sheffield-iGEM ")

        elif "squid notes" in command:
            os.system(
                "start https://www.dropbox.com/home/Apps/Papyrus%20App/samsung%20SM-T585/PDFs")

        elif 'website' in command:
            command = command.replace('website', '')
            os.system(
                f"start https://www.google.co.uk/search?q=={command.replace(' ','+')}"
            )

        elif 'save to database' in command:
            os.system(r'cd "C:\Users\Uchek\Protocol\protocol_backend"')
            os.system(
                r'python "C:\Users\Uchek\Protocol\protocol_backend\sql_db_interface\database_interface.py"')
            os.system(
                r'python "C:\Users\Uchek\Protocol\protocol_backend\automatic_db_update.py"')

        elif 'start up' in command:
            self.give_start_up_instructions()

        elif "visual studio code" in command:
            os.system("start code")

        elif "move files" in command:
            source_path = input("source_path path?:")
            destination_path = input("destination path?:")
            self.move_resource(source_path,
                               destination_path)

        elif "weekly schema" in command:
            os.system(
                r'start https://onedrive.live.com/edit.aspx?resid=D6E96D5E52A0D29C!640457&cid=d6e96d5e52a0d29c&CT=1663827043213&OR=ItemsView')

        elif "font awesome" in command:
            os.system("start https://fontawesome.com/icons")

        elif "react icons" in command:
            os.system("start https://react-icons.github.io/react-icons")

        elif "tailwind documentation" in command:
            os.system("start https://tailwindcss.com/docs")

        elif 'start diet' in command:
            os.system(r'start https://www.sainsburys.co.uk/gol-ui/SearchResults/')
            os.system(
                r'start https://groceries.morrisons.com/webshop/startWebshop.do')
            os.system(r'start code "C:\Users\Uchek\Protocol\sofia-diet2"')

        elif 'heroku' in command:
            os.system("start https://dashboard.heroku.com")

        elif "launch sop" in command:
            os.system("start https://github.com/kesler20/SOP")

        elif "configuration settings" in command:
            os.system("start https://github.com/kesler20/Config_settings")

        elif 'github' in command:
            os.system('start https://github.com/kesler20?tab=repositories')

        elif 'email' in command:
            # command = command.replace('email', '')
            # gmail_api.send_email(command)
            os.system('start https://mail.google.com/mail/u/0/?hl=en-GB#inbox')

        elif 'youtube' in command:
            os.system('start https://www.youtube.com/')

        elif 'pomodoro' in command:
            os.system('start https://pomofocus.io/')

        elif 'instruction' in command:
            os.system(
                r'start https://onedrive.live.com/edit.aspx?resid=D6E96D5E52A0D29C!471416&ithint=file%2cdocx')

        elif 'exercise' in command:
            print(command)
            self.gym_routine()
            os.system(
                r'start excel "C:/Users/Uchek/OneDrive/Documents/training.csv"')

        elif 'good morning' in command:
            try:
                self.add_tasks()
            except:
                self.add_tasks()

        elif 'calendar' in command:
            os.system(r'start https://calendar.google.com/calendar/u/0/r?tab=kc')

        elif 'excel' in command:
            os.system('start excel.exe')

        elif 'open write folder' in command:
            os.system(r'start code "C:/Users/Uchek/Protocol/write"')

        elif 'onenote' in command:
            os.system('start onenote')

        elif 'tasks' in command:
            command = command.replace('tasks ', '')
            self.create_task(command)

        elif 'take notes' in command:
            os.system(
                r'start code "C:\Users\Uchek\Protocol\Config_settings"')

        elif 'document' in command:
            os.chdir("C://Users//Uchek//OneDrive//Documents")
            os.system("start .")
            os.chdir(os.getcwd())

        elif 'protocol' in command:
            os.chdir(r"C:\Users\Uchek\Protocol")
            os.system("start .")
            os.chdir(os.getcwd())

        elif 'downloads' in command:
            os.chdir(r"C:\Users\Uchek\Downloads")
            os.system("start .")
            os.chdir(os.getcwd())

        elif 'launch sofia' in command:
            os.system(r'start code "C:\Users\Uchek\Protocol\sofia_silent"')

        elif 'clean javascript' in command:
            os.system(
                r'start code "C:\Users\Uchek\Protocol\learn_javascript\clean_code_javascript.md"')

        elif 'one drive' in command:
            os.system(
                r'start https://onedrive.live.com/?id=root&cid=D6E96D5E52A0D29C')

        elif 'web notes' in command:
            os.system(
                r"C:/Users/Uchek/OneDrive/Documents/Web_development_notes.docx")

        elif 'what is the time' in command:
            self.tell_the_time()

        elif 'algorithms' in command:
            os.system(
                'start winword.exe "C:/Users/Uchek/OneDrive/Documents/DATA_STRUCTURES_AND_BIG_OH.docx"')

        elif 'python algos' in command:
            os.system(
                'start winword.exe "C:/Users/Uchek/OneDrive/Documents/Data_Structures_and_Algorithms_in_Python.pdf"')

        elif 'clean code' in command:
            os.system(
                'start winword.exe "C:/Users/Uchek/OneDrive/Documents/Clean_Code.docx"')

        elif 'current working directory' in command:
            os.system(f'start "{os.getcwd()}"')

        elif 'blackboard' in command:
            os.system(r'start https://vle.shef.ac.uk/ultra/stream')

        elif 'cascade' in command:
            os.system('start https://www.taskade.com/d/FUZpsyou3tdrE98R')

        elif 'list bugs' in command:
            os.system(
                r'start https://docs.google.com/document/d/1lKFhkwju1F5U8LuJYR0_oiIpeLQ8wPCnQoJZKmATgEE/edit')

        elif 'create file' in command:
            command = command.replace('create file', '')
            command = command.replace(' ', '.')
            os.system(f'echo > {command}')
        
        elif "create file in protocol" in command:
            command = command.replace('create file in protocol',"")
            self.create_file(command)

        elif "open code" in command:
            command = command.replace("open code","")
            self.launch_folder_code(command)

        elif "open explorer" in command:
            command = command.replace("open explorer","")
            self.launch_folder_explorer(command)
            
        elif 'open commands' in command:
            # sofia commands
            os.system(
                'start https://github.com/kesler20/sofia_silent/blob/master/Context/speaker.py')

        elif 'router' in command:
            os.system(r'start https://main.d2lxk97p0eyatl.amplifyapp.com/')

        elif 'react app' in command:
            os.system(r'create-react-app my-app')
            os.system(r'start code my-app')

        elif 'google drive' in command:
            os.system(r'start https://drive.google.com/drive/u/0/my-drive')

        elif 'reaction textbook' in command:
            os.system(
                r'start msedge "C:\Users\Uchek\OneDrive\Documents\fogler.pdf"')

        elif 'spotify' in command:
            command = command.replace('spotify', '')
            command = command.replace(' ', r'%20')
            os.system(f'start https://open.spotify.com/search/{command}')

        elif "phd work" in command:
            os.system(
                r'start winword.exe "C:\Users\Uchek\OneDrive\Documents\Back log of tasks to complete.docx"')
            os.system(
                "start https://github.com/kesler20/SOP/blob/master/productivity/PhD_work.md")

        elif "software sop" in command:
            os.system(
                "start https://github.com/kesler20/SOP/blob/master/coding/Software_development.md")

        elif 'google docs' in command:
            os.system(
                'start https://docs.google.com/document/u/0/')

        elif 'angry tools' in command:
            os.system('start https://angrytools.com')

        elif 'main back end' in command:
            os.system(
                r'start code "C:\Users\Uchek\Protocol\protocol_backend"')

        elif 'draw uml' in command:
            os.system(r'start code "C:\Users\Uchek\Protocol\draw-uml"')

        elif 'jaguar' in command:
            os.system(r'start code "C:\Users\Uchek\Protocol\jaguar"')

        elif 'aws accounts' in command:
            os.system("start https://eu-west-2.console.aws.amazon.com ")

        elif 'draw sql' in command:
            os.system("start https://drawsql.app/diagrams ")

        elif 'recycle bin' in command:
            os.chdir(r"C:\Users\Uchek\Recycle Bin")
            os.system("start .")
            os.chdir(os.getcwd())

        else:
            pass

    def start_listening(self, listener: speech_recognition.Recognizer, engine: pyttsx3.engine):
        try:
            command = self.listen_to_command(listener)
            print(f"\n COMMAND {command}  \n")
            self.run_context(command)
        except speech_recognition.UnknownValueError:
            engine.say(" sorry I didn't get that")
            engine.runAndWait()
