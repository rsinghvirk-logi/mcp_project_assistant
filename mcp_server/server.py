from mcp.server.fastmcp import FastMCP
from tools.read_file import read_file
from tools.write_file import write_file
from tools.fetch_web import fetch_web

app = FastMCP(name="Goal-Driven Research Assistant Tools")

app.tool(
    name="read_file",
    description="Read a text file from disk"
)(read_file)

app.tool(
    name="write_file",
    description="Write text to a file on disk"
)(write_file)

app.tool(
    name="fetch_web",
    description="Fetch raw text content from a URL"
)(fetch_web)