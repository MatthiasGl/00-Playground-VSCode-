import io
from typing import List, Dict, Any
from msgraph import GraphServiceClient
from auth import get_graph_client
from config import ALLOWED_PATHS

class OneDriveClient:
    def __init__(self):
        self.client: GraphServiceClient = None
    
    async def _ensure_client(self):
        if self.client is None:
            self.client = await get_graph_client()
    
    def _is_path_allowed(self, path: str) -> bool:
        """Check if a path is allowed based on ALLOWED_PATHS"""
        if not path.startswith('/'):
            path = '/' + path
        
        for allowed in ALLOWED_PATHS:
            if path.startswith(allowed):
                return True
        return False
    
    async def _get_item_path(self, item_id: str) -> str:
        """Get the full path of an item by ID"""
        await self._ensure_client()
        try:
            item = await self.client.me.drive.items_by_id(item_id).get()
            path = ""
            current = item
            while current.parent_reference:
                path = "/" + current.name + path
                if current.parent_reference.id == current.parent_reference.drive_id:
                    break  # Root reached
                current = await self.client.me.drive.items_by_id(current.parent_reference.id).get()
            return path
        except Exception:
            return ""
    
    async def list_files(self, folder_path: str = "root") -> List[Dict[str, Any]]:
        """List files in OneDrive folder"""
        if folder_path != "root" and not self._is_path_allowed(folder_path):
            raise Exception(f"Access denied: Path '{folder_path}' is not allowed")
        
        await self._ensure_client()
        try:
            if folder_path == "root":
                result = await self.client.me.drive.root.children.get()
            else:
                result = await self.client.me.drive.root.item_with_path(folder_path).children.get()
            
            items = result.value if result.value else []
            
            return [
                {
                    "id": item.id,
                    "name": item.name,
                    "size": item.size or 0,
                    "is_folder": hasattr(item, 'folder') and item.folder is not None,
                    "created": item.created_date_time.isoformat() if item.created_date_time else None,
                    "modified": item.last_modified_date_time.isoformat() if item.last_modified_date_time else None,
                    "web_url": item.web_url
                }
                for item in items
            ]
        except Exception as e:
            raise Exception(f"Failed to list files: {str(e)}")
    
    async def upload_file(self, file_path: str, destination_path: str) -> Dict[str, Any]:
        """Upload file to OneDrive"""
        if not self._is_path_allowed(destination_path):
            raise Exception(f"Access denied: Path '{destination_path}' is not allowed")
        
        await self._ensure_client()
        try:
            with open(file_path, "rb") as f:
                file_content = f.read()
            
            result = await self.client.me.drive.root.item_with_path(destination_path).content.put(file_content)
            
            return {
                "id": result.id,
                "name": result.name,
                "size": result.size,
                "web_url": result.web_url
            }
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    
    async def download_file(self, file_id: str, local_path: str) -> bool:
        """Download file from OneDrive"""
        # Check if file path is allowed
        file_path = await self._get_item_path(file_id)
        if not self._is_path_allowed(file_path):
            raise Exception(f"Access denied: File '{file_path}' is not in allowed paths")
        
        await self._ensure_client()
        try:
            result = await self.client.me.drive.items_by_id(file_id).content.get()
            
            with open(local_path, "wb") as f:
                f.write(result)
            
            return True
        except Exception as e:
            raise Exception(f"Failed to download file: {str(e)}")
    
    async def delete_file(self, file_id: str) -> bool:
        """Delete file from OneDrive"""
        # Check if file path is allowed
        file_path = await self._get_item_path(file_id)
        if not self._is_path_allowed(file_path):
            raise Exception(f"Access denied: File '{file_path}' is not in allowed paths")
        
        await self._ensure_client()
        try:
            await self.client.me.drive.items_by_id(file_id).delete()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete file: {str(e)}")
    
    async def get_file_info(self, file_id: str) -> Dict[str, Any]:
        """Get detailed file information"""
        # Check if file path is allowed
        file_path = await self._get_item_path(file_id)
        if not self._is_path_allowed(file_path):
            raise Exception(f"Access denied: File '{file_path}' is not in allowed paths")
        
        await self._ensure_client()
        try:
            result = await self.client.me.drive.items_by_id(file_id).get()
            
            return {
                "id": result.id,
                "name": result.name,
                "size": result.size,
                "created": result.created_date_time.isoformat() if result.created_date_time else None,
                "modified": result.last_modified_date_time.isoformat() if result.last_modified_date_time else None,
                "web_url": result.web_url,
                "parent_reference": result.parent_reference.id if result.parent_reference else None
            }
        except Exception as e:
            raise Exception(f"Failed to get file info: {str(e)}")