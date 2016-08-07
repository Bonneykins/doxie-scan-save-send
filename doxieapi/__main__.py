import os

from .api import DoxieScanner
from .smtp import send_mail


def main():
    """
    Grab all available scan images and save them to the current working directory
    """
    scanners = DoxieScanner.discover()
    for scanner in scanners:
        print("Discovered {}.".format(scanner))
        for scan in scanner.download_scans_renamed(os.getcwd()):
            print("Saved {}".format(scan))
            send_mail(  send_from='1494hardware@gmail.com',
                        send_to='sam@1494.co.nz',
                        subject='Test Subject',
                        text='Scan from a Wild Doxie',
                        files=[scan],
                        server="smtp.gmail.com",
                        port=587,
                        username='1494hardware@gmail.com',
                        password='hardware1',
                        isTls=True)
            print("Sent {}".format(scan))
        scanner.delete_scans([scan['name'] for scan in scanner.scans])
        print("Deleted scans")

if __name__ == '__main__':
    main()
