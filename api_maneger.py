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
        print(selected_key)
        # Remove the selected key from the available list
        self.available_keys.remove(selected_key)
        return selected_key


# List of API keys (update the list with your keys)
API_KEYS = [
    "AIzaSyCCMYyicdsYdfQGRjDr3HAs0ncPFcIdIpE", # 1
    "AIzaSyCS_9W2zFwJ-vN96PW4w0EtU5f5tFOWB_o", # 1
    "AIzaSyAFUrDlI4YzcUpcSVLRGFDiHrzYN6RgTgo", # 1
    "AIzaSyBcqaGmVIBd-21S7ncw1TO43Oa8vpyRirg", # 1
    "AIzaSyCwPOjW_MJGkGPRPO7e3i5NRE1i2EpPe00" # 1
]
# Create an instance of APIManager
api_manager = APIManager(API_KEYS)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ADHAR CARD
system_prompt_Adhar = """
        You are a specialist in analyzing government-issued identity documents.
        You will receive images of documents such as PAN cards and Aadhar cards,
        and your task is to extract structured data fields based on the document type.
        """
user_prompt_Adhar = """
        You are an intelligent assistant specialized in extracting structured data from government-issued documents. 
        Given the text extracted from an identity document, please provide the following fields in JSON format based on the document type:
        For an Aadhar Card:
        - "documentType": "Aadhar Card"
        - "Aadhar Number": The unique 12-digit Aadhar number.
        - "Name": The name of the individual.
        - "dateOfBirth": The date of birth in the format DD/MM/YYYY. (if Date of Birth is not present then Year Of Birth will be present and that will be in YYYY forma but it will also included in dateOfBirth )
        - "Address": The full address including street, city, district, state, and postal code.
        Ensure the fields are extracted accurately, respecting any formatting for dates and numbers. 
        """

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PAN CARD
system_prompt_pan = """
        You are a specialist in analyzing government-issued identity documents.
        You will receive images of documents such as PAN cards and Aadhar cards,
        and your task is to extract structured data fields based on the document type.
        """
user_prompt_pan = """
        You are an intelligent assistant specialized in extracting structured data from government-issued documents. 
        Given the text extracted from an identity document, please provide the following fields in JSON format based on the document type:
        For a PAN Card:
        - "documentType": "PAN Card"
        - "panNumber": The Permanent Account Number (PAN) on the card.
        - "name": The name of the individual.
        - "fatherName": The father's name (if present). (father name will be the next line of the name)
        - "dateOfBirth": The date of birth in the format DD/MM/YYYY. (dateOfBirth will be the next line of father name)
        """