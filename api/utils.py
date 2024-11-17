from random import shuffle

from models import User


def generate_secret_santa_pairings(users: list[User]) -> dict[str, str]:
    """Generate secret santa pairings for a list of users."""
    user_emails = [user.email for user in users]
    shuffle(user_emails)

    return {user.email: user_emails[(index + 1) % len(user_emails)] for index, user in enumerate(users)}
