import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Bot API Token (IDE ÍRD BE A TOKENED)
API_TOKEN = '8155014777:AAEwMDwt5e2Hqqkf1lPNr9xAb3XAVcWhNe0'

# Bankroll fájl neve
BANKROLL_FILE = "bankroll.txt"

# Bankroll betöltése fájlból
def load_bankroll():
    if os.path.exists(BANKROLL_FILE):
        with open(BANKROLL_FILE, "r") as file:
            return int(file.read())
    return 100000  # Alapértelmezett bankroll

# Bankroll mentése fájlba
def save_bankroll(value):
    with open(BANKROLL_FILE, "w") as file:
        file.write(str(value))

# Bankroll kezdőérték betöltése
bankroll = load_bankroll()

# Bankroll lekérdezése
async def get_bankroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Jelenlegi bankroll: {bankroll} Ft.")

# Fogadás hozzáadása
async def add_bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bankroll
    try:
        tét = int(context.args[0])
        odds = float(context.args[1])
        eredmény = context.args[2].lower()

        if eredmény == "nyer":
            nyeremény = tét * odds
            bankroll += nyeremény
            save_bankroll(bankroll)
            üzenet = f"Nyeremény: {nyeremény:.2f} Ft. Új bankroll: {bankroll:.2f} Ft."
        elif eredmény == "veszít":
            bankroll -= tét
            save_bankroll(bankroll)
            üzenet = f"Veszteség: {tét} Ft. Új bankroll: {bankroll:.2f} Ft."
        else:
            üzenet = "Hibás eredmény! Csak 'nyer' vagy 'veszít' lehet."

        await update.message.reply_text(üzenet)
    except IndexError:
        await update.message.reply_text("Használat: /add_bet <tét> <odds> <nyer/veszít>")
    except ValueError:
        await update.message.reply_text("Kérlek, helyes formátumot adj meg (pl. /add_bet 1000 2.5 nyer)")

# 5%-os tét egység kiszámítása
async def auto_bet_unit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bet_unit = bankroll * 0.05
    await update.message.reply_text(f"Az aktuális bankroll alapján az 5%-os tét egység: {bet_unit:.2f} Ft.")

# Bankroll manuális frissítése
async def set_bankroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bankroll
    try:
        új_érték = int(context.args[0])
        bankroll = új_érték
        save_bankroll(bankroll)
        await update.message.reply_text(f"Az új bankroll értéke: {bankroll} Ft.")
    except (IndexError, ValueError):
        await update.message.reply_text("Használat: /set_bankroll <új érték>")

# Parancsok listázása
async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 **Bankroll Bot Parancsok**:\n\n"
        "/bankroll - Jelenlegi bankroll lekérdezése\n"
        "/add_bet <tét> <odds> <nyer/veszít> - Fogadás hozzáadása\n"
        "/bet_unit - 5%-os tét egység kiszámítása\n"
        "/set_bankroll <új érték> - Bankroll manuális beállítása\n"
        "/help - Parancsok listájának megjelenítése\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# Start parancs
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Üdvözöllek a Bankroll Botban! Írd be a /help parancsot a funkciók listájához.")
    await show_help(update, context)

# Program főfüggvény
def main():
    application = Application.builder().token(API_TOKEN).build()

    # Parancsok regisztrálása
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", show_help))
    application.add_handler(CommandHandler("bankroll", get_bankroll))
    application.add_handler(CommandHandler("add_bet", add_bet))
    application.add_handler(CommandHandler("bet_unit", auto_bet_unit))
    application.add_handler(CommandHandler("set_bankroll", set_bankroll))

    # Bot indítása
    application.run_polling()

if __name__ == "__main__":
    main()
