#!/usr/bin/python3 
import os
from dotenv import load_dotenv
from modules import (
    webserver
)
load_dotenv()

if __name__ == "__main__":
    server = webserver.server()
    server.start()