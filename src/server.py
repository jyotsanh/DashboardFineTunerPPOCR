import argparse
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config.base import BaseConfig, load_environment_variables
from routes import register_routes

# Initialize FastAPI app
app = FastAPI()

# when running the code inside the src folder:
# mode = os.getenv("APP_ENV", "dev")
# load_environment_variables(mode)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware to add processing time header
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Register routes
register_routes(app)

# Run the application
if __name__ == "__main__":
    # parse --run argument
    parser = argparse.ArgumentParser(description="run server in two modes")
    parser.add_argument(
        "--run",
        default="dev",
        choices=["dev", "prod"],
        help="Run mode: dev or prod",
    )
    args = parser.parse_args()

    # Load environment variables
    load_environment_variables(args.run)

    # loads configs
    config = BaseConfig()
    print(f"API Key: {config.API_KEY}")
    if args.run == "prod":
        uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
    else:
        uvicorn.run(
            "server:app",
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info",
        )
