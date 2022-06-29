import requests, sys, hashlib, time, json


######################################
########## GLOBAL CONSTANTS ##########
######################################

APIKEY = "" # API key
FILE_NAME = sys.argv[1] # File name/path passed in as argument
FILE_URL = "https://api.metadefender.com/v4/file" # File lookup URL
BUF_SIZE = 65536 # Hash buffer; allows for more efficient hashing than using entire file 

# Basic API headers
HEADERS = { 
 "apikey": f"{APIKEY}"
}

# API headers for file upload
FILE_HEADERS = { 
 "apikey": f"{APIKEY}",
  "Content-Type": "application/octet-stream", 
 "filename": f"{FILE_NAME}"
}

# API headers for file lookup using data_id
LOOKUP_HEADERS = { 
    "apikey": f"{APIKEY}",
    "x-file-metadata": "1" # 
}

FILE = {'file': open(FILE_NAME,'rb')} # File for upload to API for scan


##########################################
########## FUNCTION DEFINITIONS ##########
##########################################

def print_results(file_name: str, results: dict): # print results of file scan

    print(f"filename: {file_name}\n") # Print name of file_uploaded 
    overall_status = results['scan_results']['scan_all_result_a'] # Overall status of all engine scans of file from API results
    print(f"overall_status: {overall_status}") # Print overall status result
    scan_results = results['scan_results'] # JSON result containing all engines and scan results 
    scan_details = scan_results['scan_details'] # Details of each engine scan i.e. engine, threat_found, etc.

    if len(scan_details) == 0: # If no scan_details, file is still in queue
        print("File has not been scanned yet. try again later") 

    for engine, result in scan_details.items(): # Iterate through details of file scan results; individual engine and results
        print(f"engine: {engine}")
        print("")
        print(f"threat_found: {result['threat_found']}") # Print threat_found results
        print("")
        print(f"scan_result: {result['scan_result_i']}") # Print individual engine results
        print("")
        print(f"def_time: {result['def_time']}") # Print def_time
        print("")

    sys.exit() # Exit program after printing scan results
    

def check_in_queue(file_upload_response: dict): # Check if file is in queue (not scanned) before printing results

    print('Checking if file is still in queue. This may take some time...')
    data_id = file_upload_response['data_id'] # Corresponding file data_id
    file_lookup_id_url = f"https://api.metadefender.com/v4/file/{data_id}"     
    data_id_lookup_response = requests.request("GET", file_lookup_id_url, headers=LOOKUP_HEADERS) # GET request for file lookup
    data_id_lookup_response = json.loads(data_id_lookup_response.text) # File lookup response
    
    start_time = time.time()
    end_time = 0
    while 'scan_result_history_length' not in data_id_lookup_response: # File still in queue not scanned yet, no history yet
        time.sleep(5) # If you don't get response, wait a few seconds before seeking results again; bit more efficient
        data_id_lookup_response = requests.request("GET", file_lookup_id_url, headers=LOOKUP_HEADERS) # Lookup file again if necessary
        data_id_lookup_response = json.loads(data_id_lookup_response.text) # File lookup response
        # print(f"Current scan percentage : {data_id_lookup_response['scan_results']['progress_percentage']}")
        end_time = time.time()
        if end_time - start_time > 120: # If file is still in queue after a couple minutes, exit program
            print("File is still in queue. You may want to wait a few minutes before trying again.")
            sys.exit()



##### MAIN #####

if __name__ == "__main__":
    
# Calculate hash below 
    file_hash = hashlib.sha256() # Using SHA256 for purposes of this program; Python hashlib library
    print("Hashing file...")
    with open(FILE_NAME, 'rb') as f: # Open the file to read bytes
        fb = f.read(BUF_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BUF_SIZE) # Read the next block from the file

    hash = file_hash.hexdigest() # Convert calculated hash to hexadecimal
    print(f"Calculated SHA256 hash: {hash}") # Print hash
    hash_url = f"https://api.metadefender.com/v4/hash/{hash}" # Hash lookup URL for API
    response = requests.request("GET", hash_url, headers=HEADERS) # GET request for hash lookup using hash URL

    json_response = response.text # or could response.content; TypeError: the JSON object must be str, bytes or bytearray, not dict
    hash_lookup_response = json.loads(json_response) # Load hash lookup JSON response as dict

    try: 
        if 'data_id' in hash_lookup_response: # If 'data_id' is present in response, a file was matched and returned  
            check_in_queue(hash_lookup_response) # Check if file has been scanned yet
            print_results(FILE_NAME, hash_lookup_response) # Print results of scan

        if 'error' in hash_lookup_response: # If 'error' is returned, than no file hash was matched

            print("Uploading file to API. This may take a minute...")
            file_upload_response = requests.post(FILE_URL, files=FILE, headers=HEADERS) # Upload file to API
            file_upload_response = json.loads(file_upload_response.text) # File upload response containing data_id
            check_in_queue(file_upload_response) # Check if file is still in queue
            print_results(FILE_NAME, file_upload_response) # File is not in queue anymore, print results

    except KeyError as error:
        print(f"Unexpected API response: {error}")
        sys.exit()
    
