class UserPreference:
    # Initialize UserPreference object with default value (no filter)
    def __init__(self):
        self.max_price_code = None  # C1 value (1-6)
        self.min_ram_code = None    # C2 value (1-4)
        self.selected_profile = "Default"
        self.is_active = False

    # Set constraint for max price based on C1 sub-criteria code
    def set_price_constraint(self, code: int):
        self.max_price_code = code
        self.is_active = True

    # Set constraint for minimum RAM based on C2 sub-criteria code
    def set_ram_constraint(self, code: int):
        self.min_ram_code = code
        self.is_active = True

    # Reset all preferences and filters
    def reset(self):
        self.max_price_code = None
        self.min_ram_code = None
        self.selected_profile = "Default"
        self.is_active = False

    # Check if a smartphone meets the constraints
    def is_eligible(self, smartphone) -> bool:
        if not self.is_active:
            return True
            
        # Check price (C1 is cost, code 1 is cheapest)
        # If user sets max_price_code = 3, then 4,5,6 are ineligible
        if self.max_price_code is not None:
            price_val = smartphone.get_nilai("C1")
            if price_val > self.max_price_code:
                return False
                
        # Check RAM (C2 is benefit, code 1 is lowest)
        # If user sets min_ram_code = 3, then 1,2 are ineligible
        if self.min_ram_code is not None:
            ram_val = smartphone.get_nilai("C2")
            if ram_val < self.min_ram_code:
                return False
                
        return True

    # String representation for UI
    def __str__(self) -> str:
        if not self.is_active:
            return "Tidak ada filter aktif"
        
        parts = []
        if self.max_price_code:
            parts.append(f"Max Harga: Level {self.max_price_code}")
        if self.min_ram_code:
            parts.append(f"Min RAM: Level {self.min_ram_code}")
        
        parts.append(f"Profil: {self.selected_profile}")
        return ", ".join(parts)
