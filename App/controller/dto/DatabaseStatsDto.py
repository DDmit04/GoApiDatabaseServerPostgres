class DatabaseStatsDto:
    def __init__(self, current_bytes, fill_percent) -> None:
        super().__init__()
        self.fill_percent = fill_percent
        self.current_size = current_bytes
