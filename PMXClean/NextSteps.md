change pings to ping the available network range from the interface and its subnet mask
 - [ ] Get the IP address and subnet mask of the interface
	- [ ] ping along the network range of the interface and subnet mask
	- [ ] on successful ping, send specific commands to the responding host to determine if it is the device we expect to find
	- [ ] when it's the galil, check the firmware version

Add the ability to load backups from the installed locations in a list format as well
 - [ ] Create a list of installed locations where backups are stored
 - [ ] Load the backups from these locations and display them in a list format for the user to select from

Move MainWindow into Views folder to better fit MVVM

Determine if \Resources folder is needed

Rework the Deploy script for single file deployment

Add ability to diff between two backups, instead of just a backup and our versions list

ultimate goal: create a tool that compares the installed version or the backup with our version that is AHEAD of the installed version, 
and provides the user with a list of changes needed for their #locked files so they know what to do in order to progress
