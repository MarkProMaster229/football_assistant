from business_logic.negotiation import Negotiation

class NegotiationManager:
    def __init__(self):
        self.negotiation = Negotiation()
    def negotiationManager(self):
        self.negotiation.connekted()