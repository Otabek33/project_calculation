from django.contrib.auth.mixins import AccessMixin


class FinanceRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_finance or request.user.is_super_user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ProjectUsageRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_universal_user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
