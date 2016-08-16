DEFAULT_DEVICE = '/dev/usb/lp0'

class MachinePrinter:
    def __init__(self, path=DEFAULT_DEVICE):
        self.path = path
        self.stream = open(path, 'wb')

    def print(self, text):
        encoded = text.replace('\n', '\n\r').encode('cp437', 'replace')
        self.stream.write(encoded)
        self.stream.write(b'\n\r\n\r')
        self.stream.flush()

