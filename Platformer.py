#    Platformer.py v1.0.0
# James C. Wise - 2020-04-14 
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

def getButtons():
	buttons=""
	if keyboard.is_pressed("up")     : buttons+="U" # Phase up 3 blocks
	if keyboard.is_pressed("right")  : buttons+="R" # Move right
	if keyboard.is_pressed("down")   : buttons+="D" # Stop falling
	if keyboard.is_pressed("left")   : buttons+="L" # Move right
	if keyboard.is_pressed("space")  : buttons+="S" # Phase up 5 blocks
	if keyboard.is_pressed("control"): buttons+="C" # CTRL+Right / CTRL+Left phase sidewats 2 blocks
	return buttons

pos=[0, 0]
blockPre={
	" ":"",
	"#":"",
	"X":"\033[31m",
	"O":"\033[32m",
	"@":"\033[33m"
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
mapData=[]
for yi, y in enumerate(mapText.splitlines()):
	mapLine=[]
	for xi, x in enumerate(y):
		# Doing using a 2d array of chars instead of a 1d list of strings in case I need to edit map data mid-game
		if x=="@":
			# Set spawnpoint
			mapLine.append(" ")
			pos=[xi, yi]
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

def isWall(dx=0, dy=0, block="#"):
	return mapData[pos[1]+dy][pos[0]+dx]==block
def cursorPos(x, y):
	return "\033["+str(y+1)+";"+str(x+1)+"H"

fallTimer=time.time() # You only fall every 0.5 seconds (Well it's every 0.6 because the vFPS is 0.2 but whatever)
buttons="."
while True:
	# Print screen
	if buttons!="": # If there's no player input, don't reprint the map
		for yi, y in enumerate(mapData):
			for xi, x in enumerate(mapData[yi]):
				print(cursorPos(xi, yi)+(blockPre[x] if x in blockPre.keys() else "")+x+blockPost)
	# Calculate death/win conditions
	if pos[1]==len(mapData)-1 or isWall(0, 0, "X"):
		print("\033[2J\033[1;1HDead\nPress any key to continue")
		msvcrt.getch()
		exit()
	elif isWall(0, 0, "O"):
		print("\033[2J\033[1;1HWin\nPress any key to continue")
		msvcrt.getch()
		exit()
	# Erase player
	# If there's no player movement but you're falling, this prevents a trail from happening
	print(cursorPos(pos[0], pos[1])+mapData[pos[1]][pos[0]])
	# Compute next position
	hphase=1+int("C" in buttons)
	if "R" in buttons and pos[0]+hphase<mapWidth and not isWall(hphase, 0)   : pos[0]+=hphase
	if "L" in buttons and pos[0]-hphase>=0 and not isWall(-hphase, 0)        : pos[0]-=hphase
	if "U" in buttons and pos[1]-3>=0 and isWall(0, 1) and not isWall(0, -3): pos[1]-=3
	if "S" in buttons and pos[1]-5>=0 and isWall(0, 1) and not isWall(0, -5): pos[1]-=5
	if mapData[pos[1]+1][pos[0]]=="#":fallTimer=time.time()
	if not ("D" in buttons) and not isWall(0, 1) and time.time()-fallTimer>0.5   : pos[1]+=1; fallTimer=time.time()
	print(cursorPos(pos[0], pos[1])+blockPre["@"]+"@"+blockPost) # Print player
	buttons=""
	for i in range(12):
		# Checks for buttons every 60th of a second but only does physics every 5th of a second
		# It is a very stupid solution but it works
		buttons+=getButtons()
		time.sleep(1/60)
