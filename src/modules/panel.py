from pydactyl.api.servers import Servers
from config import PANEL_URL, PANEL_API


class PanelServer(Servers):
    def __init__(self, session=None):
        super().__init__(PANEL_URL, PANEL_API, session)
    
    def get_all_servers(self):
        data = self.list_servers()
        print(data)
    