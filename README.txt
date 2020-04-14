   Platformer.py v1.0.0
James C. Wise - 2020-04-14 
 See LICENSE.md for legal

Requirements:
	- Python 3
	- Windows (probably)
	- Tolerance for unpolished games

Controls:
	Right: Move right
	Left:  Move left
	Down:  Stop falling
	Up:    Phase up 3 blocks
	Space: Phase up 5 blocks

Phasing:
	Unlike in most platformers which have jumps that are stopped by ceilings, this game has phasing
	Phasing is like jumping, but you can go through blocks
	If there's a block 4 blocks above you when you hit space, instead of being blocked by the ceiling and only going up 3 blocks, you'll still go up 5 blocks; Effectively phasing through the block

Making maps:
	`map.txt` is the map file; In it, there are 5 "tile" types:
	Air   ( ): No special effect
	Block (#): Blocks movement/falling and phasing; You can only phase while standing on a block
	Death (X): When touched, the player dies
	Win   (O): When touched, the player wins
	Spawn (@): Defines where the player spawns from

TODO/Known Bugs:
	- Shift+Right / Shift+Left allowing you to phase through walls
	- Map select screen
	- Attempting to enter a tile that isn't in map.txt-even if it's within the bounding box for the map-crashes the game
	- Better documentation
	- Compile game into an exe

Changelog:
v1.0.0 - Initial:
	- Created the game