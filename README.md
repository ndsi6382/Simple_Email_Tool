# Simple Email Tool
This is a simple command line program to create and send emails, and supports 
adding bodies read from a text file, or writing formatted bodies from files 
given in HTML or Markdown.

## Setup and Configuration
There is only one dependency outside of the Python Standard Library: 
`markdown2`, which can be installed with: `pip install markdown2`.  
After navigating to the directory of the program, run 
`sudo chmod +x ./simple_email_tool.py` to allow the file's execution.  

`config.py` contains parameters used by the program for the sender's email 
login details and SMTP server address. For security reasons, these are allowed 
to be left blank, but will be prompted for at the beginning of the program's 
execution. The password can alternatively be stored in an environment 
variable called `EMAILPASS`, otherwise it will also be asked for.  

*The use of this program is not recommended outside of personal contexts.*

## Usage
Usage is as follows: 
`simple_email_tool.py [-h] [-to ADDRESS [ADDRESS ...]] [-cc ADDRESS [ADDRESS ...]] [-bcc ADDRESS [ADDRESS ...]] [-s SUBJECT] [-b BODY | -bt FILE | -bm FILE] [-a FILE [FILE ...]] [-y]`
- `-h, --help` Show the help message and exit
- `-to ADDRESS [ADDRESS ...]` Recipient addresses
- `-cc ADDRESS [ADDRESS ...]` Cc addresses
- `-bcc ADDRESS [ADDRESS ...]` Bcc addresses
- `-s SUBJECT, --subject SUBJECT` Subject text
- `-b BODY, --body BODY` Body (as plaintext - suitable for quick/short messages)
- `-bt FILE, --bodytextfile FILE` Write email body from a text file
- `-bm FILE, --bodymarkdown FILE` Write email body from a markdown file
- `-a FILE [FILE ...], --attachments FILE [FILE ...]` Attachment filenames/paths
- `-y, --yes` Skip the confirmation prompt before sending

Multiple addresses/paths/filenames should be separated by a space.  
Any text containing spaces that is passed in at the command line must be enclosed by 
quotation marks.  
If no arguments are given, then the user will be prompted for each field.  
The body of an email created by prompt can contain no new lines.
