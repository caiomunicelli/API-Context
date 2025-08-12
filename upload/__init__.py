import azure.functions as func
from ..function_app import main

async def main(req: func.HttpRequest) -> func.HttpResponse:
    return await main(req)
