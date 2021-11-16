ReadMe


Neural Network I/O
	
	INPUT

		: X position of the puck
		: Y position of the puck
		: X position of the bar

	OUTPUT

		: Bar moves left
		: Bar moves right


Fitness Scoring Method

	ADDING FITNESS

	: While the puck is still in play
		Add a fitness of 1.2 (per second) while the puck is still alive

	: When the bar hits the puck
		Reward generously; Add a fitness of 4

	SUBTRACTING FITNESS

	: bar trying to leave the x-axis bounds of the window
		Subtract 1.2 (per second) to discourage the habit of leaning to the right/left all the time
		Note: the bars do not leave the game window as they have been hard-coded to touch the walls if they do.  