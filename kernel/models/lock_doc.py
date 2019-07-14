class LockDoc:
    def __init__(self, _id, status="", last_updated="", last_run="", last_id=""):
        self._id = _id
        self.status = status
        self.last_updated = last_updated
        self.last_run = last_run
        self.last_id = last_id
