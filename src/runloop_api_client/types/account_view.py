# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AccountView", "Billing", "BillingAws", "BillingStripe"]


class BillingAws(BaseModel):
    """AWS Marketplace billing information."""

    customer_identifier: Optional[str] = None
    """The AWS account ID used for Marketplace billing (12-digit)."""

    license_arn: Optional[str] = None
    """The AWS Marketplace license ARN."""

    subscription_status: Optional[str] = None
    """The AWS Marketplace subscription status."""


class BillingStripe(BaseModel):
    """Stripe billing information."""

    active_subscription: Optional[str] = None
    """The active Stripe subscription ID."""

    customer_id: Optional[str] = None
    """The Stripe customer ID."""


class Billing(BaseModel):
    """The account billing information."""

    account_billing_type: Literal["STRIPE", "AWS_MARKETPLACE", "STRIPE_PROJECTS", "UNRECOGNIZED"]
    """The account billing type."""

    aws: Optional[BillingAws] = None
    """AWS Marketplace billing information."""

    stripe: Optional[BillingStripe] = None
    """Stripe billing information."""

    stripe_customer_id: Optional[str] = None
    """Deprecated: use stripe.customer_id."""


class AccountView(BaseModel):
    """Account information."""

    id: str
    """The account ID."""

    account_status: Literal[
        "ACCOUNT_STATUS_INVALID",
        "ACCOUNT_STATUS_ONBOARDING",
        "ACCOUNT_STATUS_ENABLED",
        "ACCOUNT_STATUS_DISABLED_BY_ADMIN",
        "ACCOUNT_STATUS_DISABLED_QUOTA_REACHED",
        "ACCOUNT_STATUS_TRIAL_CANCELLED",
        "ACCOUNT_STATUS_STRIPE_PENDING_RESOURCES",
        "UNRECOGNIZED",
    ]
    """The account status."""

    billing: Billing
    """The account billing information."""

    created_at: str
    """The account creation timestamp."""

    name: str
    """The account name."""

    tier: Literal[
        "ACCOUNT_TIER_INVALID",
        "ACCOUNT_TIER_BASIC",
        "ACCOUNT_TIER_PRO",
        "ACCOUNT_TIER_ENTERPRISE",
        "ACCOUNT_TIER_TRIAL",
        "UNRECOGNIZED",
    ]
    """The account tier."""

    account_billing_type: Optional[Literal["STRIPE", "AWS_MARKETPLACE", "STRIPE_PROJECTS", "UNRECOGNIZED"]] = None
    """Deprecated: use billing.account_billing_type."""

    active_subscription: Optional[str] = None
    """Deprecated: use billing.stripe.active_subscription."""

    external_billing_account_id: Optional[str] = None
    """Deprecated: use billing.aws.customer_identifier."""

    stripe_customer_id: Optional[str] = None
    """Deprecated: use billing.stripe.customer_id."""
