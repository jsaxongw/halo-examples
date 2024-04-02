# Call Halo API with Basic Authentication

This C# script demonstrates how to make an API call to the Halo platform using basic authentication. The API call sends a binary file to the Halo API, retrieves the response (a ZIP archive), and extracts its contents to a specified directory.

## Prerequisites

- [.NET Core SDK](https://dotnet.microsoft.com/download) installed on your system.
- Required NuGet packages: `Flurl.Http`, `Polly`.

## Usage

1. **Clone the Repository**: Clone or download the repository containing the C# script.

2. **Update Script Variables**: Open the C# script (`Program.cs`) in a text editor and update the following variables:

    - `url`: The URL of the Halo API endpoint.
    - `username`: Your username for basic authentication.
    - `password`: Your password for basic authentication.
    - `filePath`: The path to the binary file you want to send to the API.
    - `saveDirectory`: The directory where you want to save the extracted files.

3. **Install NuGet Packages**: Restore the required NuGet packages using the following command in the terminal or command prompt:

    ```
    dotnet restore
    ```

4. **Run the Script**: Build and run the C# script using the following command:

    ```
    dotnet run
    ```

    This will make the API call with the specified parameters. If successful, the extracted files will be saved in the specified directory.

## Retry Policy

The script includes a retry policy to handle rate-limited responses (HTTP status code 429). It will automatically retry the API call up to 3 times with a fixed delay of 10 seconds between retries.

## Error Handling

The script handles various error scenarios, such as HTTP errors, API call failures, and exceptions during execution. Error messages will be displayed in the console output for troubleshooting.
