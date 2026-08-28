📌 🖥️ Telegram Wake-on-LAN Bot

A small Telegram bot that lets you wake up a sleeping computer over the local network by sending a /wake command.

✏ How it works

The bot listens for the /wake <name> command, looks up the MAC address for that name, and shells out to the [wakeonlan](https://github.com/cobbler/wakeonlan) CLI tool to broadcast a magic packet. Only pre-authorised Telegram chat IDs are allowed to use it.

✏ Prerequisites

⦁ Python 3.10+
⦁ *wakeonlan* installed on the machine running the bot (the CLI tool, not the Python package)
⦁ The bot must run on a machine on the same LAN as the target computers
⦁ Wake-on-LAN enabled in the target's BIOS/UEFI
# Python dependency

`pip install python-telegram-bot wakeonlan`

✏ Environment variables

The bot reads three variables at startup:

Variable  | Format                        | Example                                        | Description
----------+-------------------------------+------------------------------------------------+-----------------------------------------
TOKEN     | string                        | 123456:ABC-DEF…                                | Your bot token from @BotFather
VALID_IDS | pipe-separated ints           | 111111|222222                                  | Telegram chat IDs allowed to use the bot
COMPUTERS | pipe-separated name-MAC pairs | office-00:11:22:33:44:55|lab-aa:bb:cc:dd:ee:ff | The computers you can wake

How to find your Telegram chat ID: message @userinfobot on Telegram.

How to find a MAC address:
⦁ Windows: getmac /v
⦁ Linux: ip link show
⦁ macOS: ifconfig

📚 Example .env / shell export

export TOKEN="123456:ABC-your-real-token"
export VALID_IDS="111111|222222"
export COMPUTERS="office-00:11:22:33:44:55|lab-aa:bb:cc:dd:ee:ff"

✏ Running

python bot.py

You should see your chat IDs and the VALID_IDS value printed to stdout, followed by the bot starting its polling loop.

✏ Usage

Send these commands to the bot on Telegram:

Command      | What it does
-------------+-----------------------------------------------
/wake <name> | Sends a WOL magic packet to the named computer
/help        | Shows a short usage hint

📚 Examples

/wake office
→ "Your computer is waking up"

/wake
→ "wake what? your choices: office, lab"

/wake kitchen
→ "unknown computer, your choices: office, lab"

/wake office lab
→ "too many arguments, send only one"

Unauthorised chat IDs get a terse "Who are you?? Get lost" reply.

✏ Project structure

bot.py          ← the entire bot (single file)

✏ Troubleshooting

Symptom                                     | Likely cause
--------------------------------------------+-------------------------------------------------------------------
KeyError: 'TOKEN' (or VALID_IDS, COMPUTERS) | Environment variable not set in the shell where you launch the bot
wakeonlan: command not found                | The CLI tool isn't installed or isn't on $PATH
No response from the target                 | WOL disabled in BIOS, wrong MAC, or bot not on the same subnet
"Who are you?? Get lost"                    | Your chat ID isn't in VALID_IDS

✏ License

MIT — do whatever you want with it.
