#!/usr/bin/env python

import os
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

class FileForensics:

    def __init__(self):
        self.filelist = list()

    def scan_dir(self, dir):
        import pathlib
        import magic

        for filename in find_all_files(dir):
            self.filelist.append({
                    "filename": filename,
                    "mime": magic.from_file(filename, mime=True),
                    "size_bytes": os.path.getsize(filename),
                    "ext": pathlib.Path(filename).suffix
                    })

    def get_lenght(self):
        return len(self.filelist)

    def get_big_files(self, size_threshold=2):
        """Return list of file bigger than X MB (size in MB)."""
        for f in self.filelist:
            if f["size_bytes"] > size_threshold*(1024*1024):
                yield f["size_bytes"]/(1024*1024), f["mime"], f["filename"]

    def get_keyword_files(
            self,
            filename_keywords="keywords1.txt",
            read_size=1024*1024,
            offset=50):
        import ahocorasick

        A = ahocorasick.Automaton()
        with open(filename_keywords, encoding="utf8", errors='ignore') as f:
            while True:
                word = f.readline()
                if not word:
                    break
                A.add_word(word.strip(), word.strip())

        A.make_automaton()

        for file in self.filelist:
            with open(file["filename"], "rb") as f:
                matches = list()
                buff1= f.read(read_size)
                buff=str(buff1)
                for match in A.iter(buff):
                    pos_cur = match[0]
                    pos_start = max(match[0]-offset, 0)
                    pos_end = min(match[0]+offset, read_size)
                    offset_start = buff[
                            pos_start:pos_cur-len(match[1])+1
                        ].find("\n")
                    offset_end = buff[pos_cur+1:pos_end].rfind("\n")

                    if offset_start >= offset:
                        offset_start = 0
                    if offset_end <= 0:
                        offset_end = offset
                    offset_end = offset - offset_end

                    matched_text = buff[
                            pos_start+offset_start:pos_cur-len(match[1])+1
                        ] + \
                        buff[pos_cur-len(match[1])+1:pos_cur+1] + \
                        buff[pos_cur+1:pos_end-offset_end]

                    matches.append((matched_text.replace("\n", " "), match[1]))
                if len(matches) > 0:
                    yield (file, matches)

def find_all_files(path):
    for root, dirs, files in os.walk(os.path.join(path)):
        for filename in files:
            yield os.path.join(root, filename)

def send_mail(send_from,send_to,subject,text,server,port,username,password,isTls=True):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("output.txt", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="output.txt"')
    msg.attach(part)

    #context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
    #SSL connection only working on Python 3+
    smtp = smtplib.SMTP(server, port)
    if isTls:
        smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


def main():
    ff = FileForensics()
    ff.scan_dir("/directory/to/be/scanned")
    out=open("output.txt","w+")

    print ("\n!---HERE ARE YOUR BIG FILES---!")
    out.write("\n ---HERE ARE YOUR BIG FILES---!")
    for (size, mime, filename) in ff.get_big_files():
        print ("{:>10} MB"+"   {:<20} {:<10}".\
            format(size, mime, filename))
        out.write("{:>10} MB"+"   {:<20} {:<10}".\
            format(size, mime, filename))

    print ("\n!---KEYWORDS FOUND---!")
    out.write("\n!---KEYWORDS FOUND---!")
    for (file, matches) in ff.get_keyword_files():
        print ("{:<5} {:<20} ({:<10})".format(
            len(matches), file["mime"], file["filename"]))
        out.write("{:<5} {:<20} ({:<10})".format(
            len(matches), file["mime"], file["filename"]))
        out.write("\n")

        for position, match in matches:
            print ("\t- {:<10} {:<10}".format(position, match))
            out.write("\t- {:<10} {:<10}".format(position, match))
            out.write(" \n ")
        print
    out.close()
    text = '''Hello,
    This mail contains information from File Forensics.
    '''
    send_from = 'senders address'
    send_to = 'receivers address'
    subject='File Forensics'
    server='smtp.gmail.com'
    port=587
    username='senders address'
    password='password'
    send_mail(send_from,send_to,subject,text,server,port,username,password,isTls=True)
    print('Mail Sent')

if __name__ == "__main__":
    main()
