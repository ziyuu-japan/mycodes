from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from gtts import gTTS

from kivy.core.audio import SoundLoader
import os
from os.path import sep, expanduser, isdir, dirname
from kivy.garden.filebrowser import FileBrowser

class PlaySpeechWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(PlaySpeechWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.widgets_list = []
        self.filepath= ""

        boxlayout= BoxLayout()
        self.filename_label = Label(text='File Name')
        self.findfile_button = Button(text='Find mp3 file')
        self.findfile_button.bind(on_press=self.switch_to_filebrowser)
        boxlayout.add_widget(self.filename_label)
        boxlayout.add_widget(self.findfile_button)
        self.widgets_list.append(boxlayout)
        self.add_widget(boxlayout)

        speech_button = Button(text='Speech')
        speech_button.bind(on_press=self.speech)
        self.widgets_list.append(speech_button)
        self.add_widget(speech_button)

        self.filebrowser_widget = FileBrowser(select_string='Select',
            favorites=[(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'speeches'), 'speeches')])
        self.filebrowser_widget.bind(
                    on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled)

    def switch_to_filebrowser(self, instance):
        self.clear_widgets()
        self.add_widget(self.filebrowser_widget)

    def _fbrowser_canceled(self, instance):
        print 'cancelled, Close self.'
        self.clear_widgets()
        for widget in self.widgets_list:
            self.add_widget(widget)


    def _fbrowser_success(self, instance):
        self.filepath = instance.selection[0]
        self.filename_label.text = self.filepath
        self.clear_widgets()
        for widget in self.widgets_list:
            self.add_widget(widget)
        print instance.selection

    def speech(self, instance):
        sound = SoundLoader.load('{}'.format(self.filepath))
        if sound:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            sound.play()



class SpeechCreateWidget(BoxLayout):

    create_text_to_speech_text = ObjectProperty()
    create_text_to_speech_filename = ObjectProperty()

    def check_text_input_property(self, instance):
        #print(instance)
        print(self.text_input_property.text)
        tts = gTTS(text="{title}".format(title=self.text_input_property.text), lang='en')
        tts.save("test.mp3")
        sound = SoundLoader.load('test.mp3')
        if sound:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            sound.play()

    def create_text_to_speech_mp3_file(self, instance):
        if len(self.create_text_to_speech_text.text) <= 0 or len(self.create_text_to_speech_filename.text) <= 0:
            # TODO: Pop up a message saying "Enter text or filename"
            return
        tts = gTTS(text="{text}".format(text=self.create_text_to_speech_text.text), lang='en')
        tts.save("speeches/{filename}.mp3".format(filename=self.create_text_to_speech_filename.text))

    def __init__(self, **kwargs):
        super(SpeechCreateWidget, self).__init__(**kwargs)


class TTSRootWidget(BoxLayout):
    pass

class Main1App(App):
    pass

if __name__ == '__main__':
    Main1App().run()
