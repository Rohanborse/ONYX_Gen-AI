import random


class APIManager:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.available_keys = list(api_keys)  # Copy of the API keys for tracking usage

    def get_random_api(self):
        # Check if all keys are exhausted
        if not self.available_keys:
            # Reinitialize the list when all keys have been used
            self.available_keys = list(self.api_keys)
            print("All keys used once. Reinitializing the keys.")

        # Randomly select a key from available keys
        selected_key = random.choice(self.available_keys)
        # Remove the selected key from the available list
        self.available_keys.remove(selected_key)
        return selected_key


# List of API keys (update the list with your keys)
API_KEYS = [
    "AIzaSyCfU4W6oGTpz6tZYW5Yyzce8AAKYQlnXlY",
    "AIzaSyC0-mdLaPgzxEmxQVK71SH4MxXjIAB6SqM",
    "AIzaSyC3IACYubtlzO6djU8Y4wDB5oSwVACkw_Y",
    "AIzaSyCraN2qjLcwFoWlmmCyFuWGhAQmcWYuQZE",
    "AIzaSyCCMYyicdsYdfQGRjDr3HAs0ncPFcIdIpE",
    "AIzaSyCS_9W2zFwJ-vN96PW4w0EtU5f5tFOWB_o",
    "AIzaSyAFUrDlI4YzcUpcSVLRGFDiHrzYN6RgTgo",
    "AIzaSyCP6JZiT1SCjT7d0R1WHwS6mt7BO3btvcs",
    "AIzaSyBcqaGmVIBd-21S7ncw1TO43Oa8vpyRirg",
    "AIzaSyCwPOjW_MJGkGPRPO7e3i5NRE1i2EpPe00"
]

# Create an instance of APIManager

api_manager = APIManager(API_KEYS)
