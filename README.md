# 📌 🖥️ Telegram Wake-on-LAN Bot

A small Telegram bot that lets you wake up a sleeping computer over the local network by sending a `/wake` command.

## ✏️ How it works

The bot listens for the `/wake <name>` command, looks up the MAC address for that name, and shells out to the [`wakeonlan`](https://github.com/cobbler/wakeonlan) CLI tool to broadcast a magic packet.

Only pre-authorised Telegram chat IDs are allowed to use it.

## ✏️ Prerequisites

- Python 3.10+
- `wakeonlan` installed on the machine running the bot (the **CLI tool**, not the Python package)
- The bot must run on a machine on the same LAN as the target computers
- Wake-on-LAN enabled in the target's BIOS/UEFI

### Python dependency

```bash
pip install python-telegram-bot wakeonlan
```

> **Note:** The `wakeonlan` Python package and the `wakeonlan` CLI tool are separate things. The bot shells out to the CLI tool, so make sure the command is available on your `$PATH`.

## ✏️ Environment variables

The bot reads three variables at startup:

| Variable | Format | Example | Description |
|---|---|---|---|
| `TOKEN` | string | `123456:ABC-DEF…` | Your bot token from `@BotFather` |
| `VALID_IDS` | pipe-separated integers | `111111\|222222` | Telegram chat IDs allowed to use the bot |
| `COMPUTERS` | pipe-separated name-MAC pairs | `office-00:11:22:33:44:55\|lab-aa:bb:cc:dd:ee:ff` | The computers you can wake |

### How to find your Telegram chat ID

Message [`@userinfobot`](https://t.me/userinfobot) on Telegram.

### How to find a MAC address

**Windows:**

```powershell
getmac /v
```

**Linux:**

```bash
ip link show
```

**macOS:**

```bash
ifconfig
```

## 📚 Example `.env` / shell export

```bash
export TOKEN="123456:ABC-your-real-token"
export VALID_IDS="111111|222222"
export COMPUTERS="office-00:11:22:33:44:55|lab-aa:bb:cc:dd:ee:ff"
```

> **Security:** Never commit your real bot token to Git. If you accidentally expose it, revoke it through `@BotFather` and generate a new one.

## ✏️ Running

```bash
python bot.py
```

You should see your chat IDs and the `VALID_IDS` value printed to stdout, followed by the bot starting its polling loop.

## ✏️ Usage

Send these commands to the bot on Telegram:

| Command | What it does |
|---|---|
| `/wake <name>` | Sends a WoL magic packet to the named computer |
| `/help` | Shows a short usage hint |

### 📚 Examples

```text
/wake office
→ Your computer is waking up
```

```text
/wake
→ wake what? your choices: office, lab
```

```text
/wake kitchen
→ unknown computer, your choices: office, lab
```

```text
/wake office lab
→ too many arguments, send only one
```

Unauthorised chat IDs get a terse:

```text
Who are you?? Get lost
```

## ✏️ Project structure

```text
bot.py          ← the entire bot (single file)
```

## ✏️ Troubleshooting

| Symptom | Likely cause |
|---|---|
| `KeyError: 'TOKEN'` (or `VALID_IDS`, `COMPUTERS`) | Environment variable not set in the shell where you launch the bot |
| `wakeonlan: command not found` | The CLI tool isn't installed or isn't on `$PATH` |
| No response from the target | WoL disabled in BIOS/UEFI, wrong MAC address, or bot isn't on the same subnet |
| `Who are you?? Get lost` | Your Telegram chat ID isn't in `VALID_IDS` |

## ✏️ License

MIT — do whatever you want with it.
