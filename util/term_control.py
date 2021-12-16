'''
	Further reading
	https://ss64.com/nt/syntax-ansi.html
	https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
'''


import os
import colorama

class TermControl:
	def clear():
		os.system('cls' if os.name == 'nt' else 'clear')
