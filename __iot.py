from pirc522 import RFID

class Render:
    def __init__(self, rdr) -> None:
        self.rdr = rdr
        self.preuid = ''
        self.state = 'untached'
        self.count = 0
    
    def recognit(self):
        (error, _) = self.rdr.request()
        user_id = ''
        if not error:
            (error, uid) = self.rdr.anticoll()
            if not error:
                user_id = str(uid)
                if self.preuid != user_id:
                    self.preuid = user_id
                    self.state = 'touched'
                    return user_id
        
        else :
            self.count+=1
            self.state = 'untouched'
            if self.count > 5:
                self.rdr.wait_for_tag()
            return user_id

        return user_id

    def suspend(self):
        self.rdr.wait_for_tag()