from django.contrib import admin
from .models import User
from rest_framework.authtoken.admin import TokenAdmin


class UserAdmin(admin.ModelAdmin):
  # explicitly reference fields to be shown, note image_tag is read-only
  fields = ( 
	  	'image_tag', 
	  	'image',
	  	'first_name', 
	  	'last_name',
	  	'email', 
	  	'username', 
	  	'password', 
	  	'phone_number',
	  	'overview',
			'is_active', 
			'is_staff', 
			'is_superuser', 
			'last_login'
	  	# 'superuser_status',
	  	# 'is_active',
	  	# 'is_staff',
	  	# 'groups',
	  	# 'user_permissions'
  	)
  readonly_fields = ('image_tag',)


TokenAdmin.raw_id_fields = ('user',)
admin.site.register(User, UserAdmin)