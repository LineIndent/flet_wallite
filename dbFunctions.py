import aiosqlite

# Database class
class Database:
    # we create a db, table, and return the db in this function
    async def ConnectDatabase(**kwargs):
        try:
            db = await aiosqlite.connect("./example.db")
            c = await db.cursor()
            await c.execute(
                "CREATE TABLE if not exists wallite (Bank TEXT, CardNumber TEXT, CVV TEXT)"
            )
            await db.commit()
            return db
        except:
            print("Error")

    # this function takes in one argument, values, which we will pass the user's input in.
    async def InsertDatabase(db, values):
        c = await db.cursor()
        await c.execute(
            "INSERT INTO wallite (Bank, CardNumber, CVV) VALUES (?, ?, ?)",
            values,
        )
        await db.commit()

    # this function reads the database so we can reimport the card details when we close and re-open the app.
    async def ReadDatabase(db):
        c = await db.cursor()
        await c.execute("SELECT Bank, CardNumber, CVV FROM wallite")
        records = await c.fetchall()
        return records
