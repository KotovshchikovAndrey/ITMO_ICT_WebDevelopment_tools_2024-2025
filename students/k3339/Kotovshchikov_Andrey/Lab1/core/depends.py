from fastapi import Request


async def get_session(request: Request):
    connection = request.app.state.connection
    session = connection.get_session()
    try:
        yield session
        await session.commit()
    except Exception as exc:
        await session.rollback()
        raise exc
    finally:
        await session.remove()
