from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from sqlmodel import Session, create_engine

from models import User, Address, Base

engine = create_engine("sqlite:///database.db")

Base.metadata.create_all(engine)


async def create_user(request: Request):
    user = await request.json()
    with Session(engine) as session:
        spongebob = User(
            name="spongebob",
            fullname="Spongebob Squarepants",
            addresses=[Address(email_address="spongebob@sqlalchemy.org")],
        )
        sandy = User(
            name="sandy",
            fullname="Sandy Cheeks",
            addresses=[
                Address(email_address="sandy@sqlalchemy.org"),
                Address(email_address="sandy@squirrelpower.org"),
            ],
        )
        patrick = User(name="patrick", fullname="Patrick Star")
        session.add_all([spongebob, sandy, patrick])
        session.commit()
        return JSONResponse(spongebob.as_dict())


routes = [
    Route(path="/", endpoint=create_user, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)


def main():
    import uvicorn

    uvicorn.run(app, port=5000, log_level="debug")


if __name__ == "__main__":
    main()
