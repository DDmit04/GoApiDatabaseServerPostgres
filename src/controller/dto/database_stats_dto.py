class DatabaseStatsDto:
    def __init__(self, current_bytes: int, fill_percent: float,
                 database_and_username: str, allow_connections: bool):
        super().__init__()
        self.fill_percent = fill_percent
        self.current_size = current_bytes
        self.database_and_username = database_and_username
        self.allow_connections = allow_connections
