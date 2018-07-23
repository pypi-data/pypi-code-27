import vimeo_api
import preference_manager

class PrefEPy:
    def __init__(self, address = None):
        #For use with flask if needed later
        self.address = address
    def update_response(self):
        pass

    def get_videos(self):
        return preference_manager.test_videos()