from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window

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
                on_press: root.get_username()  # Button, get_username metodunu çağırıyor

            Label:
                text: 'Başarılar..'
                size_hint: (None, None)
                size: (100, 50)
                pos_hint: {'center_x': 0.5}

''')

class MainScreen(Screen):
    def get_username(self):
        # username_input içindeki metni alır
        username = self.ids.username_input.text
        print(f"Kullanıcı Adı: {username}")

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='menu'))
        Window.size = (800, 600)
        return sm

if __name__ == '__main__':
    TestApp().run()
