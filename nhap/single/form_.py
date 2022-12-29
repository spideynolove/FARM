from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/double")
async def double_num(request: Request):
    return templates.TemplateResponse('double.html', context={'request': request})


@app.post("/double")
async def double_num(num: float = Form(...)):
    return num * 2


# @app.get("/login")
# async def login(request: Request):
#     return templates.TemplateResponse('login.html', context={'request': request})


# @app.post("/login")
# async def login(num: float = Form(...)):
#     # print access token
#     return num * 2


@app.get('/submit', response_class=HTMLResponse)
async def event_create_form(request: Request):
    html_content = """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Hello</title>
        <script>
            document.addEventListener("DOMContentLoaded", (event) => {
                document.getElementById("myForm").addEventListener("submit", function (e) {
                    e.preventDefault(); // Cancel the default action
                    submitForm();
                });
            });
        </script>
    </head>

    <body>
        <form id="myForm" method="POST" action="/submittt">
            <input type="text" name="id">
            <input type="submit" value="Create Event">
        </form>
        <div id="responseArea">Type a number</div>
        <script>
            function submitForm() {
                var formElement = document.getElementById('myForm');
                var data = new FormData(formElement);
                // fetch this
                fetch('/submit', {   
                    method: 'POST',
                    body: data,
                })
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById("responseArea").innerHTML = data;
                    })
                    .catch(error => {
                        console.error(error);
                    });
            }
        </script>
    </body>

    </html>
    """
    return HTMLResponse(content=html_content, status_code=200, )


@app.post('/submit')
async def event_create(id: int = Form(...)):
    return id