"""
   Common snapshot execpetion.
"""
class SnapshotsException(Exception):
    """Exception raised for snapshots"""

    def __init__(self, message="Error in snapshots for container"):
        self.message = message
        super().__init__(self.message)
