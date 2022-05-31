import kivy
from googlesearch import search
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.config import Config
from model_work import predict_class
from Users import check_existing_user, new_user, username_criteria, password_len, check_pw
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
kivy.require("1.11.1")


class MainWindow(Screen):
    pass


class SelectPage(Screen):
    image_file_dir = ""
    answer = ""
    flag = True

    def __init__(self, **kwargs):
        super(SelectPage, self).__init__(**kwargs)
        self.image_file_dir = ""
        self.answer = ""

    def selected(self, filename=""):
        self.ids.error.text = ""
        self.ids.image.source = ""
        try:
            if not filename[0].lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                self.ids.error.text = "Select an image"
            else:
                self.ids.image.source = filename[0]
        except IndexError:
            self.ids.error.text = "Select an image"
            pass

    @classmethod
    def predictimage(cls, file_path):
        try:
            if file_path[0].lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                cls.answer = predict_class(file_path[0])
                return True
            else:
                return False
        except IndexError:
            pass


class AboutUs(Screen):
    def __init__(self, **kwargs):
        super(AboutUs, self).__init__(**kwargs)
        self.text = """[size=20]Have you ever been caught in a situation where you
        see a delicious dish, but you have no idea what it actually is? 
        Well here you have it!
        With this app you can identify that along with a 
        list of recipes to make it all by yourself!
        Flambe provides an easy means to do it 
        where the user has to simply upload the picture of 
        the dish and would get various links to that recipe! 
        Along with this, the user can also 
        visit their history of searched dishes by creating an account 
        on the app and revisit the same recipes.[/size]"""

        Clock.schedule_once(self.set_text, 1)

    def set_text(self, _):
        self.ids.about.text = self.text


class LoginPage(Screen):
    mode = ""
    username = ""
    pw = ""

    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        self.mode = ""

    @classmethod
    def update_creds(cls, username, pw):
        cls.username = username
        cls.pw = pw

    def existing_user(self):
        self.ids.error.text = ""
        self.ids.error.pos_hint = {"x": 0.3, 'top': 1.14}
        username = self.ids.username.text
        pw = self.ids.password.text
        if check_existing_user(username, pw):
            if check_pw(username, pw):
                return True
            else:
                self.ids.error.text = "Incorrect\nPassword"
                self.ids.error.pos_hint = {"x": 0.3, 'top': 0.98}
        else:
            self.ids.error.text = "User does\nnot exist"

    @classmethod
    def user(cls):
        cls.mode = "user"

    @classmethod
    def guest(cls):
        cls.mode = "guest"


class NewUserPage(LoginPage, Screen):
    def create_user(self):
        self.ids.error.text = ""
        self.ids.error.pos_hint = {"x": 0.3, 'top': 1.14}
        username = self.ids.username.text
        pw = self.ids.password.text
        if not check_existing_user(username, pw):
            if username_criteria(username):
                if password_len(pw):
                    LoginPage.username = username
                    LoginPage.pw = pw
                    new_user(username, pw)
                    return True
                else:
                    self.ids.error.text = "Password too\n long"
                    self.ids.error.pos_hint = {"x": 0.3, 'top': 0.98}
            else:
                self.ids.error.text = "No special \ncharacters or \nspaces allowed \nin username"
        else:
            self.ids.error.text = "User already \nexists"


class PredictionPage(LoginPage, SelectPage, Screen):
    def __init__(self, **kwargs):
        super(PredictionPage, self).__init__(**kwargs)
        self.answer = ""
        self.mode = ""
        self.username = ""
        self.pw = ""

    def show_ans(self):
        self.mode = LoginPage.mode
        self.username = LoginPage.username
        self.pw = LoginPage.pw
        images_predicted = []
        img_dir = "images"
        links = ""
        self.answer = SelectPage.answer
        self.ids.ans.text = "[size=25]The Dish is : " + self.answer.replace("_", " ").capitalize() + "[/size]"
        img_dir = os.path.join(img_dir, self.answer)
        for img in os.listdir(img_dir):
            images_predicted.append(os.path.join(img_dir, img))
        self.ids.img1.source = images_predicted[0]
        self.ids.img2.source = images_predicted[1]
        self.ids.img3.source = images_predicted[2]
        for link in search(self.answer.replace("_", " ")+"easy recipe", tld="co.in", num=10, stop=10, pause=2):
            links += "[ref="+link+"]"+link+"[/ref]\n"
        self.ids.links.text = links
        if self.mode == 'user':
            self.update_history(images_predicted[0], self.answer, links)

    def update_history(self, picture, dish, link):
        user_file_obj = open("{}.txt".format(self.username), "a")
        user_file_obj.write(picture + "\t" + dish + "\t" + link + "\n\n")
        user_file_obj.close()


class HistoryPage(LoginPage, Screen):
    def __init__(self, **kwargs):
        super(HistoryPage, self).__init__(**kwargs)
        self.username = ""
        self.pw = ""
        self.user_file_obj = ""
        self.positions = []
        self.current_position = 0

    def open_file(self):
        self.username = LoginPage.username
        self.pw = LoginPage.pw
        self.user_file_obj = open("{}.txt".format(self.username), "r")
        self.positions = []
        self.positions.append(self.current_position)

    def show_search(self):
        try:
            self.current_position = self.user_file_obj.tell()
            line = self.user_file_obj.readline().split('\t')
            img = line[0]
            dish = line[1]
            links = line[2]
            no_of_links = 11
            for each in range(no_of_links):
                links += self.user_file_obj.readline()
            self.ids.dish.text = "[size=25]" + dish.replace("_", " ").capitalize() + "[/size]"
            self.ids.image.source = img
            self.ids.links.text = links[:-2]
            self.current_position = self.user_file_obj.tell()
            if self.current_position not in self.positions:
                self.positions.append(self.current_position)
        except:
            pass

    def seek_back(self):
        try:
            prev_position = self.positions[self.positions.index(self.user_file_obj.tell())-2]
            if self.user_file_obj.tell() == self.positions[1]:
                pass
            else:
                self.user_file_obj.seek(prev_position)
                self.show_search()
        except:
            pass

    def close_file(self):
        self.user_file_obj.close()

    pass


class LobbyPage(LoginPage, Screen):
    @classmethod
    def logout(cls):
        LoginPage.username = ""
        LoginPage.pw = ""
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("flambe.kv")


class FlambeApp(App):
    icon = 'images/windowicon.jpg'
    title = 'Flambé'

    def build(self):
        return kv


if __name__ == '__main__':
    FlambeApp().run()
