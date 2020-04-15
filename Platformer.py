#    Platformer.py v1.0.0
# James C. Wise - 2020-04-14 
#  See LICENSE.md for legal

import colorama, os, subprocess as sp, keyboard, time, ctypes, msvcrt
colorama.init()

# Some ctypes bullshit to make the terminal cursor not appear
try:
	class _CursorInfo(ctypes.Structure):
		_fields_ = [("size", ctypes.c_int),
		("visible", ctypes.c_byte)]
	ci = _CursorInfo()
	handle = ctypes.windll.kernel32.GetStdHandle(-11)
	ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
	ci.visible = False
	ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
except:
	pass
# Good lord that was gross

px, py=0, 0
prefixes={
	" ":"",
	"#":"",
	"X":"\033[31m",
	"O":"\033[32m",
	"@":"\033[33m"
}
suffix="\033[39m"

# Get map data
maps=[x for x in os.listdir() if x.endswith(".map") and os.path.isfile(x)]
mapIndex=0
if len(maps)==0:
	print("No maps detected!")
	print("Press any key to exit")
	msvcrt.getch()
	exit()
else:
	while True:
		"""key=msvcrt.getch()
		if key==b"\r":
			break
		if key==b"\xe0":
			key=msvcrt.getch()
		if key==b"H" : mapIndex=(mapIndex+1)%len(maps)
		if key==b"P"   : mapIndex=(mapIndex-1+len(maps))%len(maps)"""
		print(">>> "+maps[mapIndex])
		if msvcrt.getch()==b"\xe0": msvcrt.getch()
		if keyboard.is_pressed("escape"): exit()
		if keyboard.is_pressed("enter"): break
		if keyboard.is_pressed("up")   : mapIndex=(mapIndex+1)%len(maps)
		if keyboard.is_pressed("down") : mapIndex=(mapIndex-1+len(maps))%len(maps)
		print("\033[1A\033[2K",end="")
sp.run("cls", shell=True)
sp.run(["title", maps[mapIndex]], shell=True)
mapText=open(maps[mapIndex], "r").read()
# Not too sure why I'm doing it like `[["Block"]]` instead of `["Blocks"]` but it doesn't matter too much to me
mapData=[]
for yi, y in enumerate(mapText.splitlines()):
	mapLine=[]
	for xi, x in enumerate(y):
		if x=="@": # Set spawnpoint
			mapLine.append(" ")
			py, px=yi, xi
		else:
			mapLine.append(x)
	mapData.append(mapLine)
empty=False
try:
	width=max(*[len(x) for x in mapData])
except:
	width=0
if width==0:
	print("The map selected is empty; Try another map")
	msvcrt.getch()
	exit()
# Pad lines that don't extend to the bounding box
for yi,y in enumerate(mapData):
	mapData[yi]+=[" "]*(width-len(y))
#os.system("mode con: cols="+str(width)+" lines="+str(len(mapData)+1)) # Set screen size to map size

def getButtons():
	buttons=""
	if keyboard.is_pressed("up")     : buttons+="U" # Phase up 3 blocks
	if keyboard.is_pressed("right")  : buttons+="R" # Move right
	if keyboard.is_pressed("down")   : buttons+="D" # Stop falling
	if keyboard.is_pressed("left")   : buttons+="L" # Move right
	if keyboard.is_pressed("space")  : buttons+="S" # Phase up 5 blocks
	if keyboard.is_pressed("control"): buttons+="+" # CTRL+Right / CTRL+Left phase sidewats 2 blocks
	return buttons

fallTimer=time.time() # You only fall every 0.5 seconds (Well it's every 0.6 because the vFPS is 0.2 but whatever)
buttons="."
while True:
	# Handle buttons
	# Print screen
	if buttons!="": # If there's no player input, don't reprint the map
		for yi, y in enumerate(mapData):
			for xi, x in enumerate(mapData[yi]):
				print("\033["+str(yi+1)+";"+str(xi+1)+"H"+(prefixes[x] if x in prefixes.keys() else "")+x+suffix)
	# Calculate death/win conditions 
	if py==len(mapData)-1 or mapData[py][px]=="X":
		print("\033[2J\033[1;1HDead")
		print("Press any key to continue")
		msvcrt.getch()
		exit()
	elif mapData[py][px]=="O":
		print("\033[2J\033[1;1HWin")
		print("Press any key to continue")
		msvcrt.getch()
		exit()
	# Erase player
	# If there's no player movement but you're falling, this prevents a trail from happening
	print("\033["+str(py+1)+";"+str(px+1)+"H"+mapData[py][px])
	# Compute next position
	hphase=1+int("+" in buttons)
	if "R" in buttons and px+hphase<len(mapData[py]) and mapData[py][px+hphase]!="#"   : px+=hphase
	if "L" in buttons and px-hphase>=0 and mapData[py][px-hphase]!="#"                 : px-=hphase
	if "U" in buttons and py-3>=0 and mapData[py+1][px]=="#" and mapData[py-3][px]!="#": py-=3
	if "S" in buttons and py-5>=0 and mapData[py+1][px]=="#" and mapData[py-5][px]!="#": py-=5
	if mapData[py+1][px]=="#":fallTimer=time.time()
	if not ("D" in buttons) and mapData[py+1][px]!="#" and time.time()-fallTimer>0.5   : py+=1; fallTimer=time.time()
	print("\033["+str(py+1)+";"+str(px+1)+"H"+prefixes["@"]+"@"+suffix) # Print player
	buttons=""
	for i in range(12):
		# Checks for buttons every 60th of a second but only does physics every 5th of a second
		# It is a very stupid solution but it works
		buttons+=getButtons()
		time.sleep(1/60)
