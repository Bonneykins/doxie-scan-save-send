import os

from .api import DoxieScanner
from .smtp import send_mail
from time import sleep



def main():
    """
    Grab all available scan images and save them to the current working directory
    """
    scanners = DoxieScanner.discover()
    for scanner in scanners:
        print("Discovered {}.".format(scanner))
        for scan in scanner.download_scans_renamed(os.getcwd()):
            print("Saved {}".format(scan))
            head, tail = os.path.split(scan)
            send_mail(  send_from= '1494hardware@gmail.com',
                        send_to= 'sam@1494.co.nz',
                        subject= tail + ' from ' + format(scanner),
                        text= tail + ' from ' + format(scanner),
                        files= [scan],
                        server= "smtp.gmail.com",
                        port= 587,
                        username= '1494hardware@gmail.com',
                        password= 'hardware1',
                        isTls= True)
            print("Sent {}".format(scan))
            os.remove(scan)
            print("Deleted {} from local".format(scan))
        scanner.delete_scans([scan['name'] for scan in scanner.scans])
        print("Deleted scans from Doxie")

while __name__ == '__main__':
    print('Initializing')
    main()
    print('Sleeping')
    sleep(5.0)
