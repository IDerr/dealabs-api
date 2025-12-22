import datetime


def parse_timestamp(value):
    """
    Parse a timestamp value that can be a Unix timestamp (int/float) or ISO string.
    Returns a datetime object or None if parsing fails.
    """
    if isinstance(value, (int, float)):
        return datetime.datetime.fromtimestamp(value, tz=datetime.timezone.utc)
    elif isinstance(value, str):
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            try:
                return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                return None
    return None


class Deal:
    def __init__(self, data):
        self.data = data
        self.deal_type = data.get('_type')
        self.thread_id = data.get('thread_id')
        self.title = data.get('title')
        self.url = data.get('deal_uri')
        self.price = data.get('price')
        self.category = data.get('group_display_summary')
        self.groups = data.get('group_ids')
        self.merchant = data.get('merchant', {}).get('name') if data.get('merchant') else None
        self.temperature = int(data.get('temperature_rating'))
        self.temperature_level = data.get('temperature_level')
        self.is_hot = data.get('is_hot')
        self.created = parse_timestamp(data.get('created'))

    def __repr__(self):
        return f"Deal(id={self.thread_id}, title='{self.title}')"

    def to_dict(self):
        return {
            'thread_id': self.thread_id,
            'title': self.title,
            'url': self.url,
            'price': self.price,
            'category': self.category,
            'merchant': self.merchant,
            'temperature': self.temperature,
            'temperature_level': self.temperature_level,
            'is_hot': self.is_hot,
            'created': self.created.isoformat() if self.created else None
        }


class Thread:
    def __init__(self, data):
        self.data = data
        self.thread_id = data.get('thread_id')
        self.title = data.get('title')
        self.status = data.get('status')
        self.deal_uri = data.get('deal_uri')
        self.type = data.get('_type')

        # Timestamps
        self.submitted_at = parse_timestamp(data.get('submitted_at'))
        self.bumped_at = parse_timestamp(data.get('bumped_at'))
        self.updated = parse_timestamp(data.get('updated'))
        self.hot_date = parse_timestamp(data.get('hot_date'))

        # Counters and ratings
        self.comment_count = data.get('comment_count', 0)
        self.temperature_rating = data.get('temperature_rating', 0)
        self.is_hot = data.get('is_hot', False)

        # Price information
        self.price = data.get('price')
        self.price_display = data.get('price_display')

        # Merchant information
        merchant_data = data.get('merchant', {})
        if isinstance(merchant_data, dict):
            self.merchant_name = merchant_data.get('name')
            self.merchant_id = merchant_data.get('merchant_id')
            self.merchant_logo = merchant_data.get('logo_uri')
        else:
            self.merchant_name = None
            self.merchant_id = None
            self.merchant_logo = None

        # User/poster information
        poster_data = data.get('poster', {})
        if isinstance(poster_data, dict):
            self.poster_username = poster_data.get('username')
            self.poster_user_id = poster_data.get('user_id')
            self.poster_avatar = poster_data.get('profile_image_uri')
        else:
            self.poster_username = None
            self.poster_user_id = None
            self.poster_avatar = None

        # Additional fields
        self.shareable_link = data.get('shareable_link')
        self.code = data.get('code')
        self.is_verified = data.get('is_verified', False)
        self.description = data.get('description')
        self.main_image = data.get('main_image')
        self.temperature_level = data.get('temperature_level')
        self.category = data.get('group_display_summary')
        self.groups = data.get('group_ids', [])

    def __repr__(self):
        return f"Thread(id={self.thread_id}, title='{self.title}')"

    def to_dict(self):
        return {
            'thread_id': self.thread_id,
            'title': self.title,
            'status': self.status,
            'deal_uri': self.deal_uri,
            'type': self.type,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'bumped_at': self.bumped_at.isoformat() if self.bumped_at else None,
            'updated': self.updated.isoformat() if self.updated else None,
            'hot_date': self.hot_date.isoformat() if self.hot_date else None,
            'comment_count': self.comment_count,
            'temperature_rating': self.temperature_rating,
            'is_hot': self.is_hot,
            'price': self.price,
            'price_display': self.price_display,
            'merchant_name': self.merchant_name,
            'merchant_id': self.merchant_id,
            'merchant_logo': self.merchant_logo,
            'poster_username': self.poster_username,
            'poster_user_id': self.poster_user_id,
            'poster_avatar': self.poster_avatar,
            'shareable_link': self.shareable_link,
            'code': self.code,
            'is_verified': self.is_verified,
            'description': self.description,
            'main_image': self.main_image,
            'temperature_level': self.temperature_level,
            'category': self.category,
            'groups': self.groups,
        }


class Comment:
    def __init__(self, data):
        self.data = data
        self.comment_id = data.get('comment_id')
        self.thread_id = data.get('thread_id')
        self.content_unformatted = data.get('content_unformatted')

        # Timestamps
        self.posted = parse_timestamp(data.get('posted'))
        self.updated = parse_timestamp(data.get('updated'))

        # User/poster information
        poster_data = data.get('poster', {})
        if isinstance(poster_data, dict):
            self.poster_username = poster_data.get('username')
            self.poster_user_id = poster_data.get('user_id')
            self.poster_avatar = poster_data.get('profile_image_uri')
        else:
            self.poster_username = None
            self.poster_user_id = None
            self.poster_avatar = None

        # Status and permissions
        self.status = data.get('status')
        self.is_editable = data.get('is_editable', False)
        self.is_liked = data.get('is_liked', False)
        self.can_like = data.get('can_like', False)
        self.can_reply = data.get('can_reply', False)

        # Reaction counters
        self.reaction_counters = data.get('reaction_counters', {})

        # Thread structure
        self.parent_id = data.get('parent_id')
        self.children_count = data.get('children_count', 0)
        self.replied_to = data.get('replied_to')

    def __repr__(self):
        return f"Comment(id={self.comment_id}, thread_id={self.thread_id}, poster='{self.poster_username}')"

    def to_dict(self):
        return {
            'comment_id': self.comment_id,
            'thread_id': self.thread_id,
            'content_unformatted': self.content_unformatted,
            'posted': self.posted.isoformat() if self.posted else None,
            'updated': self.updated.isoformat() if self.updated else None,
            'poster_username': self.poster_username,
            'poster_user_id': self.poster_user_id,
            'poster_avatar': self.poster_avatar,
            'status': self.status,
            'is_editable': self.is_editable,
            'is_liked': self.is_liked,
            'can_like': self.can_like,
            'can_reply': self.can_reply,
            'reaction_counters': self.reaction_counters,
            'parent_id': self.parent_id,
            'children_count': self.children_count,
            'replied_to': self.replied_to,
        }
