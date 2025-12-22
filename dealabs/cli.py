"""
Command-line interface for dealabs-api.
Provides commands for fetching hot deals, monitoring deals, and viewing thread details.
"""
import time
import click
import requests
import json
import datetime
from dealabs import Dealabs
from dealabs.models import Deal, Thread, Comment


@click.group()
def main():
    """Dealabs API Client - Fetch deals, threads, and comments"""
    pass


@main.command()
@click.option('--page', default=0, type=int, help='Page number (default: 0)')
@click.option('--limit', default=25, type=int, help='Number of deals to fetch (default: 25)')
@click.option('--days', default=1, type=int, help='Number of days to look back (default: 1)')
def hots(page, limit, days):
    """Fetch and display hot deals."""
    try:
        dealabs = Dealabs()
        params = {
            'page': page,
            'limit': limit,
            'days': days
        }

        response = dealabs.get_hot_deals(params)
        deals_data = response.get('data', [])
        deals = [Deal(deal_data) for deal_data in deals_data]

        click.echo(f"\nFound {len(deals)} hot deals:\n")
        for deal in deals:
            click.echo(f"ID: {deal.thread_id}")
            click.echo(f"Title: {deal.title}")
            click.echo(f"Price: {deal.price}")
            click.echo(f"Merchant: {deal.merchant}")
            click.echo(f"Temperature: {deal.temperature}")
            click.echo(f"URL: {deal.url}")
            click.echo(f"Category: {deal.category}")
            click.echo("-" * 80)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command('get-thread')
@click.argument('thread_id', type=int, required=True)
@click.option('--json-output', is_flag=True, help='Output as JSON')
def get_thread(thread_id, json_output):
    """Fetch and display thread details."""
    try:
        dealabs = Dealabs()
        thread = dealabs.get_thread(thread_id)

        if json_output:
            click.echo(json.dumps(thread.to_dict(), indent=2))
        else:
            click.echo(f"\nThread Details:\n")
            click.echo(f"ID: {thread.thread_id}")
            click.echo(f"Title: {thread.title}")
            click.echo(f"Status: {thread.status}")
            click.echo(f"Type: {thread.type}")
            click.echo(f"Temperature: {thread.temperature_rating}")
            click.echo(f"Is Hot: {thread.is_hot}")
            click.echo(f"Comment Count: {thread.comment_count}")
            click.echo(f"Price: {thread.price_display or thread.price}")
            click.echo(f"Merchant: {thread.merchant_name}")
            click.echo(f"Poster: {thread.poster_username}")
            click.echo(f"Posted: {thread.submitted_at}")
            click.echo(f"URL: {thread.deal_uri}")
            if thread.shareable_link:
                click.echo(f"Share: {thread.shareable_link}")
            if thread.code:
                click.echo(f"Code: {thread.code}")
            if thread.description:
                click.echo(f"\nDescription:\n{thread.description}")
            click.echo("-" * 80)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command('get-comments')
@click.argument('thread_id', type=int, required=True)
@click.option('--page', default=0, type=int, help='Page number (default: 0)')
@click.option('--limit', default=50, type=int, help='Number of comments to fetch (default: 50)')
@click.option('--sort', default='new', type=click.Choice(['new', 'hot', 'old']), help='Comment ordering (default: new)')
@click.option('--json-output', is_flag=True, help='Output as JSON')
def get_comments(thread_id, page, limit, sort, json_output):
    """Fetch and display thread comments."""
    try:
        dealabs = Dealabs()
        params = {
            'page': page,
            'limit': limit,
            'order': sort
        }

        comments = dealabs.get_thread_comments(thread_id, params)

        if json_output:
            comments_dict = [comment.to_dict() for comment in comments]
            click.echo(json.dumps(comments_dict, indent=2))
        else:
            click.echo(f"\nFound {len(comments)} comments:\n")
            for comment in comments:
                indent = "  " * (1 if comment.parent_id else 0)
                click.echo(f"{indent}Comment ID: {comment.comment_id}")
                click.echo(f"{indent}Posted by: {comment.poster_username}")
                click.echo(f"{indent}Posted: {comment.posted}")
                if comment.content_unformatted:
                    # Truncate long comments for display
                    content = comment.content_unformatted[:200]
                    if len(comment.content_unformatted) > 200:
                        content += "..."
                    click.echo(f"{indent}Content: {content}")
                if comment.children_count > 0:
                    click.echo(f"{indent}Replies: {comment.children_count}")
                click.echo(f"{indent}" + "-" * 70)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.option('--webhook', required=True, help='Webhook URL to send deals to')
@click.option('--filter', 'filters', multiple=True, help='Filters to apply (can be specified multiple times)')
@click.option('--keywords', multiple=True, help='Keywords to match in deal titles (can be specified multiple times)')
@click.option('--categories', multiple=True, help='Categories to match (can be specified multiple times)')
@click.option('--interval', default=300, type=int, help='Scan interval in seconds (default: 300)')
@click.option('--min-age', default=300, type=int, help='Minimum age in seconds before processing (default: 300)')
@click.option('--min-temperature', default=50, type=int, help='Minimum temperature level before processing (default: 50)')
def monitor(webhook, filters, keywords, categories, interval, min_age, min_temperature):
    """Monitor new deals and send to webhook."""
    try:
        dealabs = Dealabs()
        last_processed_id = 0

        click.echo(f"Starting Dealabs monitor. Scanning every {interval} seconds...")
        click.echo(f"Keywords: {list(keywords) if keywords else 'None'}")
        click.echo(f"Categories: {list(categories) if categories else 'None'}")
        click.echo(f"Filters: {list(filters) if filters else 'None'}")
        click.echo(f"Webhook: {webhook}")
        click.echo("Press Ctrl+C to stop\n")

        while True:
            try:
                # Get new deals since last check
                params = {'page': 0, 'limit': 50}
                deals = dealabs.get_new_deals(params)
                deals = list(filter(lambda deal: deal.deal_type == 'deals', deals))

                # Sort deals by thread_id to ensure correct processing order
                deals.sort(key=lambda deal: deal.thread_id)

                # Determine the highest thread_id in the current batch
                current_batch_max_id = last_processed_id
                if deals:
                    current_batch_max_id = max(deal.thread_id for deal in deals)

                current_time = datetime.datetime.now(datetime.timezone.utc)

                for deal in deals:
                    # Only process deals newer than the last processed ID
                    if deal.thread_id <= last_processed_id:
                        continue

                    # Check if deal is old enough to process
                    if deal.created is None:
                        click.echo(f"Warning: Deal {deal.thread_id} has no valid creation time, skipping.", err=True)
                        continue

                    age_seconds = (current_time - deal.created).total_seconds()

                    if age_seconds < min_age:
                        # Deal is too recent, skip processing
                        continue

                    title = deal.title.lower() if deal.title else ''
                    category = deal.category.lower() if deal.category else ''

                    # Check for keyword or category match
                    keyword_match = any(kw.lower() in title for kw in keywords) if keywords else True
                    category_match = any(cat.lower() in category for cat in categories) if categories else True
                    temperature_match = deal.temperature >= min_temperature

                    if (keyword_match or category_match) and temperature_match:
                        # Prepare payload
                        payload = {
                            'title': deal.title,
                            'url': deal.url,
                            'price': deal.price,
                            'category': deal.category,
                            'merchant': deal.merchant,
                            'temperature': deal.temperature
                        }

                        # Send to webhook
                        try:
                            response = requests.post(
                                webhook,
                                data=json.dumps(payload),
                                headers={'Content-Type': 'application/json'}
                            )
                            if response.status_code == 200:
                                click.echo(f"Sent deal: {deal.title}")
                            else:
                                click.echo(f"Failed to send deal (Status {response.status_code}): {deal.title}", err=True)
                        except requests.exceptions.RequestException as e:
                            click.echo(f"Error sending to webhook: {e}", err=True)

                # Update last_processed_id for the next iteration
                last_processed_id = current_batch_max_id

                # Wait for next scan
                time.sleep(interval)

            except KeyboardInterrupt:
                click.echo("\nStopping monitor...")
                raise
            except Exception as e:
                click.echo(f"Error occurred: {e}", err=True)
                time.sleep(60)

    except KeyboardInterrupt:
        click.echo("\nMonitor stopped by user")
    except Exception as e:
        click.echo(f"Fatal error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    main()
