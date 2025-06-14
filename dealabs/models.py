import datetime

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
        # Handle 'created' timestamp or datetime string
        created_value = data.get('created')
        if isinstance(created_value, (int, float)):
            self.created = datetime.datetime.fromtimestamp(created_value, tz=datetime.timezone.utc)
        elif isinstance(created_value, str):
            try:
                self.created = datetime.datetime.strptime(created_value, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                self.created = None # Or handle error as appropriate
        else:
            self.created = None

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
