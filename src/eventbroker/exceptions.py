
class EventBrokerError(Exception):
    """Base exception for EventBroker Lite."""


class SubscriptionError(EventBrokerError):
    """Raised when subscription registration fails."""


class PublishError(EventBrokerError):
    """Raised when publishing fails."""
