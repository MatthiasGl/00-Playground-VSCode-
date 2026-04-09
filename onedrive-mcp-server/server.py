import asyncio
from mcp.server.fastmcp import FastMCP
from onedrive_client import OneDriveClient
from config import settings

# Initialize MCP server
mcp = FastMCP(
    name=settings.MCP_SERVER_NAME,
    instructions="OneDrive file management server with list, upload, download capabilities"
)

# Initialize OneDrive client
onedrive = OneDriveClient()

# ============ TOOLS ============

@mcp.tool()
async def list_files(folder_path: str = "root") -> str:
    """List files in OneDrive folder
    
    Args:
        folder_path: Path to folder (default: 'root')
    
    Returns:
        JSON string with file listing
    """
    try:
        files = await onedrive.list_files(folder_path)
        return f"Found {len(files)} items:\n" + "\n".join(
            f"- {f['name']} ({'Folder' if f['is_folder'] else f['size']} bytes)"
            for f in files
        )
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def upload_file(local_path: str, destination_path: str) -> str:
    """Upload file to OneDrive
    
    Args:
        local_path: Local file path
        destination_path: Destination path in OneDrive
    
    Returns:
        Upload result with file info
    """
    try:
        result = await onedrive.upload_file(local_path, destination_path)
        return f"✓ File uploaded successfully:\nName: {result['name']}\nSize: {result['size']} bytes\nURL: {result['web_url']}"
    except Exception as e:
        return f"✗ Upload failed: {str(e)}"

@mcp.tool()
async def download_file(file_id: str, local_path: str) -> str:
    """Download file from OneDrive
    
    Args:
        file_id: OneDrive file ID
        local_path: Local save path
    
    Returns:
        Download status
    """
    try:
        success = await onedrive.download_file(file_id, local_path)
        if success:
            return f"✓ File downloaded successfully to {local_path}"
        return "✗ Download failed"
    except Exception as e:
        return f"✗ Download failed: {str(e)}"

@mcp.tool()
async def delete_file(file_id: str) -> str:
    """Delete file from OneDrive
    
    Args:
        file_id: OneDrive file ID
    
    Returns:
        Deletion status
    """
    try:
        success = await onedrive.delete_file(file_id)
        if success:
            return "✓ File deleted successfully"
        return "✗ Deletion failed"
    except Exception as e:
        return f"✗ Deletion failed: {str(e)}"

@mcp.tool()
async def get_file_info(file_id: str) -> str:
    """Get detailed file information
    
    Args:
        file_id: OneDrive file ID
    
    Returns:
        File information details
    """
    try:
        info = await onedrive.get_file_info(file_id)
        return f"""File Information:
Name: {info['name']}
Size: {info['size']} bytes
Created: {info['created']}
Modified: {info['modified']}
URL: {info['web_url']}"""
    except Exception as e:
        return f"Error: {str(e)}"

# ============ RESOURCES ============

@mcp.resource("onedrive://files/{folder_path}")
async def read_files(folder_path: str = "root") -> str:
    """Resource to browse OneDrive files"""
    files = await onedrive.list_files(folder_path)
    import json
    return json.dumps(files, indent=2)

@mcp.resource("onedrive://file-info/{file_id}")
async def read_file_info(file_id: str) -> str:
    """Resource to get file information"""
    info = await onedrive.get_file_info(file_id)
    import json
    return json.dumps(info, indent=2)

# ============ PROMPTS ============

@mcp.prompt()
def onedrive_help() -> str:
    """OneDrive MCP Server Help"""
    return """OneDrive MCP Server provides tools for:
    
1. **list_files(folder_path)** - List files in a folder
2. **upload_file(local_path, destination_path)** - Upload file to OneDrive
3. **download_file(file_id, local_path)** - Download file from OneDrive
4. **delete_file(file_id)** - Delete file from OneDrive
5. **get_file_info(file_id)** - Get detailed file information

Resources:
- onedrive://files/{folder_path} - Browse files
- onedrive://file-info/{file_id} - File details

Use these tools to manage your OneDrive storage."""

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=settings.MCP_PORT)