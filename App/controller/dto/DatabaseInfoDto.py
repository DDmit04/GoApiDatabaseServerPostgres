class DatabaseInfoDto:

    def __init__(self, database_name, username) -> None:
        super().__init__()
        self.database_name = database_name
        self.username = username
