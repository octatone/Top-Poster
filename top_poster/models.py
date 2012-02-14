class Last(object):
    def __init__(self):
        self.file = './data/last.txt'
        
    def getContents(self):
        """Returns data flat file contents"""
        target = open(self.file)
        self.contents = target.read()
        target.close()

    def isStored(self, data):
        """Checks is current submission is stored"""
        self.getContents()
        if self.contents.find(data.title) == -1 and self.contents.find(data.url) == -1:
            return False
        else:
            return True

    def store(self, data):
        """Store data"""
        string = ''
        for item in data:
            if item.title and item.url:
                string += item.title + ' ' + item.url

        write_file = open(self.file,'w')
        write_file.truncate()
        write_file.write(string)
        write_file.close()

        return True


