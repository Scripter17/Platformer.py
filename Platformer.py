#    Platformer.py v1.4.0
# James C. Wise - 2020-04-17 
#  See LICENSE.md for legal

# Note to self: Up=H Right=P Down=M Left=K (HPMK)

import colorama, os, subprocess as sp, keyboard, time, ctypes, msvcrt, atexit
colorama.init()

# === GROSS ASS CTYPED BULLSHIT ===
def setCursorVisible(b=False):
	class _CursorInfo(ctypes.Structure):
		_fields_ = [("size", ctypes.c_int),
		("visible", ctypes.c_byte)]
	ci = _CursorInfo()
	handle = ctypes.windll.kernel32.GetStdHandle(-11)
	ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
	ci.visible = b
	ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
setCursorVisible(False)

# === ONEXIT HANDLING ===
def onExit():
	setCursorVisible(True)
	while msvcrt.kbhit():
		msvcrt.getch()
atexit.register(onExit)
def cursorPos(x, y):
	return "\033["+str(y+1)+";"+str(x+1)+"H"

class Player:
	class maps:
		p1of1={"up":"U", "right":"R", "down":"D", "left":"L", "space"    :"S", "ctrl"                   :"C"}
		p1of2={"up":"U", "right":"R", "down":"D", "left":"L", "backslash":"S", "right alt OR right ctrl":"C"}
		p2of2={"r" :"U", "g"    :"R", "f"   :"D", "d"   :"L", "s"        :"S", "a"                      :"C"}
		p1char="@"
		p2char="!"
	def __init__(this, buttonMapping=maps.p1of1, char=maps.p1char, pos=[0, 0], fallTimer=None):
		this.buttonMapping=buttonMapping
		this.char=char
		this.pos=pos
		this.fallTimer=time.time() if fallTimer==None else fallTimer
	def getButtons(this):
		"""buttons=""
		if keyboard.is_pressed("up")     : buttons+="U" # Phase up 3 blocks
		if keyboard.is_pressed("right")  : buttons+="R" # Move right
		if keyboard.is_pressed("down")   : buttons+="D" # Stop falling
		if keyboard.is_pressed("left")   : buttons+="L" # Move right
		if keyboard.is_pressed("space")  : buttons+="S" # Phase up 5 blocks
		if keyboard.is_pressed("control"): buttons+="C" # CTRL+Right / CTRL+Left phase sidewats 2 blocks
		return buttons"""
		buttons=""
		for keyList in this.buttonMapping:
			if any([keyboard.is_pressed(x) for x in keyList.split(" OR ")]): buttons+=this.buttonMapping[keyList]
		return buttons
	def isWall(this, dx=0, dy=0, blocks="#"):
		#sp.run(["title",str([p.pos==[this.pos[0]+dx, this.pos[1]+dy] and this!=p for p in players])], shell=True)
		return (mapData[this.pos[1]+dy][this.pos[0]+dx] in blocks) or any([p.pos==[this.pos[0]+dx, this.pos[1]+dy] and this!=p for p in players])
	def printSelf(this):
		#sp.run(["title", str(this.pos)], shell=True)
		print(cursorPos(this.pos[0], this.pos[1])+"\033[33m"+this.char+"\033[39m")

blockPre={
	" ":"",
	"#":"",
	"X":"\033[31m",
	"O":"\033[32m"
}
blockPost="\033[39m"

# === MAP SELECT AND INITIALIZING ===
mapList=[x for x in os.listdir() if x.endswith(".map") and os.path.isfile(x)]
mapIndex=0
if len(mapList)==0:
	print("No maps detected!\nPress any key to exit")
	msvcrt.getch()
	exit()
else:
	t=str(mapIndex)
	while True:
		print(">>> "+mapList[mapIndex])
		# Gross ass msvcrt black magic because the keyboard module has failed me
		key=msvcrt.getch()
		if key==b"\xe0" : key+=msvcrt.getch()
		if key==b"\xb1" : exit()
		if key==b"\r"   : break
		if key==b"\xe0H": mapIndex=(mapIndex+1)%len(mapList)
		if key==b"\xe0P": mapIndex=(mapIndex-1+len(mapList))%len(mapList)
		print("\033[1A\033[2K", end="")


mapText=open(mapList[mapIndex], "r").read()

def indexLineNumber(string, sub):
	if not (sub in string):
		return -1
	return len(string[:string.index(sub)+1].splitlines())-1
def indexOnLine(string, sub, line=None):
	if line==None:
		line=indexLineNumber(string, sub)
	if line==-1:
		return -1
	if not (sub in string.splitlines()[line]):
		return -1
	return string.splitlines()[line].index(sub)
players=[]
buttons=[]
if "@" in mapText:
	if "!" in mapText:
		players.append(Player(Player.maps.p1of2, char=Player.maps.p1char, pos=[indexOnLine(mapText, Player.maps.p1char), indexLineNumber(mapText, Player.maps.p1char)]))
		buttons.append("")
		players.append(Player(Player.maps.p2of2, char=Player.maps.p2char, pos=[indexOnLine(mapText, Player.maps.p2char), indexLineNumber(mapText, Player.maps.p2char)]))
		buttons.append("")
	else:
		players.append(Player(Player.maps.p1of1, char=Player.maps.p1char, pos=[indexOnLine(mapText, Player.maps.p1char), indexLineNumber(mapText, Player.maps.p1char)]))
		buttons.append("")
#while True:
#	for p in players:
#		print(p, p.getButtons())
#	time.sleep(0.1)
mapData=[]
for yi, y in enumerate(mapText.splitlines()):
	mapLine=[]
	for xi, x in enumerate(y):
		# Doing using a 2d array of chars instead of a 1d list of strings in case I need to edit map data mid-game
		if x in "@!":
			mapLine.append(" ")
		else:
			mapLine.append(x)
	mapData.append(mapLine)
mapWidth=max(*[len(x) for x in mapData]) if len(mapData)!=0 else 0
if mapWidth==0:
	print("The map selected is empty; Try another map")
	msvcrt.getch()
	exit()
for yi, y in enumerate(mapData):
	# Pad lines that don't extend to the bounding box
	mapData[yi]+=[" "]*(mapWidth-len(y))

# === CLEAR WINDOW AND SET TITLE ===
sp.run("cls", shell=True)
sp.run(["title", mapList[mapIndex]], shell=True)

fallTimer=time.time() # You only fall every 0.5 seconds (Well it's every 0.6 because the vFPS is 0.2 but whatever)
while True:
	# Print screen
#	if "".join(buttons)!="": # If there's no player input, don't reprint the map
	for yi, y in enumerate(mapData):
		for xi, x in enumerate(mapData[yi]):
			if not [xi, yi] in [p.pos for p in players]:
				print(cursorPos(xi, yi)+(blockPre[x] if x in blockPre.keys() else "")+x+blockPost)
	# Calculate death/win conditions
	for pi, p in enumerate(players):
		if p.pos[1]==len(mapData)-1 or p.isWall(0, 0, "X"):
			print("\033[2J\033[1;1HDead\nPress any key to continue")
			msvcrt.getch()
			exit()
		elif p.isWall(0, 0, "O"):
			print("\033[2J\033[1;1HWin\nPress any key to continue")
			msvcrt.getch()
			exit()
		# Erase player
		# If there's no player movement but you're falling, this prevents a trail from happening
		print(cursorPos(p.pos[0], p.pos[1])+mapData[p.pos[1]][p.pos[0]])
		# Compute next position
		hphase=1+int("C" in buttons[pi])
		if "R" in buttons[pi] and p.pos[0]+hphase<mapWidth and not p.isWall( hphase, 0)  : p.pos[0]+=hphase
		if "L" in buttons[pi] and p.pos[0]-hphase>=0       and not p.isWall(-hphase, 0)  : p.pos[0]-=hphase
		if "U" in buttons[pi] and p.pos[1]-3>=0 and p.isWall(0, 1) and not p.isWall(0, -3): p.pos[1]-=3
		if "S" in buttons[pi] and p.pos[1]-5>=0 and p.isWall(0, 1) and not p.isWall(0, -5): p.pos[1]-=5
		if p.isWall(0, 1): p.fallTimer=time.time()
		if not p.isWall(0, 1) and not ("D" in buttons) and time.time()-p.fallTimer>0.5: p.pos[1]+=1; p.fallTimer=time.time()
		#print(cursorPos(pos[0], pos[1])+blockPre["@"]+"@"+blockPost) # Print player
		p.printSelf()
	for p in range(len(players)):
		buttons[p]=""
	for i in range(12):
		for pi, p in enumerate(players):
			# Checks for buttons every 60th of a second but only does physics every 5th of a second
			# It is a very stupid solution but it works
			buttons[pi]+=p.getButtons()
		time.sleep(1/60)
