""" UPDATE on Wallite app """

""" THe modules """
import flet
from flet import Page
from app import App

""" Main function that starts the app """


def start(page: Page):

    # TITLE of app
    page.title = "Wallite"

    # App dimensions
    page.window_width = 450
    page.window_height = 790

    # Update
    page.update()

    # Call the App() class from app.py file
    app = App()
    # Add the instance of App() ==> app to the root page
    page.add(app)


if __name__ == "__main__":
    flet.app(target=start)

""" The files used in this final build 
        1. dbFunctions.py ==> database stuff,
        2. main.py ==> THIS file that starts the app build,
        3. app.py ==> UI build and main application components,
        4. settings.py ==> color class  

"""
