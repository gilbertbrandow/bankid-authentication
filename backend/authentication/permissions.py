class CustomPermission:
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True