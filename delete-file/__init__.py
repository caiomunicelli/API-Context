import azure.functions as func
from ..function_app import delete_file

async def main(req: func.HttpRequest) -> func.HttpResponse:
    return await delete_file(req)
