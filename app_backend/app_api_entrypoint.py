
import os

import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEFAULT_PORT = 8000
PORT: int = int(os.getenv("ASSISTANT_PORT", str(DEFAULT_PORT)))

host: str = "0.0.0.0"
log_level: str = "info"

if __name__ == "__main__":
    uvicorn.run("app_api:app", host=host, port=PORT,log_level=log_level)
