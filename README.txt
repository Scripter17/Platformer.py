   Platformer.py v1.4.0
James C. Wise - 2020-04-17
 See LICENSE.md for legal

Requirements:
	- Python 3
	- Windows
	- Tolerance for unpolished games

Controls (2 player mode is in beta and probably very buggy):
	Player | 3 up | Move right | Stop Falling | Move left | HPhase   | 5 up     
	-------+------+------------+--------------+-----------+----------+----------
	1 of 1 | Up   | Right      | Down         | left      | CTRL     | Space    
	1 of 2 | Up   | Right      | Down         | left      | ALT/CTRL | Backslash
	2 of 2 | R    | G          | F            | D         | A        | S        

Phasing:
	Unlike in most platformers which have jumps that are stopped by ceilings, this game has phasing
	Phasing is like jumping, but you can go through blocks
	If there's a block 4 blocks above you when you hit space, instead of being blocked by the ceiling and only going up 3 blocks, you'll still go up 5 blocks; Effectively phasing through the block

Making maps:
	`map.txt` is the map file; In it, there are 5 tile types:
	Air   ( ): No special effect
	Block (#): Blocks movement/falling and phasing; You can only vertically phase while standing on a block
	Death (X): When touched, the player dies
	Win   (O): When touched, the player wins
	Spawn (@): Defines where the player spawns from

TODO:
	- Better in-code documentation
	- Compile game into an exe
	- Cut down the number of modules I'm using
	- CLEAN THE F@!#ING CODE
Known Bugs:

Changelog:
v1.0.0 - Initial:
	- Created the game
v1.1.0 - Sideways phasing:
	- Control+Right and Control+Left allows you to phase 2 blocks to the right and left
	- Fixed entering an undefined tile within the map's bounding box crashing the game
	  The default map.txt reflects this on line 8
	- The game window now automatically resizes into the map's dimensions
	  Whether or not this change will stay is to be determined
v1.1.1 - Should be possible to get working on linux
	- The keyboard module breaks things on the Linux subsystem for my Windows 10 machine, but it might work on yours
	- Also removed the console resizing thing because gross
v1.3.0 - Some colorful colors and colorful language to Linux
	- Officially not supporting Linux for the time being due to just generally being a pain
	- The player, death zones, and win zones are color coded to be orange, red, and green
	- Created a map selection screen
v1.4.0 - Platforming with friends!
	- Added a beta 2 player mode. Two players cannot occupy the same block,
	  so it can create an interesting 2 player dynamic where players use eachother as platforms
