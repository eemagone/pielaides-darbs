import sys
import json
import random
import csv

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QProgressBar, QHBoxLayout
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QValidator

#lai kods stradatu windows key + r, un saja lodziņā ievadīt: pip install PyQt5
#viss pārējais ir python

USER_DATA_FILE = "lietotajs.json"

# LOGIN
class LoginWindow(QWidget):
    def __init__(self):

#login logs

        super().__init__()
        self.setWindowTitle("Pieslēgšanās / Reģistrācija")
        self.setGeometry(800, 300, 350, 350)
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Ievadi lietotājvārdu")
        self.user_input.setFixedHeight(30)
        

#paroles logs


        pass_layout = QHBoxLayout()
        self.pass_input = QLineEdit(self)
        self.pass_input.setPlaceholderText("Ievadi paroli")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedHeight(30)
        

#poga lai redz paroli


        self.toggle_pass_btn = QPushButton("👀", self)  
        self.toggle_pass_btn.setFixedWidth(30)  
        self.toggle_pass_btn.setCheckable(True)  
        self.toggle_pass_btn.clicked.connect(self.toggle_password)  
        pass_layout.addWidget(self.pass_input)
        pass_layout.addWidget(self.toggle_pass_btn) 


#pieslegties/registreties poga


        self.login_button = QPushButton("Pieslēgties", self)
        self.login_button.setFixedHeight(35)
        self.login_button.clicked.connect(self.login)

        self.signup_button = QPushButton("Reģistrēties", self)
        self.signup_button.setFixedHeight(35)
        self.signup_button.clicked.connect(self.signup)


#pogas login/sign up


        layout.addWidget(QLabel("Lietotājvārds:"))
        layout.addWidget(self.user_input)
        layout.addWidget(QLabel("Parole:"))
        layout.addLayout(pass_layout)  
        layout.addWidget(self.login_button)
        layout.addWidget(self.signup_button)

        self.setLayout(layout)


#uzspiez un redz kada parole


    def toggle_password(self):  
        if self.toggle_pass_btn.isChecked():
            self.pass_input.setEchoMode(QLineEdit.Normal) #redz paroli
        else:
            self.pass_input.setEchoMode(QLineEdit.Password)#neredz paroli


#ja ir user data loadot to


    def load_users(self):
        try:
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}


#saglabat datus, pec tam lai nav duplicates


    def save_users(self, users):
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(users, file, indent=4)


#saglaba sign up datus


    def signup(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        users = self.load_users()

        if username in users:
            QMessageBox.warning(self, "Kļūda", "Lietotājvārds jau eksistē.")
            return

        users[username] = {"password": password}
        self.save_users(users)

        QMessageBox.information(self, "Reģistrācija veiksmīga", "Pieslēdzies!")


#stripo ievaditos datus un parbauda vai eksiste lietotajs


    def login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        users = self.load_users()

        if username not in users or users[username]["password"] != password:
            QMessageBox.warning(self, "Kļūda", "Nepareizs lietotājvārds vai parole.")
            return

        QMessageBox.information(self, "Pieslēgšanās izdevās", f"Vai, sveiki {username}!")
        self.hide()
        self.main_window = Galvenais(username)
        self.main_window.show()

#--------------------------------------------------------------------------------------------

#PATI PROGRAMMA

#--------------------------------------------------------------------------------------------

#lai var saglabat goals

class GoalsWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Mainīt mērķus")
        self.setGeometry(850, 350, 300, 200)  
        layout = QFormLayout()

        # Izveido laukus mērķiem

        self.miegs_goal = QLineEdit(self)  
        self.udens_goal = QLineEdit(self)  
        self.sports_goal = QLineEdit(self)  

        # Pievieno validatorus, lai ļautu tikai skaitliskas vērtības

        self.miegs_goal.setValidator(QDoubleValidator(0.0, 24.0, 1, self))
        self.udens_goal.setValidator(QDoubleValidator(0.0, 10.0, 1, self))
        self.sports_goal.setValidator(QIntValidator(0, 14, self))

        layout.addRow(QLabel("Miega mērķis (stundas/dienā):"), self.miegs_goal)
        layout.addRow(QLabel("Ūdens mērķis (litri/dienā):"), self.udens_goal)
        layout.addRow(QLabel("Sporta mērķis (reizes/nedēļā):"), self.sports_goal)


        # Poga mērķu saglabāšanai

        self.save_button = QPushButton("Saglabāt mērķus")
        self.save_button.clicked.connect(self.save_goals)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.load_goals()


#user faila limitus saglaba

    def load_goals(self):
        user_file = f"{self.username}_info.json"
        try:
            with open(user_file, "r", encoding="utf-8") as file:
                user_data = json.load(file)
            goals = user_data.get("goals", {})
            self.miegs_goal.setText(goals.get("Miega mērķis", ""))
            self.udens_goal.setText(goals.get("Ūdens mērķis", ""))
            self.sports_goal.setText(goals.get("Sporta mērķis", ""))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

#parbauda vai ir cipars merkos ierakstits

    def save_goals(self):
        if self.miegs_goal.validator().validate(self.miegs_goal.text(), 0)[0] != QValidator.Acceptable:
            QMessageBox.warning(self, "Kļūda", "Lūdzu ievadiet derīgu miega mērķi (cipars vai decimāldaļa)!")
            return
        if self.udens_goal.validator().validate(self.udens_goal.text(), 0)[0] != QValidator.Acceptable:
            QMessageBox.warning(self, "Kļūda", "Lūdzu ievadiet derīgu ūdens mērķi (cipars vai decimāldaļa)!")
            return
        if self.sports_goal.validator().validate(self.sports_goal.text(), 0)[0] != QValidator.Acceptable:
            QMessageBox.warning(self, "Kļūda", "Lūdzu ievadiet derīgu sporta mērķi (vesels skaitlis)!")
            return

        goals = {
            "Miega mērķis": self.miegs_goal.text(),
            "Ūdens mērķis": self.udens_goal.text(),
            "Sporta mērķis": self.sports_goal.text(),
        }

        user_file = f"{self.username}_info.json"
        try:
            with open(user_file, "r", encoding="utf-8") as file:
                user_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            user_data = {}

        user_data["goals"] = goals

        with open(user_file, "w", encoding="utf-8") as file:
            json.dump(user_data, file, indent=4)

        QMessageBox.information(self, "Saglabāts", "Mērķi saglabāti veiksmīgi!")
        self.close()


#--------------------------------------------------------------------------------------------


class Galvenais(QWidget):
    def __init__(self, username):
        super().__init__()

#nakosais lodzins

        self.username = username
        self.setWindowTitle("Veselības Kompass")
        self.setGeometry(800, 300, 300, 250)  
        self.setStyleSheet("background-color: #ffffff;")
        self.progress_win = None  

        mainl = QVBoxLayout()
        forml = QFormLayout()

        self.miegs_input = QLineEdit(self)
        self.udens_input = QLineEdit(self)
        self.sports_input = QLineEdit(self)
        self.esanas_paradumi_input = QLineEdit(self)
        self.noskana_input = QLineEdit(self)

#kur ievadit datus

        forml.addRow(QLabel("Miegs (stundas/dienā):"), self.miegs_input)
        forml.addRow(QLabel("Izdzerts ūdens (litri/dienā):"), self.udens_input)
        forml.addRow(QLabel("Fiziski aktīvs (reizes/nedēļā):"), self.sports_input)
        forml.addRow(QLabel("Ēšanas paradumi (1-5):"), self.esanas_paradumi_input)
        forml.addRow(QLabel("Noskaņojums (1-5):"), self.noskana_input)

#pogas

        self.submit_button = QPushButton("Iesniegt")
        self.submit_button.clicked.connect(self.dati)
        
        self.overall_progress_button = QPushButton("Skatīt kopējo progresu")
        self.overall_progress_button.clicked.connect(self.show_overall_progress)

        self.change_goals_button = QPushButton("Mainīt mērķus")
        self.change_goals_button.clicked.connect(self.open_goals_window)
       
        mainl.addLayout(forml)
        mainl.addWidget(self.submit_button)
        mainl.addWidget(self.overall_progress_button)
        mainl.addWidget(self.change_goals_button) 
        self.setLayout(mainl)


    def open_goals_window(self):
        self.goals_window = GoalsWindow(self.username)
        self.goals_window.show()


#--------------------------------------------------------------------------------------------

#kludu parbaude

    def dati(self):
        try:
            miegs = float(self.miegs_input.text().replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Kļūda!", "Ievadi skaitli miega laukā!")
            return

        try:
            udens = float(self.udens_input.text().replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Kļūda!", "Ievadi skaitli ūdens laukā!")
            return

        try:
            sports = float(self.sports_input.text().replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Kļūda!", "Ievadi skaitli fizisko aktivitāšu laukā!")
            return

        try:
            esanas_paradumi = int(self.esanas_paradumi_input.text())
            if not (1 <= esanas_paradumi <= 5):  
                QMessageBox.warning(self, "Kļūda!", "Ēšanas paradumiem jābūt no 1 līdz 5!")
                return
        except ValueError:
            QMessageBox.warning(self, "Kļūda!", "Ievadi skaitli no 1-5 ēšanas paradumos!")
            return
        
        try:
            noskana = int(self.noskana_input.text())
            if not (1<= noskana <=5 ):
                QMessageBox.warning(self, "Kļūda!", "Noskaņai jābūt no 1 līdz 5!")
                return
        except ValueError:
            QMessageBox.warning(self, "Kļūda!", "Ievadi skaitli no 1-5 noskaņojumā!")
            return
        

        dati = {
            "Miegs": miegs,
            "Šķidrums": udens,
            "Fiziskas aktivitātes": sports,
            "Ēšanas paradumi": esanas_paradumi,
            "Noskaņojums": noskana,
        }

        self.save_data(dati)
        prioritates = self.calc_prio(dati)
        self.paradit_prio(prioritates)

#lai parada random health tip pec ok lodzina

        health_tip = self.get_random_health_tip()
        QMessageBox.information(self, "Padoms!", f"👽 {health_tip}")

#saglaba katra lietotaja datus sava faila

    def save_data(self, dati):
        user_csv = f"{self.username}_info.csv"
        with open(user_csv, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(list(dati.values()))  

    def load_user_goals(self):
        user_file = f"{self.username}_info.json"
        try:
            with open(user_file, "r", encoding="utf-8") as file:
                user_data = json.load(file)
            return user_data.get("goals", {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}  

#aprekini prioritatem pec goals

    def calc_prio(self, dati): 
        prioritates = []
        goals = self.load_user_goals()
        sleep_goal = float(goals.get("Miega mērķis", 7))
        water_goal = float(goals.get("Ūdens mērķis", 2))
        activity_goal = float(goals.get("Sporta mērķis", 3))
        
        if dati["Miegs"] < sleep_goal:
            prioritates.append(f"Izgulies! Vismaz {sleep_goal:g}h!")
        if dati["Šķidrums"] < water_goal:
            prioritates.append(f"Dzer vairāk šķidrumus, vismaz {water_goal:g}L!")
        if dati["Fiziskas aktivitātes"] < activity_goal:
            prioritates.append(f"Sporto vairāk, vismaz {activity_goal:g} reizes nedēļā!")
        if dati["Ēšanas paradumi"] <= 3:
            prioritates.append("Ievēro veselīgāku uzturu!")
        if dati["Noskaņojums"] <= 3:
            prioritates.append("Atpūties, atrodi laiku sev!")
        return prioritates

    def paradit_prio(self, prioritates):  
        message = "Tavas prioritātes:\n\n"  
        for idx, p in enumerate(prioritates):  
            message += f"{idx+1}. {p}\n"  
        QMessageBox.information(self, "Prioritātes", message)  


#--------------------------------------------------------------------------------------------
#PROGRESS BAR 
#--------------------------------------------------------------------------------------------


    def show_overall_progress(self):
        user_csv = f"{self.username}_info.csv"
        try:
            with open(user_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                user_rows = list(reader)
        except FileNotFoundError:
            QMessageBox.information(self, "Info", "Nav saglabātu datu.")
            return

        if not user_rows:
            QMessageBox.information(self, "Info", "Nav saglabātu datu.")
            return

        recent_rows = user_rows[-7:]
        num_entries = len(recent_rows)
        sum_metrics = [0, 0, 0, 0, 0]
        for row in recent_rows:
            try:
                metrics = [float(val) for val in row]
            except ValueError:
                continue
            for i in range(5):
                sum_metrics[i] += metrics[i]
        avg_metrics = [s / num_entries if num_entries > 0 else 0 for s in sum_metrics]

        #No json file visus merkus paskatas
        goals = self.load_user_goals()
        sleep_goal = float(goals.get("Miega mērķis", 8))
        water_goal = float(goals.get("Ūdens mērķis", 2))
        activity_goal = float(goals.get("Sporta mērķis", 3))

        self.overall_win = QWidget()  
        self.overall_win.setWindowTitle("Kopējais progress")
        layout = QVBoxLayout()
        metric_names = ["Miegs", "Šķidrums", "Fiziskas aktivitātes", "Ēšanas paradumi", "Noskaņojums"]
        
        for name, avg in zip(metric_names, avg_metrics):
            bar = QProgressBar()
            #progress bara parada procentus pec merkiem vai default

#ja ievadis merkos 0 tad progress bar radisies 0

            if name == "Miegs":
                if sleep_goal == 0:  #lai sleep var but 0
                    progress_value = 0  
                    QMessageBox.information(self, "⚠️", "Miega dati tiks kļūdaini attēloti, nomaini mērķa vērtību!") #brīdina lietotāju par kļūdainiem mērķiem
                    
                else:
                    progress_value = int((avg / sleep_goal) * 100)
            
            elif name == "Šķidrums":
                if water_goal == 0:
                    progress_value =0
                    QMessageBox.information(self, "⚠️", "Uzņemtais šķidruma daudzuma dati tiks kļūdaini attēlots, nomaini mērķa vērtību!")
                else: 
                    progress_value = int((avg / water_goal) * 100)

            elif name == "Fiziskas aktivitātes":
                if activity_goal == 0:
                    progress_value = 0
                    QMessageBox.information(self, "⚠️", "Fizisko aktivitāšu daudzuma dati tiks kļūdaini attēlots, nomaini mērķa vērtību!")
                else:
                    progress_value = int((avg / activity_goal) * 100)

            else:  #prieks eating habits un mood var but tikai no 1-5 var vnk ar 20 sareizinat

                progress_value = int(avg * 20)  # 5 = 100% -> 5*20=100
            
            #lai procenti butu lidz 100%

            progress_value = max(0, min(100, progress_value))
            bar.setValue(progress_value)
            
            layout.addWidget(QLabel(f"{name} :"))
            layout.addWidget(bar)

        self.overall_win.setLayout(layout)
        self.overall_win.show()


#Health tips

    def get_random_health_tip(self):
        tips = [
            "Nepīpē!",  
            "Neizmanto telefonu pirms gulēt iešanas.",  
            "Neej uz Tallinas kvartālu",  
            "Mīli sevi!",  
            "Meditē, ievelc elpu ik pa laikam",  
            "Tīri zobus vismaz 2 reizes dienā!",  
        ]
        return random.choice(tips) 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())