from backend.models.models import InternalOrderStatus


def map_raw_to_internal_status(raw_status: str) -> InternalOrderStatus:
    pending_states = {
        "new",
        "accepted",
        "pending_new",
        "accepted_for_bidding",
        "pending_cancel",
        "pending_replace",
    }

    if raw_status in pending_states:
        return InternalOrderStatus.PENDING

    if raw_status == "partially_filled":
        return InternalOrderStatus.PARTIALLY_FILLED

    if raw_status == "filled":
        return InternalOrderStatus.FILLED

    # treat cancellation and expiration as “done/terminal”
    if raw_status in {"canceled", "expired", "done_for_day", "replaced"}:
        return InternalOrderStatus.CANCELED

    # if Alpaca rejected it outright
    if raw_status == "rejected":
        return InternalOrderStatus.FAILED

    # anything else you treat as ‘pending’
    return InternalOrderStatus.PENDING
