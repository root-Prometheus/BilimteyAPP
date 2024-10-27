from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.layout import Layout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
import time as t
from kivy.uix.screenmanager import Screen


#Yarışma süreli olabilir, süre bitiminde yarışma sona erer ve sonuçlar açıklanır.
#yarışma süresiz olur ama süre 1.yi belirlemekte kullanılabilir.
#yarışma süreli olur ama erken bitiren günü 1. si olur.
#her soru seviyesi olur sorular zorluklara zorluklarına göre ağırlık atılır ona göre o level de o sorunun denk gelme şansı yükseltilir.


#Bu LoginScreen sınıfı ve diğer sınıflar tam olmadı ama giriş ekranında görülecek kısım okey fakat classlar arası ayar
class Buttons(Button):
    pass

class Results(Widget):
    pass

class LoginScreen(AnchorLayout):
    def __init__(self,**kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        # Create a BoxLayout for the input and button
        box_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(300, 200))
        box_layout.add_widget(Label(text='2.Geleneksel Bilimtey Bilim Bilgi Yarışması', font_size=20, size_hint_y=None, height=50, pos_hint={'top_x': 0.1, 'top_y': 4}))
        box_layout.add_widget(Label(text='Kullanıcı Adı:', font_size=20, size_hint_y=None, height=50, pos_hint={'top_x': 0.5, 'top_y': 5}))
        self.username = TextInput(multiline=False, size_hint_y=None, height=50)
        box_layout.add_widget(self.username)
        box_layout.add_widget(Buttons(text='Giriş Yap', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5, 'center_y': 4.5}, on_press=self.button))
        box_layout.add_widget(Label(text='Başarılar..', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5, 'center_y': 4.5}))
        # Add the BoxLayout to the top of the screen
        self.add_widget(box_layout)
        # Create an AnchorLayout to position the image at the bottom left
        anchor_kbü = AnchorLayout(anchor_x='left', anchor_y='bottom')
        image_kbü = Image(source='kblogo.png', size_hint=(None, None), size=(100, 100))
        anchor_kbü.add_widget(image_kbü)
        anchor_Club = AnchorLayout(anchor_x='right', anchor_y='bottom')
        image_Club = Image(source='file.png', size_hint=(None, None), size=(100, 100), pos_hint={'right': 1})
        anchor_Club.add_widget(image_Club)       
        # Add the AnchorLayout to the screen

        self.add_widget(anchor_kbü)
        self.add_widget(anchor_Club)
        
    def Category(self):
        pass
    def button(self,instance): # burada instance olarak almamızın sebebi button fonksiyonunu çağırırken instance olarak çağırmamızdır.
        print(f'Button pressed by ${self.username.text}')
        self.add_widget(Results())

class BilimteyBilim(App):
    def build(self):
        global time
        time = t.time()
        Data = LoginScreen()
        return Data

#Puan hesaplama algoritaması ==> 1000 puan / bitirme süresi;

BilimteyBilim().run()
print(t.time() - time)