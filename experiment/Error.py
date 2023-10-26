
class EyetrackerNotFoundException(Exception):
    def __str__(self):
        return 'No eyetracker connected'

class EgiNotFoundException(Exception):
    def __str__(self):
        return 'No egi device connected'


