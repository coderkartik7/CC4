from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

#App
app = FastAPI()

#Mounting static files
app.mount("/static", StaticFiles(directory="./static"), name="static")

#Serving HTML Page
@app.get("/", response_class=HTMLResponse)
async def homepage():
    with open("./templates/index.html",encoding="utf-8") as f:
        return HTMLResponse(f.read())
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)