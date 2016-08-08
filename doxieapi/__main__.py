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
        try:
            """ Attempt to download scans, one at a time.
                This try-except necessary because when Doxie deletes scans
                it deletes the file but does not delete the most recent record.
                An attempte to download a named, but missing recent file would
                result in error.
            """
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
        except:
            print("Found no new scans")

while __name__ == '__main__':
    print('Initializing')
    main()
    print('Sleeping')
    sleep(5.0)
