3/21/2022 v1.0

To implement this:

  Find the usb's serial number, hash it with SHA256, and store its hex value as the hash variable on line 8
  
  Add print statement or debug to see the master password value generated based on the usb's serial number
  
  Create a new password vault using the master password generated from the usb's serial number
  
  Update paths to point to pythonw.exe and location of the new password vault
  
  Run runner.vbs
  
  Optionally, create a shortcut to the runner.vbs script and move it to the Window's startup folder
