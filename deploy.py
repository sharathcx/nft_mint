from brownie import FundMe, SimpleCollectible
from scripts.helper import get_account
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

address = get_account()
FundMe.deploy({"from":address})

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow access from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/pay")
def payment(url:str,name:str, description:str, result:str, confidense:int):
    uri = {
    "name": f"{name}",
    "description": f"{description}",
    "image": f"{url}",
    "attributes": [
            {
                "Result": f"{result}",
                "value": str(confidense)
            }
        ]
    }
    json_uri = json.dumps(uri)

    fund_me = FundMe[-1]
    tx = fund_me.fund({"from": address, "value": 1703270342374390})
    simple_collectable = SimpleCollectible.deploy({"from":address})
    tx = simple_collectable.createCollectible(json_uri, {"from":address})
    tx.wait(1)
    print(f"You can view your nft at {OPENSEA_URL.format(simple_collectable.address, simple_collectable.tokenCounter() -1)}")
    tx = fund_me.withdraw({"from": address})
    print("Payment Transfered")



def main():
    uvicorn.run(app, port=9000, host="0.0.0.0")

