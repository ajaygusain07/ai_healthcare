class EmergencyService:
    KEYWORDS = {
        "cardiac": ["chest pain", "seene mein dard", "heart attack"],
        "respiratory": ["saans nahi", "breathe nahi", "dam ghut"],
        "bleeding": ["khoon", "bleeding", "blood"],
        "unconscious": ["behosh", "unconscious", "faint"],
    }
    
    def check(self, text: str) -> dict:
        text_lower = text.lower()
        for etype, keywords in self.KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return {
                        "is_emergency": True,
                        "type": etype,
                        "message": "🚨 Yeh emergency lag rahi hai! Turant 112 call karein ya nearest hospital jayein!"
                    }
        return {"is_emergency": False}