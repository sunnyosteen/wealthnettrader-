from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from decimal import Decimal



# Use a string reference for InvestmentPlan to avoid circular import
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)  
    country = CountryField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    referral_code = models.CharField(max_length=100, blank=True, null=True)
    trading_certificates = models.ImageField(upload_to='trading_certificates/', blank=True, null=True)
    return_of_investment = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(auto_now_add=True)
    withdrawable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    referral_reward = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    selected_investment_plan = models.ForeignKey('investment.InvestmentPlan', on_delete=models.SET_NULL, null=True, blank=True)  # String reference
    govt_issued_id = models.ImageField(upload_to='govt_issued_ids/', blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    def calculate_withdrawable(self):
        """
        Updates the withdrawable amount based on the return of investment.
        """
        self.withdrawable_amount = self.return_of_investment
        self.save()

    def calculate_return_of_investment(self, deposit_amount):
        """
        Updates the return_of_investment field based on the 10% ROI on the deposit,
        or based on the selected investment plan.
        """
        if self.selected_investment_plan:
            # Calculate based on selected investment plan's interest rate
            self.return_of_investment = deposit_amount * (self.selected_investment_plan.interest_rate / Decimal('100'))
        else:
            # Fallback to default 10% if no plan is selected
            self.return_of_investment = deposit_amount * Decimal('0.10')  # 10% ROI
        self.save()

    def update_balance(self, amount, transaction_type):
        """
        Updates the user's balance based on the transaction type (deposit/withdrawal).
        """
        if transaction_type == 'deposit':
            self.balance += amount
        elif transaction_type == 'withdrawal':
            self.balance -= amount

        self.save()

    def __str__(self):
        return (
            f"User: {self.user.username}, Email: {self.user.email}, Phone: {self.phone_number}, "
            f"Wallet: {self.wallet_address}, Country: {self.country}, Address: {self.address}, "
            f"Balance: {self.balance}, Referral Reward: {self.referral_reward}, "
            f"ROI: {self.return_of_investment}, Withdrawable: {self.withdrawable_amount}, "
            f"Selected Plan: {self.selected_investment_plan.name if self.selected_investment_plan else 'None'}"
        )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
