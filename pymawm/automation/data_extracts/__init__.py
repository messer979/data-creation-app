from .extract_inventory import run_extract

class Extract:
    def __init__(self, active):
        self.active = active

    def extract_inventory(self):
        run_extract()
