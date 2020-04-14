   Platformer.py v1.0.0
James C. Wise - 2020-04-14 
 See LICENSE.md for legal

Requirements:
	- Python 3
	- Windows (probably)
	- Tolerance for unpolished games

Controls:
	Right : Move right
	Left  : Move left
	Down  : Stop falling
	Up    : Phase up 3 blocks
	Space : Phase up 5 blocks
	CTRL+Right : Phase 2 blocks right
	CTRL+Left  : Phase 2 blocks left

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

TODO/Known Bugs:
	- Map select screen
	- Better code documentation
	- Compile game into an exe
	- Colors?
	- Check if it works on Linux (Or at least Ubuntu)

Changelog:
v1.0.0 - Initial:
	- Created the game
v1.1.0 - Sideways phasing:
	- Control+Right and Control+Left allows you to phase 2 blocks to the right and left
	- Fixed entering an undefined tile within the map's bounding box crashing the game
	  The default map.txt reflects this on line 8
	- The game window now automatically resizes into the map's dimensions
	  Whether or not this change will stay is to be determined