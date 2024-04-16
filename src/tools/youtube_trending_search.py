import requests
from datetime import datetime, timedelta
import os
from langchain.tools import tool


class YouTubeTrendingSearchTool:

    @tool("Searches the latest trends on competitor's channels")
    def find_trending_videos(topic: str, days_published: int = -1, max_results: int = 10) -> list:
        """
        Searches for trending YouTube videos related to a specified topic using typical user search terms.

        Parameters:
            topic (str): The topic to search for, structured as a user might input, such as "home lab",
                         "pfsense on a raspberry pi", or "the best docker apps for home lab". Avoid using
                         logical connectors like "and" or "or" in the search terms.
            days_published (int): Optional; defines the time frame for the search, counting backwards from
                                  the current day. For example, a value of 90 searches for videos published
                                  within the last 90 days. A value of -1 applies no time constraints and performs
                                  a default search. The default is -1.
            max_results (int): Optional; sets the maximum number of search results to return. Can be set
                               between 0 and 10, inclusive, with a default value of 10.

        Returns:
            list of dict: A list containing dictionaries, each representing details of a trending video.

        Notes:
            The function returns up to 10 videos by default. It is tailored to capture recent trends based
            on user-defined topics and the specified publication window.
        """

        # Define the API endpoint and parameters
        url = "https://www.googleapis.com/youtube/v3/search"
        api_key = os.environ.get("YOUTUBE_API_KEY")

        params = {
            "part": "snippet",
            "q": topic,
            "type": "video",
            "maxResults": max_results,
            "order": "viewCount",  # Ordering by view count might mimic "trending"
            "key": api_key,
            "regionCode": "US",
            "relevanceLanguage": "en",
            "channelType": "any",
        }

        if days_published > -1:
            start_date, end_date = YouTubeTrendingSearchTool.calculate_date_range(days_published)
            params.update({"publishedAfter": start_date, "publishedBefore": end_date})

        # Make the API request
        response = requests.get(url, params=params)
        if response.status_code == 200:
            videos = response.json().get("items", [])
            video_ids = ",".join([video["id"]["videoId"] for video in videos])
            video_details = YouTubeTrendingSearchTool.get_video_details(video_ids, api_key)

            # Merge video details with search results
            # Extracting relevant details from each video
            results = [
                {
                    "title": video["snippet"]["title"],
                    # "description": video["snippet"]["description"],
                    "publishedAt": video["snippet"]["publishedAt"],
                    "channelId": video["snippet"]["channelId"],
                    "channelTitle": video["snippet"]["channelTitle"],
                    "videoId": video["id"]["videoId"],
                    "viewCount": video_details.get(video["id"]["videoId"], {}).get("viewCount", "N/A"),
                }
                for video in videos
            ]
            return results
        else:
            raise Exception("Failed to fetch data: " + response.text)

    @staticmethod
    def get_video_details(video_ids: str, api_key) -> dict:

        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "statistics",
            "id": video_ids,
            "key": api_key,
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            details = response.json().get("items", [])

            return {detail["id"]: detail["statistics"] for detail in details}
        else:
            raise Exception("Failed to fetch video details: " + response.text)

    @staticmethod
    def calculate_date_range(days_published: int) -> tuple:
        """
        Calculates the start and end dates for filtering YouTube videos based on their publication date.

        Parameters:
        - days_published: Specifies a range measured in days counting backwards from the current time.

        Returns:
        - A tuple containing the start and end dates in ISO 8601 format.
        """
        end_date = datetime.now().isoformat("T") + "Z"
        start_date = (datetime.now() - timedelta(days=days_published)).isoformat("T") + "Z"
        return start_date, end_date


# def testCode():

#     load_dotenv()

#     videos = YouTubeTrendingSearchTool.find_trending_videos(topic="homelab|pfsense", days_published=30, max_results=10)

#     for video in videos:
#         print(f"Title: {video['title']}")
#         # print(f"Description: {video['description']}")
#         print(f"Published At: {video['publishedAt']}")
#         print(f"Channel ID: {video['channelId']}")
#         print(f"Channel Title: {video['channelTitle']}")
#         print(f"Video ID: {video['videoId']}")
#         print(f"Views:{video['viewCount']}")
#         print("---")


# if __name__ == "__main__":
#     testCode()
