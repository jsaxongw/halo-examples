import io
import os
import requests
import zipfile
import time

def call_api_with_basic_auth(url, username, password, file_path, save_directory):
    try:
        # Create a session object
        session = requests.Session()

        # Set up basic authentication
        session.auth = (username, password)

        # Prepare query parameters
        params = {
            "format": "json"
        }

        # Read the binary file
        with open(file_path, 'rb') as file:
            file_data = file.read()

        # Make the API request with the JSON payload
        response = session.post(url, params=params, files={'file': file_data})

        # Check if the request was successful (status code 201 or 206)
        if response.status_code in (201, 206):
            # Unzip the response content in memory
            with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
                # Get the x-processing-id header value
                processing_id = response.headers.get('x-processing-id')

                # Create a folder with the x-processing-id value
                processing_id_folder = os.path.join(save_directory, processing_id)
                os.makedirs(processing_id_folder, exist_ok=True)

                # Extract all files from the ZIP file in memory
                zip_ref.extractall(processing_id_folder)

                # Get the original file name and extension
                original_filename, original_extension = os.path.splitext(os.path.basename(file_path))

                # Define paths to clean and analysis files
                clean_file_path = os.path.join(processing_id_folder, 'clean', 'file')
                analysis_file_path = os.path.join(processing_id_folder, 'report', 'file.report.json')

                print("clean_file_path:", clean_file_path)
                
                # Rename analysis report to analysis.json if it exists
                if os.path.exists(analysis_file_path):
                    os.rename(analysis_file_path, os.path.join(processing_id_folder, 'report', 'analysis.json'))

                if os.path.exists(clean_file_path):
                    os.rename(clean_file_path, os.path.join(processing_id_folder, 'clean', original_filename + original_extension))
                
                return processing_id_folder
        elif response.status_code == 429:
            # If the request was rate-limited (status code 429), wait and retry after some time
            print("Too many requests. Waiting for 10 seconds before retrying...")
            time.sleep(10)
            return call_api_with_basic_auth(url, username, password, file_path, save_directory)
        elif response.status_code >= 400:
            # If the request was unsuccessful and status code is 400 or above, print error details
            if 'Errors' in response.json():
                error_details = response.json()['Errors'][0]
                print(f"API call failed with error code {error_details.get('ErrorCode', 'Unknown')}: {error_details.get('ErrorDescription', 'Unknown')}")
            else:
                print("API call failed. Unknown error.")
            return None
        else:
            # If the request was unsuccessful and status code is not 400 or above, print generic error message
            print(f"Failed to call API. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        # If there was a problem with the request, print the error
        print(f"Error calling API: {e}")
        return None

# Example usage:
url = "https://api.example.com/upload"
username = "your_username"
password = "your_password"
file_path = "path_to_your_file/sample.pdf"  # Replace this with the actual path to your binary file
save_directory = "path_to_save_directory"  # Replace this with the directory where you want to save the files

processing_id_folder = call_api_with_basic_auth(url, username, password, file_path, save_directory)
if processing_id_folder:
    print("Output stored in folder:", processing_id_folder)
else:
    print("API call failed.")
