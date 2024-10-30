from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
import json as js
import random as r
import pandas as pd
from kivy.clock import Clock
from kivy.properties import NumericProperty
import os
import sys

# Kivy dosyası
Builder.load_string('''
<MainScreen>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (300, 200)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            Label:
                text: '2.Geleneksel Bilimtey Bilim Bilgi Yarışması'
                font_size: 20
                size_hint_y: None
                height: 50
            
            Label:
                text: 'Kullanıcı Adı:'
                font_size: 20
                size_hint_y: None
                height: 50
            
            TextInput:
                id: username_input
                multiline: False
                size_hint_y: None
                height: 50

            Button:
                text: 'Giriş Yap'
                size_hint: (None, None)
                size: (100, 50)
                pos_hint: {'center_x': 0.5}
                on_press: root.manager.current = 'question'
                on_press: root.get_username()
                color: 0, 0, 0, 1
            Label:
                text: 'Başarılar..'
                size_hint: (None, None)
                size: (100, 50)
                pos_hint: {'center_x': 0.5}
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'
        Image:
            source: 'APP/file.png'
            size_hint: (None, None)
            size: (100, 100)
            pos_hint: {'center_x': 0.5}
    AnchorLayout:
        anchor_x: 'right'
        anchor_y: 'bottom'
        Image:
            source: 'APP/kblogo.png'
            size_hint: (None, None)
            size: (100, 100)
            pos_hint: {'center_x': 0.5}
            

<QuestionScreen>:
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'top'
        Label:
            text: f'Kullanıcı Adı : {root.username}'
            font_size: 20
            size_hint: (None, None)
            height: 50
            width: 200
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (400, 400)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            Label:
                text: f'Kalan Süre: {root.time_left} saniye'  # Geri sayımı burada gösteriyoruz
                font_size: 20
                size_hint_y: None
                height: 50
            
            Label:
                text: root.question_text
                font_size: 20
                size_hint_y: None
                height: 50
            GridLayout:
                cols: 4
                Button:
                    text: root.A
                    size_hint: (None, None)
                    size: (100, 100)
                    on_press: root.AnswerA()
                    on_press: root.getFinalScore()
                Button:
                    text: root.B
                    size_hint: (None, None)
                    size: (100, 100)
                    on_press: root.AnswerB()
                    on_press: root.getFinalScore()
                Button:
                    text: root.C
                    size_hint: (None, None)
                    size: (100, 100)
                    on_press: root.AnswerC()
                    on_press: root.getFinalScore()
                Button:
                    text: root.D
                    size_hint: (None, None)
                    size: (100, 100)
                    on_press: root.AnswerD()
                    on_press: root.getFinalScore()
<FailsScreen>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (300, 200)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            Label:
                text:root.Name + ": " + root.Score + " Puan"
                font_size: 40
                size_hint_y: None
                height: 50
            Label:
                text:  "Toplamda " +  str(int(int(root.Score) / 5)) + " adet soruyu doğru çözdünüz." 
                font_size: 40
                size_hint_y: None
                height: 50
            Button:
                text: 'Menüye Dön'
                size_hint: (None, None)
                size: (100, 50)
                pos_hint: {'center_x': 0.5}
                on_press: root.manager.current = 'menu'
                on_press: root.manager.get_screen('question').pushData()
<WonScreen>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (300, 200)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            Label:
                text: 'Tebrikler! Oyunu Kazandınız!'
            Button:
                text: 'Menüye Dön'
                size_hint: (None, None)
                size: (100, 50)
                pos_hint: {'center_x': 0.5}
                on_press: root.manager.current = 'menu'
                on_press: root.manager.get_screen('question').pushData()
''')
class RandomNumberGenerator:
    def __init__(self):
        self.previous_number = None

    def get_random_number(self):
        while True:
            # 1 ile 100 arasında rastgele bir sayı üret
            new_number = r.randint(1, 10)
            if new_number != self.previous_number:
                self.previous_number = new_number
                return new_number

class WonScreen(Screen):
    pass
class QuestionScreen(Screen):
    question_text = StringProperty("Loading question...")
    A = StringProperty("")
    B = StringProperty("")
    C = StringProperty("")
    D = StringProperty("")
    username = StringProperty("")
    time_left = NumericProperty(10)  # Geri sayım için eklenen özellik
    num = 0
    answer = StringProperty("")
    Score = 0
    QL = 1
    timer_event = None
    def on_enter(self):
        self.load_data_from_json()
        self.start_timer()
    def start_timer(self):
        self.time_left = 10  # Süreyi başlat
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            self.time_out()

    def stop_timer(self):
        if self.timer_event:
            Clock.unschedule(self.timer_event)

    def time_out(self):
        print("Süre doldu.")
        self.stop_timer()
        self.manager.current = 'fails'  # Süre dolduğunda başarısız ekranına geç
    def load_data_from_json(self):
        try:
            if self.QL <= 2:
                soru_dosya = 'APP/Db/Soru-Easy.json'
            elif self.QL <= 6:
                soru_dosya = 'APP/Db/Soru-Medium.json'
            elif self.QL <= 10:
                soru_dosya = 'APP/Db/Soru-Hard.json'
            else:
                self.stop_timer()
                self.manager.current = 'won'
                return
                

            with open(soru_dosya, encoding='utf-8') as f:
                sorular = js.load(f)
            rmg = RandomNumberGenerator()
            num = rmg.get_random_number()
            self.manager.get_screen('question').num = num
            soru_numarası = f"Soru {num}:"  # Dosyadaki soru sayısına göre random seçiyoruz
            self.question_text = sorular[soru_numarası]["Soru"]
            self.A = sorular[soru_numarası]["A"]
            self.B = sorular[soru_numarası]["B"]
            self.C = sorular[soru_numarası]["C"]
            self.D = sorular[soru_numarası]["D"]
            answer = sorular[soru_numarası]["Cevap"]
            self.manager.get_screen('question').answer = answer
            self.QL += 1

        except Exception as e:
            print("Hata:", e)
            self.question_text = "Soru yüklenemedi."
    def check_answer(self, selected_option):
        if selected_option == self.answer:
            print("Doğru")
            # TestApp içindeki Score özelliğini güncelliyoruz
            self.manager.get_screen('question').Score += 5
            self.load_data_from_json()
        else:
            print("Yanlış")
            self.stop_timer()
            self.manager.current = 'fails'

    def AnswerA(self):
        self.manager.get_screen('question').Score += 5
        self.load_data_from_json()

    def AnswerB(self):
        self.check_answer("B")

    def AnswerC(self):
        self.check_answer("C")

    def AnswerD(self):
        self.check_answer("D")
    def getFinalScore(self):
        #self.manager.get_screen('fails').Score = str(self.manager.get_screen('question').Score)
        self.manager.get_screen('fails').Score = str(self.Score)
        self.manager.get_screen('fails').Name = self.username
        self.manager.get_screen('fails').int_Score = self.manager.get_screen('question').Score
        self.manager.get_screen('fails').time = self.time_left
    def pushData(self):
        df = pd.DataFrame([[self.username, self.Score , (self.Score / 5) , self.time_left]], columns=["Username", "Score","Level","Time"])
        df.to_csv('APP/Db/User-Info.csv', mode='a', sep='|', header=not pd.io.common.file_exists('APP/Db/User-Info.csv'), index=False)
        App.get_running_app().restart()
        
class FailsScreen(Screen):
    Score = StringProperty("0") # Bu StringProperty'yi tanımladık bunu kullanmamızın sebebi, bu değeri değiştirdiğimizde ekrandaki değer de değişecek direkt string olarak atasaydık değişmeyecekti
    Name = StringProperty("")
    time = NumericProperty(0)

class MainScreen(Screen):
    def get_username(self):
        # username_input içindeki metni alır
        username = self.ids.username_input.text
        #bunu QuestionScreen'e gönderir
        self.manager.get_screen('question').username = username

        # Kullanıcı adını bir .csv dosyasına yazar
        #df = pd.DataFrame([[username]], columns=["Username"])
        #df.to_csv('APP/Db/User-Info.csv', mode='a', header=False, index=False)

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='menu'))
        sm.add_widget(QuestionScreen(name='question'))
        sm.add_widget(FailsScreen(name='fails'))
        sm.add_widget(WonScreen(name='won'))
        Window.size = (800, 600)
        return sm
    def restart(self):
        """Uygulamayı kapatıp yeniden başlat."""
        os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == '__main__':
    TestApp().run()
    exit()
