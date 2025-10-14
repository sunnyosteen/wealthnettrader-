from django.contrib import admin

# Register your models here.
# from django.contrib import admin
# from .models import UserProfile

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone_number', 'profile_image', 'wallet_address', 'balance', 'referral_code', 'date_of_birth', 'country', 'address')
#     search_fields = ['user__username', 'phone_number', 'wallet_address', 'referral_code']
#     list_filter = ('country', 'date_of_birth')
#     list_editable = ('phone_number', 'wallet_address', 'balance')
    
#     fieldsets = (
#         (None, {
#             'fields': ('user', 'phone_number', 'profile_image', 'wallet_address', 'date_of_birth')
#         }),
#         ('Financial Information', {
#             'fields': ('balance', 'referral_code', 'return_of_investment', 'withdrawable_amount', 'referral_reward')
#         }),
#         ('Address Information', {
#             'fields': ('country', 'address')
#         }),
#         ('Additional Information', {
#             'fields': ('trading_certificates', 'selected_investment_plan', 'date')  # `date` is now read-only
#         })
#     )

#     # Make 'date' field readonly
#     readonly_fields = ('date',)

# # Register UserProfile model with the admin
# admin.site.register(UserProfile, UserProfileAdmin)


from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    # Define the columns you want to display in the list view
    list_display = (
        'user', 'phone_number', 'profile_image', 'wallet_address', 'balance',
        'referral_code', 'date_of_birth', 'country', 'address', 'first_name',
        'last_name', 'govt_issued_id'
    )
    # Add fields you want to search by in the admin search bar
    search_fields = ['user__username', 'phone_number', 'wallet_address', 'referral_code', 'first_name', 'last_name']
    
    # Add filters for the admin page
    list_filter = ('country', 'date_of_birth')
    
    # Add fields you can edit directly in the list view
    list_editable = ('phone_number', 'wallet_address', 'balance')
    
    # Define fieldsets for organizing how the fields appear in the detail view
    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name', 'phone_number', 'profile_image', 'wallet_address', 'date_of_birth')
        }),
        ('Financial Information', {
            'fields': ('balance', 'referral_code', 'return_of_investment', 'withdrawable_amount', 'referral_reward')
        }),
        ('Address Information', {
            'fields': ('country', 'address')
        }),
        ('Additional Information', {
            'fields': ('govt_issued_id', 'trading_certificates', 'selected_investment_plan', 'date')  # `govt_issued_id` is now in the Additional Information section
        })
    )

    # Make the 'date' field readonly
    readonly_fields = ('date',)

# Register the UserProfile model with the admin interface
admin.site.register(UserProfile, UserProfileAdmin)
