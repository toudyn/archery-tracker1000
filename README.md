# archery-tracker1000

This repository is currently two separate QT applications: One for scoring sessions and the second for visualizing sessions.

scorer.py is run to score sessions. Left click on the target to place a shot, save it with 'f', then continue adding other shots for an end. The previous shot can be deleted with 'd'. To start scoring the next end, press 'r'.
Once complete, press 's' to save the shots to 'output.csv'. Note that the output from this csv should be copied elsewhere, there is not currently any functionality for reading from another file and appending to it.
The output file contains the x and y locations of all shots, for a 60cm target.

visualizer.py can be run to read from a csv file and then plot all shots of sessions. The filename of the file that should be read needs to be edited in visualizer.py.