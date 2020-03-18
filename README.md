# File-Forensic-Analysis

Analyze all non-deleted files in a directory and send the output file to your email directly using this tool. 
This tool applies the following checks:
 - Identify any big files (by default files larger than 10mb, this limit can be changed in the code)
 
 - Match file contents against set a of keywords which are placed in the keywords1.txt
 (eg. "confidential", "password", by default only first 1mb of file is checked)
 
 - Check if file signature doesn't match file extension (yet to be added)
 
 ## Usage
 
- Create file called "keywords1" with one keyword per line (case sensitive) -- these keywords will be matched against 
  every file in the directory (by default only first 1mb of file is checked)
  
- Output file called "output" will be generated containing the analysis output

### Run

```
 Navids-MacBook-Pro:File_Forensics navidkagalwalla$ python file_forensic_analysis.py
```
### Output
```
---HERE ARE YOUR BIG FILES---!
    68 MB   video/quicktime      /full/path/video.mov
!---KEYWORDS FOUND---!

2     text/plain           (/Users/navidkagalwalla/Desktop/Dummy/tt.txt)
	- s together, and get access to more features. My password is pass and username is user. Kidding that a pass       
 	- and get access to more features. My password is pass and username is user. Kidding that aint it.' pass

```

### Automatically Send Email
Input details in the following places

```
send_from = 'senders address'
send_to = 'receivers address'
username='senders address'
password='password'

```

### Output

![Alt text](https://user-images.githubusercontent.com/46184137/76927728-cdfec400-6905-11ea-819e-a354642ea832.png?raw=true "Email")

_WARNING_ : Google may not allow you to log in via smtplib because it has flagged this sort of login as "less secure", 
so what you have to do is go to this [link](https://www.google.com/settings/security/lesssecureapps) while you're logged in to your google account, and allow the access.


