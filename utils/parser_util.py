import json

# NOTE "JOB === CAMPAIGN"
def parse_job(row):
    row_dict = {
        'campaign_id': str(row.campaign_id),
        'bid_amount': float(row.bid_amount),
        'influence_threshold': float(row.influence_threshold),
        'total_amount': float(row.total_amount),
        'influencer_count': int(row.influencer_count),
        'deadline': str(row.deadline),
        'keywords': list(row.keywords),
        'started_by': str(row.started_by),
        'campaign_type': str(row.campaign_type),
        'location': str(row.location),  #NOTE this has to be a be dict like object later on
        'minimum_followers': int(row.minimum_followers),
        'title': str(row.title),
        'started_at': str(row.started_at),
        'status': str(row.status),
        'collaborations': str(row.collaborations),
        'image_context': "DUMMY" #NOTE add this to the system
    }
    return row_dict
def job_rows_to_json(rows):
    json_data = {}
    for row in rows:
        row_dict = parse_job(row)
        json_data[row_dict['job_id']] = row_dict
    # return json.dumps(json_data, indent=4)
    return json_data
def one_job_row_to_json(rows):
    for row in rows:
        return parse_job(row)

def parse_user_profile(row):
    row_dict = {
        'email': row.email,
        'engagement': float(row.engagement),
        'instagram_followers_count': row.instagram_followers_count,
        'instagram_following_count': row.instagram_following_count,
        'instagram_story_per_day': float(row.instagram_story_per_day),
        'instagram_username': row.instagram_username,
        'last_updated': str(row.last_updated),
        'twitter_followers_count': row.twitter_followers_count,
        'twitter_tweets_per_day': row.twitter_tweets_per_day,
        'twitter_username': row.twitter_username,
        'instagram_account_id': row.instagram_account_id
    }
    return row_dict
def user_profile_row_to_json(row):
    row_dict = parse_user_profile(row)
    # return json.dumps(row_dict, indent=4)
    return row_dict


def parse_post(row):
    row_dict = {
        'post_id': row.post_id,
        'caption': row.caption,
        'image': row.image,
        'upload_time': row.upload_time,
        'uploaded_by': row.uploaded_by,
        'url': row.url
    }
    return row_dict
def one_post_row_to_json(row):
    row_dict = parse_post(row)
    return row_dict


