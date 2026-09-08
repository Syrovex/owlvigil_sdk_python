# Generated from contracts/management-schemas.json; do not edit.
from __future__ import annotations

from typing import Any, Dict, List, Literal, TypedDict

class Envelope(TypedDict, total=False):
    code: str
    data: Any
    message: str
    request_id: str

class Deleted(TypedDict, total=False):
    deleted: bool

class Invitation(TypedDict, total=False):
    items: List[InvitationModel]
    page_info: PageInfo

class Member(TypedDict, total=False):
    items: List[MemberModel]
    page_info: PageInfo

class Role(TypedDict, total=False):
    items: List[RoleModel]
    page_info: PageInfo

class Team(TypedDict, total=False):
    items: List[TeamModel]
    page_info: PageInfo

class Invoice(TypedDict, total=False):
    items: List[InvoiceModel]
    page_info: PageInfo

class Order(TypedDict, total=False):
    items: List[OrderModel]
    page_info: PageInfo

class PaymentMethod(TypedDict, total=False):
    items: List[PaymentMethodModel]
    page_info: PageInfo

class Plan(TypedDict, total=False):
    items: List[PlanModel]
    page_info: PageInfo

class TopupPlan(TypedDict, total=False):
    items: List[TopupPlanModel]
    page_info: PageInfo

class Model(TypedDict, total=False):
    items: List[ModelModel]
    page_info: PageInfo

class RouteCandidate(TypedDict, total=False):
    items: List[RouteCandidateModel]
    page_info: PageInfo

class MemberSpendingLimit(TypedDict, total=False):
    items: List[MemberSpendingLimitModel]
    page_info: PageInfo

class ManagementModel(TypedDict, total=False):
    items: List[DTO]
    page_info: PageInfo

class AuditLog(TypedDict, total=False):
    items: List[AuditLogModel]
    page_info: PageInfo

class PayloadSummary(TypedDict, total=False):
    items: List[PayloadSummaryModel]
    page_info: PageInfo

class RequestLog(TypedDict, total=False):
    items: List[RequestLogModel]
    page_info: PageInfo

class Trace(TypedDict, total=False):
    items: List[TraceModel]
    page_info: PageInfo

class ManagementModelModel(TypedDict, total=False):
    items: List[DTOModel2]
    page_info: PageInfo

class Record(TypedDict, total=False):
    items: List[RecordModel]
    page_info: PageInfo

class Endpoint(TypedDict, total=False):
    items: List[EndpointModel]
    page_info: PageInfo

class EventType(TypedDict, total=False):
    items: List[EventTypeModel]
    page_info: PageInfo

class Event(TypedDict, total=False):
    items: List[EventModel]
    page_info: PageInfo

class ManagementModelModel2(TypedDict, total=False):
    items: List[DTOModel22]
    page_info: PageInfo

class PageInfo(TypedDict, total=False):
    has_more: bool
    next_cursor: str

class CreateInvitationRequest(TypedDict, total=False):
    email: str
    expires_in_hours: int
    role: str
    team_id: int

class CreateRoleRequest(TypedDict, total=False):
    description: str
    key: str
    name: str
    permissions: List[str]

class CreateTeamRequest(TypedDict, total=False):
    description: str
    monthly_budget_limit: float
    name: str

class InvitationModel(TypedDict, total=False):
    created_at: str
    email: str
    expires_at: str
    id: int
    invited_by: UserBrief
    invited_by_user_id: int
    project_id: int
    role: str
    status: str
    team_id: int
    token: str
    updated_at: str
    workspace_id: int

class InviteMemberRequest(TypedDict, total=False):
    email: str
    role: str
    team_id: int

class MemberModel(TypedDict, total=False):
    email: str
    id: int
    invitation_expires_at: str
    invitation_id: int
    invitation_token: str
    invited_by: str
    joined_at: str
    member_type: str
    name: str
    role: str
    status: str
    team: str
    team_id: int
    user: UserBrief
    user_id: int
    workspace_id: int

class MemberPermissions(TypedDict, total=False):
    effective: List[str]
    groups: List[PermissionGroup]
    role: str
    user_id: int
    workspace_id: int

class Permission(TypedDict, total=False):
    default: bool
    effective: bool
    id: str
    label: str
    override: str

class PermissionGroup(TypedDict, total=False):
    id: str
    label: str
    permissions: List[Permission]

class PermissionGroups(TypedDict, total=False):
    groups: List[PermissionGroup]

class RoleModel(TypedDict, total=False):
    built_in: bool
    created_at: str
    description: str
    id: int
    key: str
    name: str
    permissions: List[str]
    scope_id: int
    scope_type: str
    updated_at: str

class RoleOption(TypedDict, total=False):
    enabled: bool
    label: str
    value: str

class RoleOptions(TypedDict, total=False):
    edit_roles: List[RoleOption]
    invite_roles: List[RoleOption]

class TeamModel(TypedDict, total=False):
    created_at: str
    deleted_at: str
    description: str
    id: int
    is_default: bool
    member_count: int
    monthly_budget_limit: float
    name: str
    project_id: int
    status: str
    updated_at: str
    workspace_id: int

class UpdateMemberRequest(TypedDict, total=False):
    role: str
    status: Literal['active', 'pending', 'suspended']
    team_id: int

class UpdatePermissionsRequest(TypedDict, total=False):
    permissions: Dict[str, Any]

class UpdateRoleRequest(TypedDict, total=False):
    description: str
    name: str
    permissions: List[str]

class UpdateTeamRequest(TypedDict, total=False):
    description: str
    monthly_budget_limit: float
    name: str

class UserBrief(TypedDict, total=False):
    email: str
    id: int
    name: str

class ChangePasswordRequest(TypedDict, total=False):
    new_password: str
    old_password: str

class InvitationModel2(TypedDict, total=False):
    converted_at: str
    created_at: str
    id: int
    invite_code: str
    invited_email: str
    invited_user_id: int
    inviter_user_id: int
    status: str

class InvitationSent(TypedDict, total=False):
    emails_sent: int
    message: str

class InvitationStats(TypedDict, total=False):
    conversion_rate: float
    converted_invitations: int
    invite_code: str
    invite_link: str
    pending_invitations: int
    total_invitations: int

class Message(TypedDict, total=False):
    message: str

class NotificationPreferences(TypedDict, total=False):
    billing: bool
    budget: bool
    marketing: bool
    reports: bool

class NotifyEmailEntry(TypedDict, total=False):
    disabled: bool
    email: str
    verified: bool

class Profile(TypedDict, total=False):
    avatar_url: str
    balance_notify_enabled: bool
    balance_notify_extra_emails: List[NotifyEmailEntry]
    balance_notify_threshold: float
    created_at: str
    default_workspace_id: int
    display_name: str
    email: str
    id: int
    name: str
    status: str
    updated_at: str
    user_id: int
    username: str

class SendInvitationRequest(TypedDict, total=False):
    emails: List[str]
    message: str

class SupportRequest(TypedDict, total=False):
    description: str
    issue_type: Literal['Technical Issue', 'Billing & Plan', 'Provider / Gateway Setup', 'Usage, Cost & Budget', 'Workspace & Team Access', 'Governance & Compliance', 'Bug Report', 'Other']
    subject: str

class UpdateProfileRequest(TypedDict, total=False):
    avatar_url: Any
    balance_notify_enabled: bool
    balance_notify_extra_emails: List[NotifyEmailEntry]
    balance_notify_threshold: Any
    default_workspace_id: int
    username: str

class AutoCharge(TypedDict, total=False):
    charge_amount: float
    configured: bool
    currency: str
    enabled: bool
    failure_reason: str
    payer_name: str
    payer_user_id: int
    payment_method: AutoChargePaymentMethod
    status: str
    threshold_amount: float
    workspace_id: int
    workspace_name: str

class AutoChargePaymentMethod(TypedDict, total=False):
    brand: str
    last4: str

class Balance(TypedDict, total=False):
    balance: float
    workspace_id: int

class BillingContact(TypedDict, total=False):
    address: str
    cc_recipients: List[str]
    email: str
    name: str
    phone: str
    tax_id: str

class CancelSubscriptionRequest(TypedDict, total=False):
    cancel_immediately: bool
    reason: str

class ChangeSubscriptionRequest(TypedDict, total=False):
    interval: str
    plan_id: str

class Checkout(TypedDict, total=False):
    amount: float
    checkout_url: str
    currency: str
    expires_at: str
    order_id: int
    order_type: str
    out_trade_no: str
    session_id: str
    status: str
    stripe_mode: str
    subscription: str
    workspace_id: int

class CheckoutConfirmation(TypedDict, total=False):
    balance: float
    order_id: int
    order_type: str
    status: str
    total_recharged: float
    workspace_id: int

class ConfirmStripeSessionRequest(TypedDict, total=False):
    session_id: str

class ConfirmSubscriptionRequest(TypedDict, total=False):
    plan_id: str
    stripe_subscription_id: str

class ConfirmTopupRequest(TypedDict, total=False):
    client_secret: str
    payment_intent_id: str

class Details(TypedDict, total=False):
    details: Dict[str, Any]
    workspace_id: int

class InAppPayment(TypedDict, total=False):
    amount: float
    balance: float
    client_secret: str
    currency: str
    message: str
    order_id: int
    order_type: str
    payment_intent_id: str
    status: str
    total_recharged: float
    workspace_id: int

class InvoiceModel(TypedDict, total=False):
    amount_due: float
    amount_paid: float
    created_at: str
    currency: str
    due_date: str
    hosted_invoice_url: str
    id: int
    invoice_number: str
    invoice_pdf_url: str
    paid_at: str
    period_end: str
    period_start: str
    status: str
    stripe_invoice_id: str
    updated_at: str
    workspace_id: int

class OrderModel(TypedDict, total=False):
    amount: float
    completed_at: str
    created_at: str
    currency: str
    expires_at: str
    failed_at: str
    failed_reason: str
    id: int
    order_type: str
    out_trade_no: str
    paid_at: str
    pay_amount: float
    pay_url: str
    payment_trade_no: str
    payment_type: str
    plan_id: int
    provider_snapshot: Dict[str, Any]
    receipt_url: str
    recharge_code: str
    source: str
    status: str
    stripe_payment_intent_id: str
    stripe_session_id: str
    updated_at: str
    user_id: int
    workspace_id: int

class Overview(TypedDict, total=False):
    balance: float
    billing_details: Dict[str, Any]
    current_month_cost: float
    current_month_requests: int
    current_month_tokens: int
    monthly_budget_limit: float
    recent_invoices: List[InvoiceModel]
    recent_invoices_page_info: PageInfoModel
    workspace_id: int

class PageInfoModel(TypedDict, total=False):
    has_more: bool
    next_cursor: str

class PaymentMethodModel(TypedDict, total=False):
    billing_email: str
    brand: str
    created_at: str
    expiry_month: int
    expiry_year: int
    id: str
    is_default: bool
    last4: str
    type: str

class PlanModel(TypedDict, total=False):
    created_at: str
    currency: str
    description: str
    feature_items: List[str]
    features: str
    for_sale: bool
    id: int
    is_public: bool
    max_api_keys: int
    max_members: int
    max_teams: int
    max_workspaces: int
    monthly_cost_quota: float
    monthly_request_quota: float
    name: str
    price_monthly: float
    price_yearly: float
    slug: str
    sort_order: int
    status: str
    stripe_price_id_monthly: str
    stripe_price_id_yearly: str
    trial_days: int
    updated_at: str

class RetryAutoChargeRequest(TypedDict, total=False):
    workspace_id: int

class SavePaymentMethodRequest(TypedDict, total=False):
    payment_method_id: str
    set_as_default: bool

class SetupIntent(TypedDict, total=False):
    client_secret: str
    setup_intent_id: str
    status: str

class SetupIntentRequest(TypedDict, total=False):
    workspace_id: int

class Subscription(TypedDict, total=False):
    can_create_more_workspaces: bool
    current_period_end: str
    current_period_start: str
    current_workspace_count: int
    effective_plan: PlanModel
    effective_subscription_plan_id: int
    effective_subscription_tier: str
    is_trial_expired: bool
    max_workspaces: int
    pending_plan_effective_at: str
    pending_plan_id: int
    plan: PlanModel
    stripe_customer_id: str
    stripe_schedule_id: str
    stripe_subscription_id: str
    subscription_cancel_at_period_end: bool
    subscription_plan_id: int
    subscription_status: str
    subscription_tier: str
    trial_ends_at: str
    user_id: int

class SubscriptionCheckout(TypedDict, total=False):
    checkout_url: str
    expires_at: str
    metadata: Dict[str, Any]
    order_id: int
    session_id: str
    status: str

class SubscriptionCheckoutRequest(TypedDict, total=False):
    cancel_url: str
    interval: str
    plan_id: str
    success_url: str

class SubscriptionInApp(TypedDict, total=False):
    amount: float
    client_secret: str
    currency: str
    payment_intent_id: str
    status: str
    stripe_subscription_id: str

class SubscriptionInAppRequest(TypedDict, total=False):
    interval: str
    plan_id: str
    return_url: str

class TopupCheckoutRequest(TypedDict, total=False):
    amount: float
    cancel_url: str
    success_url: str
    topup_plan_id: str
    workspace_id: int

class TopupInAppRequest(TypedDict, total=False):
    amount: float
    return_url: str
    topup_plan_id: str
    workspace_id: int

class TopupPlanModel(TypedDict, total=False):
    currency: str
    custom_amount: bool
    fee_rate: float
    id: str
    max_amount: float
    min_amount: float
    name: str
    payment_channels: List[str]

class UpdateAutoChargeRequest(TypedDict, total=False):
    charge_amount: float
    enabled: bool
    transfer_payer: bool
    workspace_id: int

class UpdateDetailsRequest(TypedDict, total=False):
    address: str
    billing_details: BillingContact
    cc_recipients: List[str]
    email: str
    name: str
    phone: str
    tax_id: str

class ModelModel(TypedDict, total=False):
    created_at: str
    developer: str
    group: str
    icon: str
    id: int
    model_id: str
    name: str
    route_count: int
    status: str
    type: str
    updated_at: str

class ModelDetail(TypedDict, total=False):
    created_at: str
    developer: str
    group: str
    icon: str
    id: int
    model_card: Any
    model_id: str
    name: str
    route_count: int
    routes: List[RouteCandidateModel]
    status: str
    type: str
    updated_at: str

class Preview(TypedDict, total=False):
    candidate_count: int
    candidates: List[RouteCandidateModel]
    model: str
    preview_metadata: Dict[str, Any]
    workspace_id: int

class PreviewRequest(TypedDict, total=False):
    key_id: int
    metadata: Dict[str, Any]
    model: str
    workspace_id: int

class RouteCandidateModel(TypedDict, total=False):
    actual_model: str
    channel_id: int
    channel_name: str
    channel_status: str
    channel_type: str
    id: int
    match_source: str
    model: str
    price: Any
    price_reference_id: str
    provider_platform: str
    provider_source: str
    route_id: str
    workspace_id: int

class BudgetCap(TypedDict, total=False):
    api_key_id: int
    current_spend: float
    email: str
    enabled: bool
    monthly_amount: float
    name: str
    scope_id: int
    scope_type: str
    team_id: int
    user_id: int

class Governance(TypedDict, total=False):
    currency: str
    exceeded_action: str
    gateway_key_caps: List[BudgetCap]
    member_caps: List[BudgetCap]
    member_limits: List[MemberSpendingLimitModel]
    notification_channels: List[str]
    team_caps: List[BudgetCap]
    thresholds: Thresholds
    usage_multiplier: float
    workspace_cap: BudgetCap
    workspace_id: int

class MemberSpendingLimitModel(TypedDict, total=False):
    daily_limit: float
    daily_spend: float
    email: str
    monthly_limit: float
    monthly_spend: float
    name: str
    user_id: int
    weekly_limit: float
    weekly_spend: float

class PreviewModel(TypedDict, total=False):
    affected_gateway_keys: List[int]
    affected_members: List[int]
    affected_teams: List[int]
    valid: bool
    violations: List[str]

class PreviewRequestModel(TypedDict, total=False):
    gateway_key_caps: List[BudgetCap]
    member_caps: List[BudgetCap]
    team_caps: List[BudgetCap]
    workspace_cap: BudgetCap

class SpendDetail(TypedDict, total=False):
    limit: float
    name: str
    percent: float
    scope_id: int
    scope_type: str
    spend: float
    status: str

class SpendSummary(TypedDict, total=False):
    current_period: str
    gateway_key_spends: List[SpendDetail]
    member_spends: List[SpendDetail]
    team_spends: List[SpendDetail]
    workspace_id: int
    workspace_spend: SpendDetail

class Thresholds(TypedDict, total=False):
    critical_percent: float
    exceeded_action: str
    warning_percent: float

class UpdateBudgetCapsRequest(TypedDict, total=False):
    gateway_key_caps: List[BudgetCap]
    member_caps: List[BudgetCap]
    team_caps: List[BudgetCap]
    workspace_cap: BudgetCap

class UpdateGovernanceRequest(TypedDict, total=False):
    exceeded_action: str
    gateway_key_caps: List[BudgetCap]
    member_caps: List[BudgetCap]
    member_limits: List[MemberSpendingLimitModel]
    team_caps: List[BudgetCap]
    thresholds: Thresholds
    usage_multiplier: float
    workspace_cap: BudgetCap

class UpdateScopeBudgetCapRequest(TypedDict, total=False):
    enabled: bool
    monthly_amount: float

class UpdateSpendingLimitsRequest(TypedDict, total=False):
    limits: List[MemberSpendingLimitModel]

class UpdateThresholdsRequest(TypedDict, total=False):
    critical_percent: float
    exceeded_action: str
    warning_percent: float

class UpdateUserSpendingLimitRequest(TypedDict, total=False):
    daily_limit: float
    monthly_limit: float
    weekly_limit: float

class CreateRequest(TypedDict, total=False):
    assignee_user_id: int
    budget_limit: float
    name: str
    provider_platform: str
    provider_source: str
    rate_limit_rpm: int
    team_id: int
    usage_multiplier: float
    workspace_id: int

class DTO(TypedDict, total=False):
    assignee_user_id: int
    created_at: str
    id: int
    key: str
    masked_key: str
    name: str
    provider_platform: str
    provider_source: str
    rate_limit_rpm: int
    status: str
    team_id: int
    updated_at: str
    usage_multiplier: float
    workspace_id: int

class UpdateRequest(TypedDict, total=False):
    assignee_user_id: int
    budget_limit: float
    clear_assignee_user_id: bool
    clear_team_id: bool
    name: str
    provider_platform: str
    provider_source: str
    rate_limit_rpm: int
    team_id: int
    usage_multiplier: float

class AuditLogModel(TypedDict, total=False):
    action: str
    actor_label: str
    after_state: Dict[str, Any]
    before_after_summary: str
    before_state: Dict[str, Any]
    created_at: str
    error_message: str
    id: int
    ip_address: str
    metadata: Dict[str, Any]
    resource_id: str
    resource_name: str
    resource_type: str
    status: str
    target_label: str
    user_agent: str
    user_email: str
    user_id: int
    user_name: str
    workspace_id: int

class LogDataQuota(TypedDict, total=False):
    cleanup_recommended: bool
    deleted_bytes: int
    deleted_objects: int
    last_calculated_at: str
    last_error: str
    limit_bytes: int
    over_limit: bool
    usage_percent: float
    used_bytes: int
    warning: bool

class LoggingSettings(TypedDict, total=False):
    capture_headers: bool
    capture_request_body: bool
    capture_response_body: bool
    capture_stream_chunks: bool
    enabled: bool
    log_data_quota: LogDataQuota
    mask_sensitive_headers: bool
    max_body_size: int
    redact_headers: List[str]
    retention_days: int

class Payload(TypedDict, total=False):
    api_key_id: int
    channel_id: int
    client_ip: str
    created_at: str
    duration_ms: int
    executions: List[PayloadExecution]
    external_id: str
    first_token_ms: int
    format: str
    id: int
    model: str
    reasoning_duration_ms: int
    request_body: Any
    request_id: str
    response_body: Any
    response_chunks: Any
    status: str
    stream: bool
    trace_id: int
    trace_key: str
    updated_at: str
    workspace_id: int

class PayloadAccess(TypedDict, total=False):
    capture_request_body: bool
    capture_response_body: bool
    capture_stream_chunks: bool
    enabled: bool
    message: str
    request_disabled_message: str
    response_disabled_message: str

class PayloadExecution(TypedDict, total=False):
    channel_id: int
    created_at: str
    error_message: str
    external_id: str
    format: str
    id: int
    model: str
    request_body: Any
    response_body: Any
    response_chunks: Any
    status: str
    status_code: int
    stream: bool
    updated_at: str

class PayloadSummaryModel(TypedDict, total=False):
    created_at: str
    format: str
    id: int
    model: str
    request_id: str
    status: str
    stream: bool
    trace_id: int
    trace_key: str
    workspace_id: int

class UpdateLoggingSettingsRequest(TypedDict, total=False):
    capture_headers: bool
    capture_request_body: bool
    capture_response_body: bool
    capture_stream_chunks: bool
    enabled: bool
    mask_sensitive_headers: bool
    max_body_size: int
    redact_headers: List[str]
    retention_days: int

class RequestLogModel(TypedDict, total=False):
    created_at: str
    format: str
    gateway_key_id: int
    id: int
    input_tokens: int
    key_name: str
    latency_ms: int
    member_name: str
    model: str
    output_tokens: int
    provider: str
    provider_id: int
    provider_source: str
    request_id: str
    status: str
    status_code: int
    stream: bool
    team_id: int
    team_name: str
    total_cost: float
    total_tokens: int
    trace_id: str
    user_id: int
    workspace_id: int

class TraceModel(TypedDict, total=False):
    created_at: str
    id: int
    thread_id: int
    trace_id: str
    updated_at: str
    workspace_id: int

class AddKeywordRequest(TypedDict, total=False):
    description: str
    enabled: bool
    keyword: str
    workspace_id: int

class BudgetPolicy(TypedDict, total=False):
    current_spend: float
    enforcement_mode: str
    id: int
    monthly_limit: float
    scope: str
    scope_id: int

class DTOModel(TypedDict, total=False):
    budget_policies: List[BudgetPolicy]
    key_id: int
    keyword_policies: List[KeywordPolicy]
    log_policies: List[LogPolicy]
    model_policies: List[ModelPolicy]
    rate_limits: List[RateLimit]
    warnings: List[str]
    workspace_id: int

class KeywordPolicy(TypedDict, total=False):
    action: str
    description: str
    enabled: bool
    id: int
    keyword: str
    scope: str

class LogPolicy(TypedDict, total=False):
    capture_request: bool
    capture_response: bool
    id: int
    retention_days: int
    scope: str

class ModelPolicy(TypedDict, total=False):
    action: str
    applies_to: List[str]
    id: int
    model_id: str
    priority: int
    provider: str
    reason: str
    redirect_to: str
    scope: str

class PreviewModel2(TypedDict, total=False):
    allowed: bool
    blocked_by: List[str]
    budget_check: str
    modified_by: List[str]
    rate_limit_check: str
    redirected_to: str
    warnings: List[str]

class PreviewRequestModel2(TypedDict, total=False):
    key_id: int
    model: str
    request: Dict[str, Any]
    workspace_id: int

class RateLimit(TypedDict, total=False):
    enforcement_mode: str
    id: int
    requests_per_min: int
    scope: str
    tokens_per_min: int

class UpdateRequestModel(TypedDict, total=False):
    action: str
    enabled: bool
    priority: int
    redirect_to: str

class CreateRequestModel(TypedDict, total=False):
    api_key: str
    api_mode: str
    base_url: str
    default_model: str
    name: str
    type: str
    workspace_id: int

class DTOModel2(TypedDict, total=False):
    api_mode: str
    base_url: str
    created_at: str
    default_model: str
    error_count: int
    id: int
    is_platform_managed: bool
    last_used_at: str
    name: str
    provider_platform: str
    provider_source: str
    request_count: int
    status: str
    type: str
    updated_at: str
    workspace_id: int

class UpdateRequestModel2(TypedDict, total=False):
    api_key: str
    api_mode: str
    base_url: str
    default_model: str
    name: str
    status: str
    workspace_id: int

class Verification(TypedDict, total=False):
    latency_ms: float
    message: str
    success: bool

class VerifyRequest(TypedDict, total=False):
    api_key: str
    api_mode: str
    base_url: str
    default_model: str
    provider_id: int
    type: str
    workspace_id: int

class Quota(TypedDict, total=False):
    limit: float
    remaining: float
    used: float

class RecordModel(TypedDict, total=False):
    cost: float
    id: str
    model: str
    provider: str
    requests: int
    timestamp: str
    tokens: int

class Summary(TypedDict, total=False):
    cost: float
    requests: int
    tokens: int

class BulkRedeliverRequest(TypedDict, total=False):
    endpoint_id: int
    event_ids: List[int]
    event_type: str
    limit: int
    workspace_id: int

class CreateEndpointRequest(TypedDict, total=False):
    event_types: List[Literal['billing.payment_failed', 'billing.invoice_available', 'quota.threshold_reached', 'workspace.member_added', 'gateway.key.created', 'gateway.key.updated']]
    url: str
    workspace_id: int

class EndpointModel(TypedDict, total=False):
    created_at: str
    event_types: List[str]
    id: int
    secret: str
    status: str
    updated_at: str
    url: str
    workspace_id: int

class EventModel(TypedDict, total=False):
    attempts: int
    created_at: str
    delivered_at: str
    endpoint_id: int
    event_type: str
    id: int
    last_error: str
    payload: Dict[str, Any]
    status: str
    updated_at: str
    workspace_id: int

class EventTypeModel(TypedDict, total=False):
    description: str
    type: str

class UpdateEndpointRequest(TypedDict, total=False):
    event_types: List[Literal['billing.payment_failed', 'billing.invoice_available', 'quota.threshold_reached', 'workspace.member_added', 'gateway.key.created', 'gateway.key.updated']]
    status: Literal['enabled', 'disabled']
    url: str

class Activity(TypedDict, total=False):
    created_at: str
    id: int
    ip: str
    meta: str
    tab: str
    what: str
    who: str

class Breakdown(TypedDict, total=False):
    by_member: List[BreakdownRow]
    by_provider: List[BreakdownRow]
    by_team: List[BreakdownRow]

class BreakdownRow(TypedDict, total=False):
    cost: float
    id: int
    key_count: int
    member_count: int
    name: str
    request_count: int
    token_label: str
    token_used: int

class CostSummary(TypedDict, total=False):
    budget: float
    current: float
    percent: int
    weekly_budget: float
    weekly_current: float

class CreateRequestModel2(TypedDict, total=False):
    description: str
    name: str
    region: str
    slug: str
    type: str

class DTOModel22(TypedDict, total=False):
    created_at: str
    description: str
    id: int
    name: str
    region: str
    role: str
    slug: str
    status: str
    type: str
    updated_at: str
    workspace_id: int

class MetricAnalysis(TypedDict, total=False):
    by_member: List[Dict[str, Any]]
    by_provider: List[Dict[str, Any]]
    by_team: List[Dict[str, Any]]
    series: SeriesCatalog
    total: List[Dict[str, Any]]

class OverviewModel(TypedDict, total=False):
    breakdown: Breakdown
    cost_analysis: MetricAnalysis
    range: str
    recent_activity: OverviewRecentActivity
    summary: OverviewSummary
    usage_analysis: MetricAnalysis

class OverviewAuditLog(TypedDict, total=False):
    action: str
    after: str
    before: str
    created_at: str
    id: int
    ip_address: str
    resource_name: str
    resource_type: str
    status: str
    user_name: str

class OverviewRecentActivity(TypedDict, total=False):
    audit_logs: List[OverviewAuditLog]
    audit_logs_available: bool
    request_logs: List[OverviewRequestLog]

class OverviewRequestLog(TypedDict, total=False):
    created_at: str
    id: int
    input_tokens: int
    key_name: str
    latency_ms: int
    member: str
    model: str
    output_tokens: int
    provider: str
    status: str
    status_code: int
    team: str
    total_cost: float
    total_tokens: int
    trace_id: str

class OverviewSummary(TypedDict, total=False):
    cost: CostSummary
    resources: ResourceSummary
    system_status: SystemStatus
    token_usage: TokenSummary

class QuotaCounter(TypedDict, total=False):
    limit: int
    used: int

class QuotaItem(TypedDict, total=False):
    key: str
    label: str
    limit: int
    unit: str
    used: int

class QuotaPlan(TypedDict, total=False):
    name: str
    quotas: Dict[str, Any]
    slug: str

class QuotaSummary(TypedDict, total=False):
    items: List[QuotaItem]
    plan: QuotaPlan
    workspace_id: int

class QuotaUsage(TypedDict, total=False):
    api_keys: QuotaCounter
    members: QuotaCounter
    teams: QuotaCounter

class ResourceSummary(TypedDict, total=False):
    active_keys: int
    members: int
    providers: int
    teams: int

class SeriesCatalog(TypedDict, total=False):
    members: List[str]
    providers: List[str]
    teams: List[str]

class SystemStatus(TypedDict, total=False):
    avg_latency_ms: int
    health_pct: int
    success_rate: float
    tone: str

class TokenSummary(TypedDict, total=False):
    current: int
    label: str
    weekly_current: int
    weekly_label: str

class UpdateRequestModel22(TypedDict, total=False):
    description: str
    name: str

ManagementSchema = Dict[str, Any]

__all__ = [
    'Envelope',
    'Deleted',
    'Invitation',
    'Member',
    'Role',
    'Team',
    'Invoice',
    'Order',
    'PaymentMethod',
    'Plan',
    'TopupPlan',
    'Model',
    'RouteCandidate',
    'MemberSpendingLimit',
    'ManagementModel',
    'AuditLog',
    'PayloadSummary',
    'RequestLog',
    'Trace',
    'ManagementModelModel',
    'Record',
    'Endpoint',
    'EventType',
    'Event',
    'ManagementModelModel2',
    'PageInfo',
    'CreateInvitationRequest',
    'CreateRoleRequest',
    'CreateTeamRequest',
    'InvitationModel',
    'InviteMemberRequest',
    'MemberModel',
    'MemberPermissions',
    'Permission',
    'PermissionGroup',
    'PermissionGroups',
    'RoleModel',
    'RoleOption',
    'RoleOptions',
    'TeamModel',
    'UpdateMemberRequest',
    'UpdatePermissionsRequest',
    'UpdateRoleRequest',
    'UpdateTeamRequest',
    'UserBrief',
    'ChangePasswordRequest',
    'InvitationModel2',
    'InvitationSent',
    'InvitationStats',
    'Message',
    'NotificationPreferences',
    'NotifyEmailEntry',
    'Profile',
    'SendInvitationRequest',
    'SupportRequest',
    'UpdateProfileRequest',
    'AutoCharge',
    'AutoChargePaymentMethod',
    'Balance',
    'BillingContact',
    'CancelSubscriptionRequest',
    'ChangeSubscriptionRequest',
    'Checkout',
    'CheckoutConfirmation',
    'ConfirmStripeSessionRequest',
    'ConfirmSubscriptionRequest',
    'ConfirmTopupRequest',
    'Details',
    'InAppPayment',
    'InvoiceModel',
    'OrderModel',
    'Overview',
    'PageInfoModel',
    'PaymentMethodModel',
    'PlanModel',
    'RetryAutoChargeRequest',
    'SavePaymentMethodRequest',
    'SetupIntent',
    'SetupIntentRequest',
    'Subscription',
    'SubscriptionCheckout',
    'SubscriptionCheckoutRequest',
    'SubscriptionInApp',
    'SubscriptionInAppRequest',
    'TopupCheckoutRequest',
    'TopupInAppRequest',
    'TopupPlanModel',
    'UpdateAutoChargeRequest',
    'UpdateDetailsRequest',
    'ModelModel',
    'ModelDetail',
    'Preview',
    'PreviewRequest',
    'RouteCandidateModel',
    'BudgetCap',
    'Governance',
    'MemberSpendingLimitModel',
    'PreviewModel',
    'PreviewRequestModel',
    'SpendDetail',
    'SpendSummary',
    'Thresholds',
    'UpdateBudgetCapsRequest',
    'UpdateGovernanceRequest',
    'UpdateScopeBudgetCapRequest',
    'UpdateSpendingLimitsRequest',
    'UpdateThresholdsRequest',
    'UpdateUserSpendingLimitRequest',
    'CreateRequest',
    'DTO',
    'UpdateRequest',
    'AuditLogModel',
    'LogDataQuota',
    'LoggingSettings',
    'Payload',
    'PayloadAccess',
    'PayloadExecution',
    'PayloadSummaryModel',
    'UpdateLoggingSettingsRequest',
    'RequestLogModel',
    'TraceModel',
    'AddKeywordRequest',
    'BudgetPolicy',
    'DTOModel',
    'KeywordPolicy',
    'LogPolicy',
    'ModelPolicy',
    'PreviewModel2',
    'PreviewRequestModel2',
    'RateLimit',
    'UpdateRequestModel',
    'CreateRequestModel',
    'DTOModel2',
    'UpdateRequestModel2',
    'Verification',
    'VerifyRequest',
    'Quota',
    'RecordModel',
    'Summary',
    'BulkRedeliverRequest',
    'CreateEndpointRequest',
    'EndpointModel',
    'EventModel',
    'EventTypeModel',
    'UpdateEndpointRequest',
    'Activity',
    'Breakdown',
    'BreakdownRow',
    'CostSummary',
    'CreateRequestModel2',
    'DTOModel22',
    'MetricAnalysis',
    'OverviewModel',
    'OverviewAuditLog',
    'OverviewRecentActivity',
    'OverviewRequestLog',
    'OverviewSummary',
    'QuotaCounter',
    'QuotaItem',
    'QuotaPlan',
    'QuotaSummary',
    'QuotaUsage',
    'ResourceSummary',
    'SeriesCatalog',
    'SystemStatus',
    'TokenSummary',
    'UpdateRequestModel22',
    'ManagementSchema',
]