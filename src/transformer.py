class DataTransformer:
    
    def transform_video(self, video):
        # Extract snippet which contains basic video information
        snippet = video.get("snippet", {})
        # Extract statistics which contains views, likes, and comments count
        stats = video.get("statistics", {})

        return {
            # Basic video information
            "video_id": video.get("id"),
            "title": snippet.get("title"),
            "channel_id": snippet.get("channelId"),
            "channel_name": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "description": snippet.get("description"),

            # Statistics, default to 0 if missing to avoid None values
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0)),
        }

    def transform_comments(self, video_id, comments):
        transformed = []
        for item in comments:
            # The actual comment data is nested inside topLevelComment
            comment = item.get("snippet", {}).get("topLevelComment", {})
            snippet = comment.get("snippet", {})

            transformed.append({
                "video_id": video_id,                           
                "author": snippet.get("authorDisplayName"),     
                "text": snippet.get("textDisplay"),             
                "published_at": snippet.get("publishedAt"),     
                "like_count": int(snippet.get("likeCount", 0)) 
            })
        return transformed

    def transform_all(self, raw_data):
        videos = []
        comments = []

        for video in raw_data:
            transformed_video = self.transform_video(video)
            videos.append(transformed_video)

            raw_comments = video.get("comments", [])
            if raw_comments:
                transformed_comments = self.transform_comments(
                    transformed_video["video_id"], 
                    raw_comments
                )
                comments.extend(transformed_comments)

        print(f"Transformed {len(videos)} videos and {len(comments)} comments")
        return videos, comments