from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
	"""
	Custom permission to only allow authors of an article to edit it.
	Also the article is not readable by others if it's private.
	"""
	
	def has_object_permission(self, request, view, obj):
		if obj.author == request.user:
			return True
		if obj.public == True and request.method in permissions.SAFE_METHODS:
			return True

		return False
