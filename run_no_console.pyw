from main.discord import DiscordPcStatus
from sys import exit

if __name__ == "__main__":
	DiscordRPC = DiscordPcStatus()
	DiscordRPC.start()
	exit()