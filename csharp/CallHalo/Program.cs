using Flurl.Http;
using Polly;
using Polly.Retry;
using SharpCompress.Archives;
using SharpCompress.Common;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "REPLACE_WITH_API_URL";
        string username = "REPLACE_WITH_USERNAME";
        string password = "REPLACE_WITH_PASSWORD";
        string filePath = "REPLACE_WITH_FILE_PATH"; // Replace this with the actual path to your binary file
        string saveDirectory = "REPLACE_WITH_SAVE_DIRECTORY"; // Replace this with the directory where you want to save the files

        string processingIdFolder = await CallApiWithBasicAuth(url, username, password, filePath, saveDirectory);
        if (processingIdFolder != null)
        {
            Console.WriteLine("Output stored in folder: " + processingIdFolder);
        }
        else
        {
            Console.WriteLine("API call failed.");
        }
    }

    static async Task<string> CallApiWithBasicAuth(string url, string username, string password, string filePath, string saveDirectory)
    {
        try
        {
            var response = await GetRetryPolicy()
                .ExecuteAsync(async () =>
                    await url
                        .WithBasicAuth(username, password)
                        .SetQueryParam("format", "json")
                        .PostMultipartAsync(mp => mp
                            .AddFile("file", filePath)));

            if (response.StatusCode == 201 || response.StatusCode == 206)
            {
                using (var archive = ArchiveFactory.Open(await response.GetStreamAsync()))
                {
                    response.Headers.TryGetFirst("x-processing-id", out var processingId);
                    var outputFolder = Path.Combine(saveDirectory, processingId);

                    foreach (var entry in archive.Entries)
                    {
                        if (!entry.IsDirectory)
                        {
                            var entryFileName = entry.Key;
                            var entryPath = Path.Combine(outputFolder, entryFileName);
                            var entryDirectory = Path.GetDirectoryName(entryPath);

                            // Ensure the directory exists
                            Directory.CreateDirectory(entryDirectory);

                            // Extract the entry
                            entry.WriteToDirectory(entryDirectory, new ExtractionOptions()
                            {
                                ExtractFullPath = false,
                                Overwrite = true
                            });
                        }
                    }

                    return outputFolder;
                }
            }
            else
            {
                Console.WriteLine($"Failed to call API. Status code: {response.StatusCode}");
                return null;
            }
        }
        catch (Exception e)
        {
            Console.WriteLine($"Error calling API: {e.Message}");
            return null;
        }
    }

    private static AsyncRetryPolicy GetRetryPolicy()
    {
        return Policy
            .Handle<FlurlHttpException>(e => e.StatusCode == 429)
            .WaitAndRetryAsync(
                3,
                (retryCount, exception, context) =>
                {
                    var delta = ((FlurlHttpException)exception).Call.HttpResponseMessage.Headers.RetryAfter.Delta;
                    return delta ?? TimeSpan.FromSeconds(10);
                },
                async (e, ts, i, ctx) => { Console.WriteLine($"CDR Platform returned busy status - retrying {i}"); });
    }
}
