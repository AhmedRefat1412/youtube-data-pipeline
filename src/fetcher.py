import json
import os
from src.api_client import YouTubeAPIClient

class DataFetcher:
    def __init__(self):
        # Create an APIClient object to handle all HTTP requests
        self.client = YouTubeAPIClient()
        self.raw_dir = "data/raw"


    def get_channel_videos(self, channel_id, max_results=50):
        videos = []
        # Parameters for the search request
        params = {
            "part": "snippet",        
            "channelId": channel_id,  
            "maxResults": 50,         
            "type": "video",       
            "order": "viewCount"      
        }
        
        # Keep fetching until we reach the required number of videos
        while len(videos) < max_results:
            response = self.client.get("search", params)
            if not response:
                break
                
            videos.extend(response.get("items", []))
            

            next_page = response.get("nextPageToken")

            if not next_page or len(videos) >= max_results:
                break
                

            params["pageToken"] = next_page

        # Return only the required number of videos
        return videos[:max_results]


    def get_video_details(self, video_ids):
        details = []
        # YouTube API accepts max 50 video IDs per request, so we split into batches
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            params = {
                "part": "snippet,statistics",  
                "id": ",".join(batch)           
            }
            response = self.client.get("videos", params)
            if response:
                details.extend(response.get("items", []))
        return details

    def get_video_comments(self, video_id, max_results=20):
        params = {
            "part": "snippet",         
            "videoId": video_id,        
            "maxResults": max_results,
            "order": "relevance"       
        }
        response = self.client.get("commentThreads", params)

        # If comments are disabled on the video, return an empty list
        if not response:
            return []
        return response.get("items", [])

    def fetch_all(self, channel_ids):
        all_data = []


        for channel_id in channel_ids:
            print(f"Fetching videos for channel: {channel_id}")

            videos = self.get_channel_videos(channel_id, max_results=50)
            
            # Extract only the video IDs from the search results
            video_ids = [
                v["id"]["videoId"] 
                for v in videos 
                if v.get("id", {}).get("videoId")
            ]
            
            details = self.get_video_details(video_ids)
            
            # Loop over each video and fetch its comments
            for video in details:
                video_id = video["id"]
                print(f"  Fetching comments for video: {video_id}")
                comments = self.get_video_comments(video_id)
                # Attach comments directly inside the video object
                video["comments"] = comments
                all_data.append(video)

        # Save all raw data before any transformation
        self.save_raw(all_data)
        return all_data

    def save_raw(self, data):
        path = os.path.join(self.raw_dir, "raw_data.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Raw data saved to {path}")