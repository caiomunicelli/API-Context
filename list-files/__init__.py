import azure.functions as func
from ..function_app import list_files

async def main(req: func.HttpRequest) -> func.HttpResponse:
    return await list_files(req)
