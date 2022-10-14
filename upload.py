from ftplib import FTP_TLS
class Upload():
    def files(self, host, username, password, directory, path, filename,
                 permission=True):
        s = FTP_TLS(host)
        s.login(username, password)
        s.prot_p()
        s.cwd(directory)
        if (permission):
            s.sendcmd('chmod 0664 ' + filename)
        s.getwelcome()
        f = open(path, 'rb')
        s.storlines('STOR ' + filename, f)
        f.close()
        s.quit()
    def picture(self, host, username, password, directory, path, filename,
                 permission=True):
        s = FTP_TLS(host)
        s.login(username, password)
        s.prot_p()
        s.cwd(directory)
        if (permission):
            s.sendcmd('chmod 0664 ' + filename)
        s.getwelcome()
        f = open(path, 'rb')
        s.storbinary('STOR ' + filename, f)
        f.close()
        s.quit()
    def audio(self, host, username, password, directory, path, filename,
                 permission=True):
        s = FTP_TLS(host)
        s.login(username, password)
        s.prot_p()
        s.cwd(directory)
        if (permission):
            s.sendcmd('chmod 0664 ' + filename)
        s.getwelcome()
        f = open(path, 'rb')
        f.storbinary('STOR ' + filename, f)
        f.close()
        s.quit()
    def video(self, host, username, password, directory, path, filename,
                 permission=True):
        s = FTP_TLS(host)
        s.login(username, password)
        s.prot_p()
        s.cwd(directory)
        if (permission):
            s.sendcmd('chmod 0664 ' + filename)
        s.getwelcome()
        f = open(path, 'rb')
        s.storbinary('STOR ' + filename, f)
        f.close()
        s.quit()
class Download():
    def files(self, host, username, password, directory, filename, store,
              permission=True):
        s = FTP_TLS(host)
        s.login(username, password)
        s.prot_p()
        s.cwd(directory)
        if (permission):
            s.sendcmd('chmod 0664 ' + filename)
        s.getwelcome()
        #def callback(data):
        d = open(store, 'w+')
        #    for line in data:
        #        d.write(line)
        #    d.close()
        s.retrlines('RETR ' + filename, d.write)
        d.close()
        s.quit()
class Delete():
    def __init__(self, host, username, password, directory, filename):
        s = FTP_TLS(host)
        s.login(username, password)
        s.prot_p()
        s.cwd(directory)
        s.sendcmd('chmod 0664 ' + filename)
        s.getwelcome()
        s.delete(filename)
        s.quit()
