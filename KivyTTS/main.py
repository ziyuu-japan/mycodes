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
#nice
class FileSelectPlusPlayWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(FileSelectPlusPlayWidget, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.file_select_button = Button(text="Select mp3 file")
        self.filename_label = Label(text="File Name")
        upper_boxlayout = BoxLayout()
        upper_boxlayout.add_widget(self.filename_label)
        upper_boxlayout.add_widget(self.file_select_button)
        self.speech_button = Button(text="Speech")

        self.add_widget(upper_boxlayout)
        self.add_widget(self.speech_button)

    def bind_file_select_button_to(self, callback):
        self.file_select_button.bind(on_press=callback)
        print(self, callback)

    def bind_speech_button_to(self, callback):
        self.speech_button.bind(on_press=callback)

    def change_filename_label_text(self, text):
        self.filename_label.text= text

class PlaySpeechWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(PlaySpeechWidget, self).__init__(**kwargs)
        self.speechfile_name = ""

        self.select_plus_speech_layout = FileSelectPlusPlayWidget()
        self.select_plus_speech_layout.bind_file_select_button_to(self.switch_to_filebrowser)
        self.select_plus_speech_layout.bind_speech_button_to(self.speech)
        self.add_widget(self.select_plus_speech_layout)

        self.filebrowser_widget = FileBrowser(select_string='Select',
            favorites=[(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'speeches'), 'speeches')])
        self.filebrowser_widget.bind(
                    on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled)

    def switch_to_filebrowser(self, instance):
        self.clear_widgets()
        self.add_widget(self.filebrowser_widget)

    def _fbrowser_canceled(self, instance):
        self.clear_widgets()
        self.add_widget(self.select_plus_speech_layout)

    def _fbrowser_success(self, instance):
        # instance.selection[0] has a abs path of a file user selected.
        # and then get only the filename
        self.speechfile_name = self.get_filename_from_absfilepath(instance.selection[0])
        # change filename_label text to the selected filename
        self.select_plus_speech_layout.change_filename_label_text(self.speechfile_name)

        self.clear_widgets()
        self.add_widget(self.select_plus_speech_layout)

    def speech(self, instance):
        sound = SoundLoader.load('speeches/{}'.format(self.speechfile_name))
        if sound:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            sound.play()

    def get_filename_from_absfilepath(self, absfilepath):
        abs_parentdirpath, filename = os.path.split(absfilepath)
        return filename



class SpeechCreateWidget(BoxLayout):

    create_text_to_speech_text = ObjectProperty()
    create_text_to_speech_filename = ObjectProperty()

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

class MainApp(App):
    pass

if __name__ == '__main__':
    MainApp().run()
