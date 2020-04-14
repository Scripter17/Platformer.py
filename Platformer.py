import colorama, os, keyboard, time, ctypes
colorama.init()

class _CursorInfo(ctypes.Structure):
	_fields_ = [("size", ctypes.c_int),
	("visible", ctypes.c_byte)]
ci = _CursorInfo()
handle = ctypes.windll.kernel32.GetStdHandle(-11)
ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
ci.visible = False
ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))

cols, lines=50, 31
os.system("mode con: cols="+str(cols)+" lines="+str(lines))
px, py=0, 0

mapText=open("map.txt", "r").read()
mapData=[]
for yi,y in enumerate(mapText.splitlines()):
	mapLine=[]
	for xi,x in enumerate(y):
		if x=="@":
			mapLine.append(" ")
			py, px=yi, xi
		else:
			mapLine.append(x)
	mapData.append(mapLine)
#print(len(mapData)); exit()

def getButtons():
	buttons=""
	if keyboard.is_pressed("up")   : buttons+="U"
	if keyboard.is_pressed("right"): buttons+="R"
	if keyboard.is_pressed("down") : buttons+="D"
	if keyboard.is_pressed("left") : buttons+="L"
	if keyboard.is_pressed("space"): buttons+="S"
	return buttons

fallTimer=time.time()
buttons="."
firstFrame=True
while True:
	# Handle buttons
	# Print screen
	if buttons!="":
		for yi, y in enumerate(mapData):
			for xi, x in enumerate(mapData[yi]):
				print("\033["+str(yi+1)+";"+str(xi+1)+"H"+x)
		firstFrame=False
	# Calculate death/win conditions 
	if py==len(mapData)-1 or mapData[py][px]=="X":
		os.system("cls")
		print("Dead")
		os.system("pause")
		exit()
	elif mapData[py][px]=="O":
		os.system("cls")
		print("Win")
		os.system("pause")
		exit()
	# Erase player
	print("\033["+str(py+1)+";"+str(px+1)+"H"+mapData[py][px])
	# Compute next position
	if "R" in buttons and px+1<len(mapData[py]) and mapData[py][px+1]!="#": px+=1
	if "L" in buttons and px-1>=0 and mapData[py][px-1]!="#": px-=1
	if "U" in buttons and py-3>=0 and mapData[py+1][px]=="#" and mapData[py-3][px]!="#": py-=3
	if "S" in buttons and py-5>=0 and mapData[py+1][px]=="#" and mapData[py-5][px]!="#": py-=5
	if not ("D" in buttons) and mapData[py+1][px]!="#" and time.time()-fallTimer>0.5:
		py+=1
		fallTimer=time.time()
	# Print player
	print("\033["+str(py+1)+";"+str(px+1)+"H"+"@")
	buttons=""
	for i in range(12):
		buttons+=getButtons()
		time.sleep(1/60)