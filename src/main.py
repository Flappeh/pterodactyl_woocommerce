from src.modules.worker import PanelWorker
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from src.schema import UpdateOrder

app = FastAPI()



@app.post("/order/update")
async def new_subscription(req: UpdateOrder):
# async def new_subscription(req: Request):
    """
    When a new user subscribes to your service we'll send you a POST request with this
    data to the URL that you register for the event `new-subscription` in the dashboard.
    """
    # res = await req.json()
    # print(res)
    request = req.model_dump()
    print(request)
    worker = PanelWorker()
    worker.check_user_exists(request["billing"]["email"])
    return PlainTextResponse("Done", 200)


@app.get("/users/")
def read_users():
    return ["Rick", "Morty"]



# if __name__ ==  "__main__":
#     conn_panel = PanelServer()
#     conn_panel.get_all_servers()
    