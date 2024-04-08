# Performance Testing with k6

This repository contains a k6 script for performance testing Halo by uploading a file with Basic Authentication. The script simulates multiple virtual users making concurrent requests to the API endpoint.

## Setup

### Prerequisites

- [k6](https://k6.io/docs/getting-started/installation/): Install k6 on your local machine.
- Node.js: Ensure Node.js is installed to run the dependencies installation script.

## Usage

1. Open the `script.js` file and update the following variables:

   - `rebuildApiHostName`: Replace `"HALO URL"` with the base URL of the API endpoint.
   - `testFilePath`: Replace `"PATH TO FILE"` with the path to the file you want to upload.
   - `username`: Replace `"USERNAME"` with your API username.
   - `password`: Replace `"PASSWORD"` with your API password.

2. Run the k6 script:

   ```bash
   k6 run halo-load-test.js
   ```

## Script Explanation

- The script loads a file specified by `testFilePath`.
- It authenticates using Basic Authentication with the provided username and password.
- Generates a unique filename using `uuidv4()` to avoid conflicts.
- Submits a POST request to the specified API endpoint with the file data.
- Checks if the response status is 201 (Created).

## Reporting

After running the script, you will get:

- A summary printed to stdout.
- A summary report in HTML format (`result.html`).
- A detailed summary in JSON format (`summary.json`).