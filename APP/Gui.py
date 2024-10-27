from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
import json as js
import random as r
import pandas as pd



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
                on_press: root.get_username()  # Button, get_username metodunu çağırıyor

            Label:
                text: 'Başarılar..'
                size_hint: (None, None)
                size: (100, 50)
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
                text: root.question_text  # Burada root.question_text kullanıyoruz
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
                Button:
                    text: root.B
                    size_hint: (None, None)
                    size: (100, 100)
                    on_press: root.AnswerB()
                Button:
                    text: root.C
                    size_hint: (None, None)
                    size: (100, 100)
                    on_press: root.AnswerC()
                Button:
                    text: root.D
                    size_hint: (None, None)
                    size: (100, 100)
                    on_press: root.AnswerD()
''')

class QuestionScreen(Screen):
    question_text = StringProperty("Loading question...")  # Bu StringProperty'yi tanımladık
    A = StringProperty("")
    B = StringProperty("")
    C = StringProperty("")
    D = StringProperty("")
    username = StringProperty("")
    num = 0
    answer = StringProperty("")
    QL = 1

    def on_enter(self):
        self.load_data_from_json()  # Ekran açıldığında soru yükleniyor

    def load_data_from_json(self):
        try:
            if self.QL <= 5:
                soru_dosya = 'APP/Db/Soru-Easy.json'
            elif self.QL <= 10:
                soru_dosya = 'APP/Db/Soru-Medium.json'
            else:
                soru_dosya = 'APP/Db/Soru-Hard.json'

            with open(soru_dosya, encoding='utf-8') as f:
                sorular = js.load(f)
            num = r.randint(1, len(sorular))
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
    def AnswerA(self):
        if "A" == self.answer:
            print("Doğru")
        else:
            print("Yanlış")
    def AnswerB(self):
        if "B" == self.answer:
            print("Doğru")
        else:
            print("Yanlış")
    def AnswerC(self):
        if "C" == self.answer:
            print("Doğru")
        else:
            print("Yanlış")
    def AnswerD(self):
        if "D" == self.answer:
            print("Doğru")
        else:
            print("Yanlış")
        
        

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
        Window.size = (800, 600)
        return sm

if __name__ == '__main__':
    TestApp().run()
