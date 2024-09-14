from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    try:
        errors = []

        for error in exc.errors():
            field = error["loc"]
            input = error["input"]
            message = error["msg"]

            if isinstance(input, dict):
                input = input.get(field[-1])

            errors.append(
                {
                    "location": " -> ".join(field),
                    "detail": message,
                    "input": input,
                }
            )

        return JSONResponse(content=errors, status_code=422)
    except TypeError:
        return JSONResponse(
            status_code=422, content={"detail": "invalid json"}
        )
