from modules.wcom import WooConn
from modules.panel import PanelServer




if __name__ ==  "__main__":
    conn_panel = PanelServer()
    conn_panel.get_all_servers()
    