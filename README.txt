Deadusers

Prints a table of all IAM users for which one of the following conditions hold:
- has never logged in on console
- logged in to console longer than 30 days ago
- has access key(s) that have never been used
- has access key(s) that were used longer than 30 days ago


Dependencies

Tested with python 3.9 on MacOs; I expect python version 3.6 and later will work.

Install dependencies using:

python3 -m pip -r requirements.txt


Running

python3 deadusers.py


Example output:

+-----------------------------------+--------------------------------------------------------------------------------------+
| User                              | Reason(s)                                                                            |
+===================================+======================================================================================+
| a.testuser@example.com            | Last console login: 2021-10-06 07:10:44+00:00 (198 days ago)                         |
|                                   | Access key AKIAWLXEP6PD46JQQMP7 never used                                           |
+-----------------------------------+--------------------------------------------------------------------------------------+
| another.user@example.com          | Access key AKIAWLPPXE6DQH44Y5VR never used                                           |
+-----------------------------------+--------------------------------------------------------------------------------------+
