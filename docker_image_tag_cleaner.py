from datetime import datetime, timedelta
import re
import docker


def extract_date_from_tag(tag):
    # Extract date from the tag using regex
    match = re.search(r'(\d{4}-\d{2}-\d{2})', tag)
    if match:
        try:
            return datetime.strptime(match.group(1), '%Y-%m-%d')
        except ValueError:
            return None
    return None


def is_tag_stale(full_image_name, days_old=30):
    if ':' not in full_image_name:
        return False  # skip malformed tag
    # _ is placeholder for the image name, for future user input functionality
    _, tag_name = full_image_name.split(':', 1)

    if tag_name.startswith("release-"):
        return False
    tag_date = extract_date_from_tag(tag_name)
    if tag_date:
        return datetime.now() - tag_date > timedelta(days=days_old)
    return False


def clean_stale_docker_images(dry_run=True):
    """using docker api to clean stale docker images
    the tags should be in the format 'tagname-YYYY-MM-DD'
    it will remove tags older than 30 days and ignore tags starting with 'release-'"""
    client = docker.from_env()
    images = client.images.list()
    for image in images:
        for tag in image.tags:
            if is_tag_stale(tag):
                if dry_run:
                    print(f"[Dry Run] Would remove: {tag}")
                else:
                    print(f"Removing stale tag: {tag}")
                    client.images.remove(tag, force=True)
    print("Stale tags cleaned up.")


if __name__ == "__main__":
    # Run the cleaner in dry run mode by default
    # To actually remove images, set function input to False

    # Optional functionalities to add: add user input for image_name and days_old
    # as well as a confirmation prompt before deletion and dry_run input

    # to be added logging functionality
    clean_stale_docker_images()