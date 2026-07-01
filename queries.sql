-- Query 1: Top 10 videos by view count
SELECT 
    title,
    channel_name,
    view_count,
    like_count,
    comment_count
FROM videos
ORDER BY view_count DESC
LIMIT 10;

-- Query 2: Average views, likes, and comments per channel
SELECT 
    channel_name,
    COUNT(*) as total_videos,
    ROUND(AVG(view_count)) as avg_views,
    ROUND(AVG(like_count)) as avg_likes,
    ROUND(AVG(comment_count)) as avg_comments
FROM videos
GROUP BY channel_name
ORDER BY avg_views DESC;

-- Query 3: Most engaging videos (highest like-to-view ratio)
SELECT 
    title,
    channel_name,
    view_count,
    like_count,
    ROUND((like_count::DECIMAL / NULLIF(view_count, 0)) * 100, 2) as engagement_rate
FROM videos
WHERE view_count > 0
ORDER BY engagement_rate DESC
LIMIT 10;