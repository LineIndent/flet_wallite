""" Wallet App using the Flet Library """

""" Milestones/Roadmap:
        1. Entry validation
        2. Entry success banner
        3. Add copy/paste function using pyperclip pip3 install pyperclip 
        4. Attach local database (sqlite3)
        
"""

""" The modules we need for this app """
import flet
from flet import (
    Page,
    Text,
    AlertDialog,
    TextField,
    TextButton,
    Column,
    Container,
    LinearGradient,
    alignment,
    border_radius,
    padding,
    Image,
    colors,
    UserControl,
    Row,
    IconButton,
)

""" Class to generate cards """


class App(UserControl):
    # Color counter
    global ColorPick
    ColorPick = 0

    # list of colors to generate gradients for our cards
    ColorList = {
        "start": ["#13547a", "#f43b47", "#30cfd0", "#243949"],
        "end": ["#80d0c7", "#453a94", "#330867", "#517fa4"],
    }

    """ Build method returns the UI to screen """

    def build(self):
        """We start off with the title and the insert button"""
        # the button here is set up as a variable, which we can call later on
        self.InsertButton = Container(
            content=IconButton(
                on_click=lambda e: self.OpenEntryForm(),
                icon="add",
                icon_size=15,
            ),
            alignment=alignment.center_right,
            padding=padding.only(0, 0, 10, 0),
        )

        # Title at the top
        self.Title = Text(value="Wallite", size=22)

        # This is a row set to self.cardwallet, and is the row which will be appended when we create a new card.
        # Orginal ==> column()
        self.CardWallet = Row()

        """ UI/UX for entry form """
        # HEre are the input text fields
        # The entry form is set up as a dialogue, so we need to open and close it accordingly
        self.CardName = TextField(
            label="Card Name",
            border="underline",
            text_size=12,
        )

        self.CardNumber = TextField(
            label="Card Number",
            border="underline",
            text_size=12,
        )

        """ Entry Form Input """
        """ This is the entry form that will be called when opened is set to True"""
        # These can be changed as needed
        self.EntryForm = AlertDialog(
            title=Text(
                "Enter Your Bank Name\nCard Number",
                text_align="center",
                size=12,
            ),
            content=Column(
                [
                    self.CardName,
                    self.CardNumber,
                ],
                spacing=20,
                height=180,
            ),
            actions=[
                # These actions fire when they are clicked.
                TextButton("Insert", on_click=lambda e: self.CheckEntryForm()),
                TextButton("Cancel", on_click=lambda e: self.CancelEntryForm()),
            ],
            actions_alignment="center",
            on_dismiss=lambda e: self.CancelEntryForm(),
        )

        """ Main display of UI """
        return Column(
            controls=[
                Row(
                    controls=[
                        self.EntryForm,
                        Container(
                            width=160,
                            content=(self.Title),
                            padding=padding.all(10),
                        ),
                        Container(
                            width=160,
                            content=(self.InsertButton),
                            alignment=alignment.center_right,
                            padding=padding.all(10),
                        ),
                    ],
                    alignment="spaceAround",
                ),
                # Original => column
                Row(
                    wrap=False,
                    scroll="auto",
                    controls=[
                        self.CardWallet,
                    ],
                ),
            ],
        )

    """ Now for the card generator """

    def CardMaker(self):
        # call the color counter here,
        global ColorPick

        # Set an image property for the card type => mastercard/visa/ etc...
        """ Images for card """
        self.img = Image()
        if self.CardNumber.value[0] == "4":
            self.img = Image(
                src=f"https://img.icons8.com/external-tal-revivo-bold-tal-revivo/384/000000/external-visa-an-american-multinational-financial-services-corporation-logo-bold-tal-revivo.png",
                width=80,
                height=80,
                fit="contain",
            )
        elif self.CardNumber.value[0] == "5":
            self.img = Image(
                src=f"https://img.icons8.com/color/1200/000000/mastercard-logo.png",
                width=80,
                height=80,
                fit="contain",
            )
        elif self.CardNumber.value[0] == "3":
            # Need an AMEX logo here
            pass
        else:
            pass

        """ Create a variable to append the controls of the build """
        # 1. start wit ha container
        self.card = Container(
            # we will need a column that will start with the bank name and then a row that will have, side by side card number and logo
            content=Column(
                controls=[
                    # 2. second contianer for the card name
                    Container(
                        content=(
                            Text(
                                self.CardName.value,
                                size=20,
                            )
                        ),
                        # align it top left
                        alignment=alignment.top_left,
                    ),
                    # 3. A row at the end of the column, with tow continaers
                    Row(
                        controls=[
                            TextButton(
                                content=Container(
                                    alignment=alignment.bottom_left,
                                    content=Column(
                                        [
                                            Text(
                                                value=f"•••• •••• •••• {self.CardNumber.value[-4:]}",
                                                size=14,
                                                color=colors.WHITE,
                                                height=20,
                                            ),
                                        ],
                                    ),
                                ),
                                on_click=None,
                            ),
                            Container(
                                content=(self.img),
                                alignment=alignment.bottom_right,
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                ],
                alignment="spaceBetween",
            ),
            # HEre we set some ui properties for the card shape
            border_radius=border_radius.all(20),
            width=280,
            height=180,
            padding=padding.all(10),
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=[
                    # For the colors, we call the dictioanry above and pick the element per index
                    App.ColorList["start"][ColorPick],
                    App.ColorList["end"][ColorPick],
                ],
            ),
        )
        # increase the global count
        ColorPick += 1

        # Append the self.cardwallet variable in the build
        self.CardWallet.controls.append(self.card)
        # Remove items from the entires
        self.CancelEntryForm()
        # Update the view
        self.update()

    """ Some minimal validation """

    def CheckEntryForm(self):
        if len(self.CardNumber.value) == 0:
            self.CardNumber.error_text = "Please enter your card number!"
            self.update()
        else:
            self.CardNumber.error_text = None
            self.update()

        if len(self.CardName.value) == 0:
            self.CardName.error_text = "Please enter your cvv!"
            self.update()
        else:
            self.CardName.error_text = None
            self.update()

        if len(self.CardNumber.value) & len(self.CardName.value) != 0:
            self.CardMaker()

    """ Opening the entry form """

    def OpenEntryForm(self):
        # we set the current dialogue to the UI, in this case called self.EntryForm
        self.dialog = self.EntryForm
        # set .open = True
        self.EntryForm.open = True
        # Update view
        self.update()

    """ If cancel is clicked """

    def CancelEntryForm(self):
        self.CardName.value, self.CardNumber.value = None, None
        self.CardNumber.error_text, self.CardName.error_text = None, None
        self.EntryForm.open = False
        self.update()


""" We start with a function that sets up the root view """


def start(page: Page):
    """title"""
    page.title = "Wallite"
    """ the column alignment of the root view = start = from top to bottom"""
    page.vertical_alignment = "start"
    """ dimensions """
    page.window_width = 320
    page.window_height = 600
    """ You can also center the app to the middle of the screen"""
    # page.window_center()
    """ scrolling if the ui goes beyound the height of the app """
    page.scroll = "auto"
    """ upddate the view """
    page.update()

    """ Here, we create an instance of a class """
    app = App()
    page.add(app)


if __name__ == "__main__":
    flet.app(target=start)
