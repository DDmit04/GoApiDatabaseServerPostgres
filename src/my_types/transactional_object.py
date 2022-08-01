from sqlalchemy.orm import Session


class TransactionalObject(object):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

