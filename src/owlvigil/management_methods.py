# Generated from contracts/management-contract.json; do not edit.
from __future__ import annotations

from typing import Any, Optional

from ._core import ApiResponse, ManagementOperationRequest


class GeneratedManagementMethods:
    def get_billing_auto_charge(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_auto-charge', request)

    def put_billing_auto_charge(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_billing_auto-charge', request)

    def post_billing_auto_charge_retry(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_auto-charge_retry', request)

    def get_billing_balance(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_balance', request)

    def get_billing_invoices(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_invoices', request)

    def get_billing_invoices_invoice_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_invoices_invoice_id', request)

    def get_billing_orders(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_orders', request)

    def get_billing_orders_order_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_orders_order_id', request)

    def post_billing_orders_order_id_confirm_stripe_session(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_orders_order_id_confirm-stripe-session', request)

    def get_billing_overview(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_overview', request)

    def get_billing_payment_methods(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_payment-methods', request)

    def post_billing_payment_methods(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_payment-methods', request)

    def post_billing_payment_methods_setup_intent(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_payment-methods_setup-intent', request)

    def delete_billing_payment_methods_payment_method_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('delete_billing_payment-methods_payment_method_id', request)

    def put_billing_payment_methods_payment_method_id_default(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_billing_payment-methods_payment_method_id_default', request)

    def get_billing_plans(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_plans', request)

    def get_billing_plans_plan_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_plans_plan_id', request)

    def get_billing_subscription(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_subscription', request)

    def post_billing_subscription_cancel(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_subscription_cancel', request)

    def post_billing_subscription_checkout(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_subscription_checkout', request)

    def post_billing_subscription_checkout_sessions_sync_latest(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_subscription_checkout-sessions_sync-latest', request)

    def get_billing_subscription_checkout_sessions_session_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_subscription_checkout-sessions_session_id', request)

    def post_billing_subscription_downgrade(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_subscription_downgrade', request)

    def post_billing_subscription_in_app(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_subscription_in-app', request)

    def post_billing_subscription_in_app_confirm(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_subscription_in-app_confirm', request)

    def post_billing_subscription_reactivate(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_subscription_reactivate', request)

    def post_billing_subscription_upgrade(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_subscription_upgrade', request)

    def get_billing_topup_plans(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_topup-plans', request)

    def get_billing_topups(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_topups', request)

    def post_billing_topups_checkout(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_topups_checkout', request)

    def post_billing_topups_in_app(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_topups_in-app', request)

    def post_billing_topups_in_app_confirm(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_billing_topups_in-app_confirm', request)

    def get_billing_topups_topup_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_billing_topups_topup_id', request)

    def get_gateway_keys(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_keys', request)

    def post_gateway_keys(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_gateway_keys', request)

    def delete_gateway_keys_key_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('delete_gateway_keys_key_id', request)

    def get_gateway_keys_key_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_keys_key_id', request)

    def patch_gateway_keys_key_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('patch_gateway_keys_key_id', request)

    def post_gateway_keys_key_id_disable(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_gateway_keys_key_id_disable', request)

    def post_gateway_keys_key_id_enable(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_gateway_keys_key_id_enable', request)

    def post_gateway_keys_key_id_rotate(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_gateway_keys_key_id_rotate', request)

    def get_gateway_models(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_models', request)

    def get_gateway_models_model_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_models_model_id', request)

    def get_gateway_payload_logs(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_payload-logs', request)

    def get_gateway_payload_logs_access(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_payload-logs_access', request)

    def get_gateway_payload_logs_payload_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_payload-logs_payload_id', request)

    def get_gateway_policies(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_policies', request)

    def post_gateway_policies_keywords(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_gateway_policies_keywords', request)

    def delete_gateway_policies_keywords_keyword_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('delete_gateway_policies_keywords_keyword_id', request)

    def post_gateway_policies_preview(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_gateway_policies_preview', request)

    def patch_gateway_policies_policy_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('patch_gateway_policies_policy_id', request)

    def get_gateway_providers(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_providers', request)

    def post_gateway_providers(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_gateway_providers', request)

    def post_gateway_providers_verify_connection(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_gateway_providers_verify-connection', request)

    def delete_gateway_providers_provider_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('delete_gateway_providers_provider_id', request)

    def get_gateway_providers_provider_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_providers_provider_id', request)

    def patch_gateway_providers_provider_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('patch_gateway_providers_provider_id', request)

    def get_gateway_quota(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_quota', request)

    def get_gateway_request_logs(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_request-logs', request)

    def get_gateway_request_logs_request_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_request-logs_request_id', request)

    def get_gateway_routes(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_routes', request)

    def post_gateway_routes_preview(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_gateway_routes_preview', request)

    def get_gateway_routes_route_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_routes_route_id', request)

    def get_gateway_traces(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_traces', request)

    def get_gateway_traces_trace_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_traces_trace_id', request)

    def get_gateway_usage(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_usage', request)

    def get_gateway_usage_summary(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_gateway_usage_summary', request)

    def get_user_notification_preferences(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_user_notification-preferences', request)

    def put_user_notification_preferences(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_user_notification-preferences', request)

    def put_user_password(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_user_password', request)

    def get_user_profile(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_user_profile', request)

    def put_user_profile(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_user_profile', request)

    def post_user_support_requests(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_user_support-requests', request)

    def get_users_me_invitation_stats(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_users_me_invitation-stats', request)

    def get_users_me_invitations(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_users_me_invitations', request)

    def get_users_me_invite_link(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_users_me_invite-link', request)

    def post_users_me_send_invitation(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_users_me_send-invitation', request)

    def get_webhook_endpoints(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_webhook-endpoints', request)

    def post_webhook_endpoints(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_webhook-endpoints', request)

    def delete_webhook_endpoints_endpoint_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('delete_webhook-endpoints_endpoint_id', request)

    def get_webhook_endpoints_endpoint_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_webhook-endpoints_endpoint_id', request)

    def patch_webhook_endpoints_endpoint_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('patch_webhook-endpoints_endpoint_id', request)

    def post_webhook_endpoints_endpoint_id_disable(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_webhook-endpoints_endpoint_id_disable', request)

    def post_webhook_endpoints_endpoint_id_enable(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_webhook-endpoints_endpoint_id_enable', request)

    def get_webhook_endpoints_endpoint_id_events(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_webhook-endpoints_endpoint_id_events', request)

    def post_webhook_endpoints_endpoint_id_rotate_secret(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_webhook-endpoints_endpoint_id_rotate-secret', request)

    def post_webhook_endpoints_endpoint_id_test(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_webhook-endpoints_endpoint_id_test', request)

    def get_webhook_event_types(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_webhook-event-types', request)

    def get_webhook_events(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_webhook-events', request)

    def post_webhook_events_bulk_redeliver(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_webhook-events_bulk-redeliver', request)

    def get_webhook_events_event_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_webhook-events_event_id', request)

    def post_webhook_events_event_id_redeliver(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_webhook-events_event_id_redeliver', request)

    def post_webhook_events_event_id_retry(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_webhook-events_event_id_retry', request)

    def get_workspaces(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces', request)

    def post_workspaces(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_workspaces', request)

    def delete_workspaces_workspace_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('delete_workspaces_workspace_id', request)

    def get_workspaces_workspace_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id', request)

    def patch_workspaces_workspace_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('patch_workspaces_workspace_id', request)

    def get_workspaces_workspace_id_activity(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_activity', request)

    def get_workspaces_workspace_id_audit_logs(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_audit-logs', request)

    def get_workspaces_workspace_id_audit_logs_audit_log_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_audit-logs_audit_log_id', request)

    def get_workspaces_workspace_id_billing_details(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_billing-details', request)

    def put_workspaces_workspace_id_billing_details(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_workspaces_workspace_id_billing-details', request)

    def get_workspaces_workspace_id_governance_financial(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_governance_financial', request)

    def put_workspaces_workspace_id_governance_financial(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_workspaces_workspace_id_governance_financial', request)

    def get_workspaces_workspace_id_governance_financial_budget_caps(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_governance_financial_budget-caps', request)

    def put_workspaces_workspace_id_governance_financial_budget_caps(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_workspaces_workspace_id_governance_financial_budget-caps', request)

    def patch_workspaces_workspace_id_governance_financial_budget_caps_scope_type_scope_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('patch_workspaces_workspace_id_governance_financial_budget-caps_scope_type_scope_id', request)

    def post_workspaces_workspace_id_governance_financial_preview(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_workspaces_workspace_id_governance_financial_preview', request)

    def get_workspaces_workspace_id_governance_financial_spend_summary(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_governance_financial_spend-summary', request)

    def get_workspaces_workspace_id_governance_financial_spending_limits(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_governance_financial_spending-limits', request)

    def put_workspaces_workspace_id_governance_financial_spending_limits(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_workspaces_workspace_id_governance_financial_spending-limits', request)

    def patch_workspaces_workspace_id_governance_financial_spending_limits_users_user_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('patch_workspaces_workspace_id_governance_financial_spending-limits_users_user_id', request)

    def get_workspaces_workspace_id_governance_financial_thresholds(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_governance_financial_thresholds', request)

    def put_workspaces_workspace_id_governance_financial_thresholds(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_workspaces_workspace_id_governance_financial_thresholds', request)

    def get_workspaces_workspace_id_invitations(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_invitations', request)

    def post_workspaces_workspace_id_invitations(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_workspaces_workspace_id_invitations', request)

    def post_workspaces_workspace_id_invitations_invitation_id_resend(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_workspaces_workspace_id_invitations_invitation_id_resend', request)

    def post_workspaces_workspace_id_invitations_invitation_id_revoke(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_workspaces_workspace_id_invitations_invitation_id_revoke', request)

    def get_workspaces_workspace_id_logging_settings(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_logging-settings', request)

    def put_workspaces_workspace_id_logging_settings(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_workspaces_workspace_id_logging-settings', request)

    def get_workspaces_workspace_id_members(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_members', request)

    def post_workspaces_workspace_id_members(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_workspaces_workspace_id_members', request)

    def get_workspaces_workspace_id_members_role_options(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_members_role-options', request)

    def delete_workspaces_workspace_id_members_member_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('delete_workspaces_workspace_id_members_member_id', request)

    def get_workspaces_workspace_id_members_member_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_members_member_id', request)

    def patch_workspaces_workspace_id_members_member_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('patch_workspaces_workspace_id_members_member_id', request)

    def get_workspaces_workspace_id_members_member_id_permissions(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_members_member_id_permissions', request)

    def put_workspaces_workspace_id_members_member_id_permissions(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('put_workspaces_workspace_id_members_member_id_permissions', request)

    def post_workspaces_workspace_id_members_member_id_permissions_reset(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_workspaces_workspace_id_members_member_id_permissions_reset', request)

    def get_workspaces_workspace_id_overview(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_overview', request)

    def get_workspaces_workspace_id_permissions(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_permissions', request)

    def get_workspaces_workspace_id_quota_summary(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_quota-summary', request)

    def get_workspaces_workspace_id_quota_usage(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_quota-usage', request)

    def get_workspaces_workspace_id_roles(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_roles', request)

    def post_workspaces_workspace_id_roles(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_workspaces_workspace_id_roles', request)

    def delete_workspaces_workspace_id_roles_role_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('delete_workspaces_workspace_id_roles_role_id', request)

    def get_workspaces_workspace_id_roles_role_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_roles_role_id', request)

    def patch_workspaces_workspace_id_roles_role_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('patch_workspaces_workspace_id_roles_role_id', request)

    def get_workspaces_workspace_id_teams(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_teams', request)

    def post_workspaces_workspace_id_teams(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('post_workspaces_workspace_id_teams', request)

    def delete_workspaces_workspace_id_teams_team_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('delete_workspaces_workspace_id_teams_team_id', request)

    def get_workspaces_workspace_id_teams_team_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('get_workspaces_workspace_id_teams_team_id', request)

    def patch_workspaces_workspace_id_teams_team_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return self.open_api('patch_workspaces_workspace_id_teams_team_id', request)


class AsyncGeneratedManagementMethods:
    async def get_billing_auto_charge(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_auto-charge', request)

    async def put_billing_auto_charge(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_billing_auto-charge', request)

    async def post_billing_auto_charge_retry(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_auto-charge_retry', request)

    async def get_billing_balance(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_balance', request)

    async def get_billing_invoices(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_invoices', request)

    async def get_billing_invoices_invoice_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_invoices_invoice_id', request)

    async def get_billing_orders(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_orders', request)

    async def get_billing_orders_order_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_orders_order_id', request)

    async def post_billing_orders_order_id_confirm_stripe_session(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_orders_order_id_confirm-stripe-session', request)

    async def get_billing_overview(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_overview', request)

    async def get_billing_payment_methods(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_payment-methods', request)

    async def post_billing_payment_methods(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_payment-methods', request)

    async def post_billing_payment_methods_setup_intent(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_payment-methods_setup-intent', request)

    async def delete_billing_payment_methods_payment_method_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('delete_billing_payment-methods_payment_method_id', request)

    async def put_billing_payment_methods_payment_method_id_default(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_billing_payment-methods_payment_method_id_default', request)

    async def get_billing_plans(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_plans', request)

    async def get_billing_plans_plan_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_plans_plan_id', request)

    async def get_billing_subscription(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_subscription', request)

    async def post_billing_subscription_cancel(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_subscription_cancel', request)

    async def post_billing_subscription_checkout(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_subscription_checkout', request)

    async def post_billing_subscription_checkout_sessions_sync_latest(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_subscription_checkout-sessions_sync-latest', request)

    async def get_billing_subscription_checkout_sessions_session_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_subscription_checkout-sessions_session_id', request)

    async def post_billing_subscription_downgrade(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_subscription_downgrade', request)

    async def post_billing_subscription_in_app(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_subscription_in-app', request)

    async def post_billing_subscription_in_app_confirm(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_subscription_in-app_confirm', request)

    async def post_billing_subscription_reactivate(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_subscription_reactivate', request)

    async def post_billing_subscription_upgrade(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_subscription_upgrade', request)

    async def get_billing_topup_plans(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_topup-plans', request)

    async def get_billing_topups(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_topups', request)

    async def post_billing_topups_checkout(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_topups_checkout', request)

    async def post_billing_topups_in_app(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_topups_in-app', request)

    async def post_billing_topups_in_app_confirm(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_billing_topups_in-app_confirm', request)

    async def get_billing_topups_topup_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_billing_topups_topup_id', request)

    async def get_gateway_keys(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_keys', request)

    async def post_gateway_keys(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_gateway_keys', request)

    async def delete_gateway_keys_key_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('delete_gateway_keys_key_id', request)

    async def get_gateway_keys_key_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_keys_key_id', request)

    async def patch_gateway_keys_key_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('patch_gateway_keys_key_id', request)

    async def post_gateway_keys_key_id_disable(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_gateway_keys_key_id_disable', request)

    async def post_gateway_keys_key_id_enable(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_gateway_keys_key_id_enable', request)

    async def post_gateway_keys_key_id_rotate(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_gateway_keys_key_id_rotate', request)

    async def get_gateway_models(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_models', request)

    async def get_gateway_models_model_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_models_model_id', request)

    async def get_gateway_payload_logs(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_payload-logs', request)

    async def get_gateway_payload_logs_access(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_payload-logs_access', request)

    async def get_gateway_payload_logs_payload_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_payload-logs_payload_id', request)

    async def get_gateway_policies(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_policies', request)

    async def post_gateway_policies_keywords(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_gateway_policies_keywords', request)

    async def delete_gateway_policies_keywords_keyword_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('delete_gateway_policies_keywords_keyword_id', request)

    async def post_gateway_policies_preview(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_gateway_policies_preview', request)

    async def patch_gateway_policies_policy_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('patch_gateway_policies_policy_id', request)

    async def get_gateway_providers(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_providers', request)

    async def post_gateway_providers(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_gateway_providers', request)

    async def post_gateway_providers_verify_connection(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_gateway_providers_verify-connection', request)

    async def delete_gateway_providers_provider_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('delete_gateway_providers_provider_id', request)

    async def get_gateway_providers_provider_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_providers_provider_id', request)

    async def patch_gateway_providers_provider_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('patch_gateway_providers_provider_id', request)

    async def get_gateway_quota(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_quota', request)

    async def get_gateway_request_logs(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_request-logs', request)

    async def get_gateway_request_logs_request_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_request-logs_request_id', request)

    async def get_gateway_routes(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_routes', request)

    async def post_gateway_routes_preview(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_gateway_routes_preview', request)

    async def get_gateway_routes_route_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_routes_route_id', request)

    async def get_gateway_traces(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_traces', request)

    async def get_gateway_traces_trace_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_traces_trace_id', request)

    async def get_gateway_usage(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_usage', request)

    async def get_gateway_usage_summary(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_gateway_usage_summary', request)

    async def get_user_notification_preferences(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_user_notification-preferences', request)

    async def put_user_notification_preferences(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_user_notification-preferences', request)

    async def put_user_password(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_user_password', request)

    async def get_user_profile(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_user_profile', request)

    async def put_user_profile(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_user_profile', request)

    async def post_user_support_requests(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_user_support-requests', request)

    async def get_users_me_invitation_stats(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_users_me_invitation-stats', request)

    async def get_users_me_invitations(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_users_me_invitations', request)

    async def get_users_me_invite_link(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_users_me_invite-link', request)

    async def post_users_me_send_invitation(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_users_me_send-invitation', request)

    async def get_webhook_endpoints(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_webhook-endpoints', request)

    async def post_webhook_endpoints(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_webhook-endpoints', request)

    async def delete_webhook_endpoints_endpoint_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('delete_webhook-endpoints_endpoint_id', request)

    async def get_webhook_endpoints_endpoint_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_webhook-endpoints_endpoint_id', request)

    async def patch_webhook_endpoints_endpoint_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('patch_webhook-endpoints_endpoint_id', request)

    async def post_webhook_endpoints_endpoint_id_disable(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_webhook-endpoints_endpoint_id_disable', request)

    async def post_webhook_endpoints_endpoint_id_enable(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_webhook-endpoints_endpoint_id_enable', request)

    async def get_webhook_endpoints_endpoint_id_events(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_webhook-endpoints_endpoint_id_events', request)

    async def post_webhook_endpoints_endpoint_id_rotate_secret(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_webhook-endpoints_endpoint_id_rotate-secret', request)

    async def post_webhook_endpoints_endpoint_id_test(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_webhook-endpoints_endpoint_id_test', request)

    async def get_webhook_event_types(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_webhook-event-types', request)

    async def get_webhook_events(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_webhook-events', request)

    async def post_webhook_events_bulk_redeliver(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_webhook-events_bulk-redeliver', request)

    async def get_webhook_events_event_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_webhook-events_event_id', request)

    async def post_webhook_events_event_id_redeliver(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_webhook-events_event_id_redeliver', request)

    async def post_webhook_events_event_id_retry(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_webhook-events_event_id_retry', request)

    async def get_workspaces(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces', request)

    async def post_workspaces(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_workspaces', request)

    async def delete_workspaces_workspace_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('delete_workspaces_workspace_id', request)

    async def get_workspaces_workspace_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id', request)

    async def patch_workspaces_workspace_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('patch_workspaces_workspace_id', request)

    async def get_workspaces_workspace_id_activity(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_activity', request)

    async def get_workspaces_workspace_id_audit_logs(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_audit-logs', request)

    async def get_workspaces_workspace_id_audit_logs_audit_log_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_audit-logs_audit_log_id', request)

    async def get_workspaces_workspace_id_billing_details(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_billing-details', request)

    async def put_workspaces_workspace_id_billing_details(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_workspaces_workspace_id_billing-details', request)

    async def get_workspaces_workspace_id_governance_financial(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_governance_financial', request)

    async def put_workspaces_workspace_id_governance_financial(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_workspaces_workspace_id_governance_financial', request)

    async def get_workspaces_workspace_id_governance_financial_budget_caps(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_governance_financial_budget-caps', request)

    async def put_workspaces_workspace_id_governance_financial_budget_caps(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_workspaces_workspace_id_governance_financial_budget-caps', request)

    async def patch_workspaces_workspace_id_governance_financial_budget_caps_scope_type_scope_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('patch_workspaces_workspace_id_governance_financial_budget-caps_scope_type_scope_id', request)

    async def post_workspaces_workspace_id_governance_financial_preview(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_workspaces_workspace_id_governance_financial_preview', request)

    async def get_workspaces_workspace_id_governance_financial_spend_summary(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_governance_financial_spend-summary', request)

    async def get_workspaces_workspace_id_governance_financial_spending_limits(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_governance_financial_spending-limits', request)

    async def put_workspaces_workspace_id_governance_financial_spending_limits(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_workspaces_workspace_id_governance_financial_spending-limits', request)

    async def patch_workspaces_workspace_id_governance_financial_spending_limits_users_user_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('patch_workspaces_workspace_id_governance_financial_spending-limits_users_user_id', request)

    async def get_workspaces_workspace_id_governance_financial_thresholds(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_governance_financial_thresholds', request)

    async def put_workspaces_workspace_id_governance_financial_thresholds(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_workspaces_workspace_id_governance_financial_thresholds', request)

    async def get_workspaces_workspace_id_invitations(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_invitations', request)

    async def post_workspaces_workspace_id_invitations(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_workspaces_workspace_id_invitations', request)

    async def post_workspaces_workspace_id_invitations_invitation_id_resend(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_workspaces_workspace_id_invitations_invitation_id_resend', request)

    async def post_workspaces_workspace_id_invitations_invitation_id_revoke(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_workspaces_workspace_id_invitations_invitation_id_revoke', request)

    async def get_workspaces_workspace_id_logging_settings(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_logging-settings', request)

    async def put_workspaces_workspace_id_logging_settings(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_workspaces_workspace_id_logging-settings', request)

    async def get_workspaces_workspace_id_members(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_members', request)

    async def post_workspaces_workspace_id_members(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_workspaces_workspace_id_members', request)

    async def get_workspaces_workspace_id_members_role_options(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_members_role-options', request)

    async def delete_workspaces_workspace_id_members_member_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('delete_workspaces_workspace_id_members_member_id', request)

    async def get_workspaces_workspace_id_members_member_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_members_member_id', request)

    async def patch_workspaces_workspace_id_members_member_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('patch_workspaces_workspace_id_members_member_id', request)

    async def get_workspaces_workspace_id_members_member_id_permissions(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_members_member_id_permissions', request)

    async def put_workspaces_workspace_id_members_member_id_permissions(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('put_workspaces_workspace_id_members_member_id_permissions', request)

    async def post_workspaces_workspace_id_members_member_id_permissions_reset(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_workspaces_workspace_id_members_member_id_permissions_reset', request)

    async def get_workspaces_workspace_id_overview(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_overview', request)

    async def get_workspaces_workspace_id_permissions(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_permissions', request)

    async def get_workspaces_workspace_id_quota_summary(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_quota-summary', request)

    async def get_workspaces_workspace_id_quota_usage(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_quota-usage', request)

    async def get_workspaces_workspace_id_roles(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_roles', request)

    async def post_workspaces_workspace_id_roles(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_workspaces_workspace_id_roles', request)

    async def delete_workspaces_workspace_id_roles_role_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('delete_workspaces_workspace_id_roles_role_id', request)

    async def get_workspaces_workspace_id_roles_role_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_roles_role_id', request)

    async def patch_workspaces_workspace_id_roles_role_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('patch_workspaces_workspace_id_roles_role_id', request)

    async def get_workspaces_workspace_id_teams(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_teams', request)

    async def post_workspaces_workspace_id_teams(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('post_workspaces_workspace_id_teams', request)

    async def delete_workspaces_workspace_id_teams_team_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('delete_workspaces_workspace_id_teams_team_id', request)

    async def get_workspaces_workspace_id_teams_team_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('get_workspaces_workspace_id_teams_team_id', request)

    async def patch_workspaces_workspace_id_teams_team_id(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        return await self.open_api('patch_workspaces_workspace_id_teams_team_id', request)
