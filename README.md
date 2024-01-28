# FolderComparator
This is a python application that compares 2 folders

## First Type: Command line script
The compareFolders.py is a commmand Line script.
Open Terminal and run the file.
Input 2 valid Folder Paths.
The script will output the different files/folders in both folders.
![Folder Comparator](https://github.com/Netrifier/FolderComparator/assets/92852012/10046ead-5254-43ab-86c4-bd2e47bb9ddf)


## Second Type: GUI application
This also compares 2 folders with a GUI.
The "Folder Comparator.py" is the GUI application.
To download the compiled .exe go to the releases page and download the latest version.
The application takes 2 folder paths and gives an option to browse for the folder or manually enter the path.
The Compare button compares the 2 folders and outputs a list in the below area.
There is a checkbox next to every file item. Selecting This checkbox and clicking the Copy selected Files will copy those files to the Second Folder from the first folder.
There is a copy button for each file item which when clicked will copy that individual file.
![Folder Comparator GUI](https://github.com/Netrifier/FolderComparator/assets/92852012/4ad37c4e-e46d-430d-96b8-a4d6f0307614)

### Disclaimer
The GUI application will only copy the items from the first folder to the second folder not vice-versa. i.e. not from the second folder to the first folder.
This is done because the application was built considering that the second folder is the backup folder of the first folder. And if there are any different files in the second folder that means you either deleted them from the first folder or renamed the item. You need to manually review these files and decide what to do with them. This maybe changed in the future to allow copying from the second folder to the first folder.
If there is a new Folder in the first folder then the whole folder will be shown as a new item and you can copy the entire folder. It will not display the individual files of that new folder.
