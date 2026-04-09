from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient
from config import settings

async def get_graph_client():
    """Create authenticated Microsoft Graph client"""
    credentials = ClientSecretCredential(
        tenant_id=settings.TENANT_ID,
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET
    )
    
    scopes = ['https://graph.microsoft.com/.default']
    graph_client = GraphServiceClient(credentials=credentials, scopes=scopes)
    return graph_client