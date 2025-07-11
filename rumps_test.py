import rumps
import sys
import logging

logging.basicConfig(filename='myapp.log', level=logging.DEBUG)

class MyApp(rumps.App):
    def __init__(self):
        super(MyApp, self).__init__("My App")
        self.menu = ["Test", "Quit"]
        logging.debug("App initialized")

    @rumps.clicked("Test")
    def test(self, _):
        logging.debug("Test clicked")
        rumps.notification("Test", "Notification", "This is a test notification")

    @rumps.clicked("Quit")
    def quit(self, _):
        logging.debug("Quit clicked")
        rumps.quit_application()

if __name__ == "__main__":
    logging.debug("Script started")
    if len(sys.argv) > 1 and sys.argv[1] == 'background':
        app = MyApp()
        app.run()
    else:
        import subprocess
        subprocess.Popen([sys.executable, sys.argv[0], 'background'])