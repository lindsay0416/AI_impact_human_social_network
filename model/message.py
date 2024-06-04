class Message:
    def __init__(self, content, sender):
        self.content = content
        self.sender = sender
        self.timestep = None
    
    def __str__(self):
        return f"SENDER: {self.sender.userID} sent CONTENT: '{self.content}' at TIMESTEP {str(self.timestep)}"

    def set_timestep(self, timestep):
        self.timestep = timestep