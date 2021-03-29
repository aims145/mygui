from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from pathlib import Path
import datetime
import random
from hoverable import HoverBehavior
Builder.load_file("design.kv")

class LoginScreen(Screen):
    def login_checker(self, username, password):
        creds = json.load(open("creds.json", "r"))
        if username in creds.keys():
            if password == creds[username]["Password"]:
                self.manager.transition.direction = "left"
                self.manager.current = "login_success"
            else:
                self.ids.login_error.text = "Entered username and password is incorrect !"
        else:
            self.ids.login_error.text = "Entered username and password is incorrect !"
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    def forgot_password(self):
        print("You have press forgot password button !")



class SignUpScreen(Screen):
    def sign_up_submit(self, username, password):
        data = {
            "UserName": username,
            "Password": password,
            "CreatedDate":str(datetime.datetime.now())
        }
        fhr = open("creds.json", "r")
        json_obj = json.loads(fhr.read())
        fhr.close()
        json_obj[username] = data
        json_obj = json.dumps(json_obj)
        fhw = open("creds.json", "w")
        fhw.write(json_obj)
        fhw.close()
        self.manager.current = "sign_up_success"
    def sign_in(self):
        self.manager.current = "login_screen"

class SignUpScreenSuccess(Screen):
    def sign_in(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def login_screen(self):
        self.manager.current = "login_screen"
        self.manager.transition.direction = "right"
    def login_input(self):
        text = str(self.ids.logininput.text).lower()
        available_feelings = glob.glob("*txt")
        available_feelings = [Path(filename).stem for filename in available_feelings]
        print(available_feelings)
        if text in available_feelings:
            with open(text+".txt", "r") as file:
                quotes = file.readlines()
            self.ids.readpara.text = random.choice(quotes)
        else:
            self.ids.readpara.text = "Try other feelings !"
class RootWidget(ScreenManager):
    pass


class ImageButton(ButtonBehavior, HoverBehavior, Image ):
    pass
class MainApp(App):

    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
