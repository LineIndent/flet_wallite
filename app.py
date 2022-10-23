""" Wallet App using the Flet Library """


""" THe modules we need for this app """

# asyncio is used for database async operations
import asyncio
import flet
from flet import (
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
    UserControl,
    Row,
    IconButton,
    margin,
    icons,
    border,
    Card,
    transform,
    animation,
    Icon,
    SnackBar,
)

# python files being imported
from settings import ColorList as cl
from dbFunctions import Database

# external library that allos copy to clipboard function
import clipboard


class App(UserControl):
    global HeightCount
    HeightCount = 25

    global ColorCount
    ColorCount = 0

    global CardCount
    CardCount = 0

    global DataDict
    DataDict = {}

    # Wallet contianer that will hold the cards
    def WalletContainer(self):

        # Some variables set as components
        self.CardList = Column(
            alignment="start",
            spacing=25,
        )

        self.ImportButton = IconButton(
            icon=icons.DOWNLOAD,
            icon_size=16,
            on_click=lambda e: asyncio.run(self.CheckDatabase()),
        )

        self.InsertButton = IconButton(
            icon=icons.ADD,
            icon_size=16,
            on_click=lambda e: self.OpenEntryForm(),
            disabled=True,
        )

        self.WalletContainer = Container(
            # alignment=alignment.center_right,
            # padding=padding.only(right=200),
            # Use CARD to get elevation feature
            content=Card(
                elevation=15,
                content=Container(
                    content=Column(
                        scroll="auto",
                        alignment="start",
                        spacing=25,
                        controls=[
                            self.snack,
                            Row(
                                alignment="spaceBetween",
                                controls=[
                                    # Title of the app
                                    Text(
                                        "Wallite", color="white", size=20, weight="bold"
                                    ),
                                    # Container with the icon buttons
                                    Container(
                                        content=Row(
                                            spacing=0,
                                            tight=True,
                                            alignment="end",
                                            controls=[
                                                self.InsertButton,
                                                self.ImportButton,
                                            ],
                                        )
                                    ),
                                ],
                            ),
                            Container(
                                content=Column(
                                    controls=[self.CardList],
                                ),
                            ),
                        ],
                    ),
                    width=360,
                    height=580,
                    padding=padding.all(20),
                    alignment=alignment.top_center,
                    border_radius=border_radius.all(15),
                    gradient=self.GradientGenerator(
                        cl.WALLITE["from"], cl.WALLITE["to"]
                    ),
                ),
            ),
        )

        return self.WalletContainer

    # Entry form function
    def EntryForm(self):

        # Set three variables as the entry form text fields
        self.BankName = TextField(
            label="Card Name",
            border="underline",
            text_size=12,
        )

        self.CardNumber = TextField(
            label="Card Number",
            border="underline",
            text_size=12,
        )

        self.CardCVV = TextField(
            label="Card CVV",
            border="underline",
            text_size=12,
        )

        # We need to seperate functions to open and close the dialog
        self.EntryForm = AlertDialog(
            title=Text(
                "Enter Your Bank Name\nCard Number",
                text_align="center",
                size=12,
            ),
            content=Column(
                [
                    self.BankName,
                    self.CardNumber,
                    self.CardCVV,
                ],
                spacing=15,
                height=280,
            ),
            actions=[
                # These actions fire when they are clicked.
                TextButton("Insert", on_click=lambda e: self.CheckEntryForm()),
                TextButton("Cancel", on_click=lambda e: self.CancelEntryForm()),
            ],
            actions_alignment="center",
            on_dismiss=lambda e: self.CancelEntryForm(),
        )

        return self.EntryForm

    # Main UI component
    def CardGenerator(self, bank, number, cvv):
        # We need these globals to carry oout several functions
        global HeightCount
        global ColorCount
        global CardCount
        global DataDict

        # NOTE: Need more images to be associated with card type. We'll be using just one for demonstration purposes
        self.img = Image(
            src=f"https://img.icons8.com/color/1200/000000/mastercard-logo.png",
            width=80,
            height=80,
            fit="contain",
        )

        # These are the values we passed into the function when we called it.
        self.bank = bank
        self.number = number
        self.cvv = cvv

        # We created a global dictionary so that we can store the data associated with each card.
        # What's happening to the dictionary is we add a nested dictioanry called CardCount, which is a number that increases with every added card, to which we add two keys or items, a number and a cvv.
        # Now the number and cvv can be accessed by clicking their respective contianers
        DataDict[CardCount] = {"number": f"{self.number}", "cvv": f"{self.cvv}"}

        # Main UI compoenent
        self.CardTest = Card(
            elevation=20,
            content=Container(
                content=(
                    Column(
                        controls=[
                            Row(
                                alignment="spaceBetween",
                                controls=[
                                    Column(
                                        spacing=1,
                                        controls=[
                                            Container(
                                                alignment=alignment.bottom_left,
                                                content=Text(
                                                    "BANK NAME",
                                                    color="gray",
                                                    size=9,
                                                    weight="w500",
                                                ),
                                            ),
                                            Container(
                                                alignment=alignment.top_left,
                                                content=Text(
                                                    # user input bank name
                                                    self.bank,
                                                    color="#e2e8f0",
                                                    size=20,
                                                    weight="w700",
                                                ),
                                            ),
                                        ],
                                    ),
                                    Icon(
                                        # settings icon for further functionality
                                        name=icons.SETTINGS_OUTLINED,
                                        size=16,
                                    ),
                                ],
                            ),
                            Container(
                                padding=padding.only(
                                    top=10,
                                    bottom=20,
                                ),
                            ),
                            Row(
                                alignment="spaceBetween",
                                controls=[
                                    Column(
                                        spacing=1,
                                        controls=[
                                            Container(
                                                alignment=alignment.bottom_left,
                                                content=Text(
                                                    "CARD NUMBER",
                                                    color="gray",
                                                    size=9,
                                                    weight="w500",
                                                ),
                                            ),
                                            Container(
                                                alignment=alignment.top_left,
                                                content=Text(
                                                    # card number input
                                                    f"**** **** **** {self.number[-4:]}",
                                                    color="#e2e8f0",
                                                    size=15,
                                                    weight="w700",
                                                ),
                                                data=(DataDict[CardCount]["number"]),
                                                on_click=lambda e: self.GetValue(e),
                                            ),
                                            Container(
                                                bgcolor="pink",
                                                padding=padding.only(
                                                    bottom=5,
                                                ),
                                            ),
                                            Container(
                                                alignment=alignment.bottom_left,
                                                content=Text(
                                                    "CVV NUMBER",
                                                    color="gray",
                                                    size=9,
                                                    weight="w500",
                                                ),
                                            ),
                                            Container(
                                                alignment=alignment.top_left,
                                                content=Text(
                                                    f"**{self.cvv[-1:]}",
                                                    color="#e2e8f0",
                                                    size=13,
                                                    weight="w700",
                                                ),
                                                data=DataDict[CardCount]["cvv"],
                                                on_click=lambda e: self.GetValue(e),
                                            ),
                                        ],
                                    ),
                                    Column(
                                        horizontal_alignment="end",
                                        controls=[self.img],
                                    ),
                                ],
                            ),
                        ]
                    )
                ),
                padding=padding.all(12),
                margin=margin.all(-5),
                width=310,
                height=185,
                border_radius=border_radius.all(18),
                gradient=self.GradientGenerator(
                    cl.CARDCOLORS["from"][ColorCount],
                    cl.CARDCOLORS["to"][ColorCount],
                ),
            ),
        )

        # Make sure to increase the globals here
        CardCount += 1
        ColorCount += 1
        HeightCount += 50

        # Append the new card to the wallet contianer
        self.CardList.controls.append(self.CardTest)
        self.CancelEntryForm()
        self.update()

    # Final function = we can copy the card number and cvv using the clipboard module
    def GetValue(self, e):
        clipboard.copy(e.control.data)
        self.snack.open = True
        self.update()

    # Method that gneerates the gradients for backgrounds
    def GradientGenerator(self, start, end):
        self.ColorGradient = LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=[
                start,
                end,
            ],
        )

        return self.ColorGradient

    """ Test copy function 

            3874 2344 2343 2343
            5476 7634 7634 7364
            4637 7634 3476 3464
            
            000
            123
            
            
    
    """

    # Some minor validation before sending data to card generator and database
    def CheckEntryForm(self):
        if len(self.CardNumber.value) == 0:
            self.CardNumber.error_text = "Please enter your card number!"
            self.update()
        else:
            self.CardNumber.error_text = None
            self.update()

        if len(self.BankName.value) == 0:
            self.BankName.error_text = "Please enter the name of your bank name!"
            self.update()
        else:
            self.BankName.error_text = None
            self.update()

        if len(self.CardCVV.value) == 0:
            self.CardCVV.error_text = "Please enter your cvv!"
            self.update()
        else:
            self.CardCVV.error_text = None
            self.update()

        if (
            len(self.CardNumber.value)
            & len(self.BankName.value)
            & len(self.CardCVV.value)
            != 0
        ):

            # Here, we pass the values as arguments to the card generator, and we also call the function to insert values into database.
            asyncio.run(self.InsertDataIntoDatabase())
            self.CardGenerator(
                self.BankName.value, self.CardNumber.value, self.CardCVV.value
            )

    def OpenEntryForm(self):
        self.dialog = self.EntryForm
        self.EntryForm.open = True
        self.update()

    # Cancel entry = close entry
    def CancelEntryForm(self):
        self.BankName.value, self.CardNumber.value, self.CardCVV.value = (
            None,
            None,
            None,
        )
        self.CardNumber.error_text, self.BankName.error_text, self.CardCVV.value = (
            None,
            None,
            None,
        )
        self.EntryForm.open = False
        self.update()

    # Insert into database
    async def InsertDataIntoDatabase(self):
        # open a new connection to the db
        db = await Database.ConnectDatabase()
        # pass the values from the user into the database
        await Database.InsertDatabase(
            db, (self.BankName.value, self.CardNumber.value, self.CardCVV.value)
        )
        await db.commit()
        await db.close()

    # Check database to see if there are records
    async def CheckDatabase(self):
        db = await Database.ConnectDatabase()
        records = await Database.ReadDatabase(db)
        # if there are records,
        if records:
            for i, __ in enumerate(records):
                # pass the record data into the cardgenerator function to create the cards
                self.CardGenerator(records[i][0], records[i][1], records[i][2])

            # disable the import function and turn on the add function
            self.ImportButton.disabled = True
            self.InsertButton.disabled = False
            self.update()
        # If there are no records,
        else:
            # Turn on the insert button and turn off the import button
            self.InsertButton.disabled = False
            self.ImportButton.disabled = True
            self.update()

    # build function returns the main component where all other controls are added to.
    def build(self):
        # Card column is the main column where all other controls are added
        self.CardColumn = Column()

        # Snack bar used to notify user that number has been copied
        self.snack = SnackBar(Text("Number copied!"))

        return Container(
            content=(
                Column(
                    alignment="center",
                    controls=[
                        self.EntryForm(),
                        self.WalletContainer(),
                    ],
                )
            ),
            width=900,
            height=800,
            margin=margin.all(-10),
            gradient=self.GradientGenerator(cl.BACKGROUND["from"], cl.BACKGROUND["to"]),
            alignment=alignment.center,
        )
