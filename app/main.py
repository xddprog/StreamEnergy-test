from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import app.routers as routers
from app.database.connection import DatabaseConnection
from app.utils.config.loads import load_database_config


async def lifespan(app: FastAPI):
    app.state.db_connection = DatabaseConnection(load_database_config())
    await app.state.db_connection.create_tables()
    yield


app = FastAPI(lifespan=lifespan)


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
    except TypeError as e:
        print(e)
        return JSONResponse(
            status_code=422, content={"detail": "invalid json"}
        )


app.include_router(routers.auth_router)
app.include_router(routers.user_router)
app.include_router(routers.notes_router)
