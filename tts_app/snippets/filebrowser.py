from kivy.app import App
from os.path import sep, expanduser, isdir, dirname
from kivy.garden.filebrowser import FileBrowser

class TestApp(App):

    def build(self):
        user_path = expanduser('~') + sep + 'Documents'
        browser = FileBrowser(select_string='Select',
                              favorites=[(user_path, 'Documents')])
        browser.bind(
                    on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled)
        return browser

    def _fbrowser_canceled(self, instance):
        print 'cancelled, Close self.'

    def _fbrowser_success(self, instance):
        print instance.selection

if __name__=='__main__':
    TestApp().run()
