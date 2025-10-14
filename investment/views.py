from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Investment,Transaction
from .forms import InvestmentForm
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Transaction
from .forms import DepositForm
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Transaction, InvestmentPlan
from .forms import DepositForm  # Assuming you have a form for deposit
from django.utils import timezone
import logging
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import InvestmentPlan, Transaction, Investment
from .forms import DepositForm  # Make sure you have a form for deposit
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import InvestmentPlan, Transaction, Investment
from .forms import DepositForm
import logging
import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction
from .forms import WithdrawalForm
from .models import Transaction, Investment
from django.utils import timezone
from .forms import InvestmentForm, WithdrawalForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import WithdrawalForm
from .models import Investment, Transaction
from django.utils import timezone
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.db import transaction
from .forms import WithdrawalForm
from .models import Transaction
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import WithdrawalForm
from .models import Transaction
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import DepositForm
from .models import Investment, InvestmentPlan, Transaction
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
import logging
from .models import Investment, Transaction
from .forms import InvestmentForm
from .models import Wallet
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from .forms import WithdrawalForm
from .models import Transaction
import logging
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect











logger = logging.getLogger(__name__)

@login_required
def withdrawal_view(request):
    """ View to handle withdrawal functionality from return_of_investment """
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            amount_to_withdraw = form.cleaned_data['amountWithdraw']
            wallet_address = form.cleaned_data['wallet_address']
            payment_date = form.cleaned_data['paymentDate']

            # Get user's profile and ensure they have enough return_of_investment
            user_profile = request.user.userprofile

            # Check if the user has enough return_of_investment for the withdrawal
            if user_profile.return_of_investment >= amount_to_withdraw:
                try:
                    with transaction.atomic():
                        # Deduct the withdrawal amount from the user's return_of_investment
                        user_profile.return_of_investment -= amount_to_withdraw
                        user_profile.save()

                        # Create a Transaction record for the withdrawal
                        transaction_record = Transaction.objects.create(
                            user=request.user,
                            amount=amount_to_withdraw,
                            transaction_type='withdrawal',
                            status='pending',  # Status is pending until approved
                            description=f"Withdrawal of {amount_to_withdraw} to wallet {wallet_address}",
                        )

                    # Redirect to the success page, passing relevant data via GET parameters
                    success_url = reverse('investment:withdrawal_success') + f"?amount_withdrawn={amount_to_withdraw}&wallet_address={wallet_address}&user_name={request.user.username}"
                    return redirect(success_url)

                except Exception as e:
                    # Pass the actual error message
                    error_message = f"An unexpected error occurred during the withdrawal process: {str(e)}"
                    logger.error(f"Unexpected error during withdrawal: {e}")
                    # Redirect to error page with the error message in the URL
                    return redirect(reverse('investment:error_view') + f'?error_message={error_message}')

            else:
                # Pass a specific error message for insufficient ROI
                error_message = "Insufficient return on investment (ROI) for the withdrawal."
                return redirect(reverse('investment:error_view') + f'?error_message={error_message}')
        else:
            # If form is invalid, pass a message for form errors
            error_message = "Please correct the errors in the withdrawal form."
            return redirect(reverse('investment:error_view') + f'?error_message={error_message}')
    else:
        form = WithdrawalForm()

    # Re-render the dashboard page, passing the form and other context
    return render(request, 'userprofile/dashboard.html', {'form': form})





@login_required
def withdrawal_success(request):
    """ Display success message after withdrawal """
    amount_withdrawn = request.GET.get('amount_withdrawn')
    wallet_address = request.GET.get('wallet_address')
    user_name = request.GET.get('user_name')

    return render(request, 'investment/withdrawal_success.html', {
        'amount_withdrawn': amount_withdrawn,
        'wallet_address': wallet_address,
        'user_name': user_name,
    })


# DEPOSIT THAT ADDS ROI AUTOMATICALLY


# @login_required
# def deposit_view(request):
#     """ View to handle deposit functionality """
#     if request.method == 'POST':
#         form = DepositForm(request.POST)
#         if form.is_valid():
#             # Get cleaned data from the form
#             selected_plan = form.cleaned_data['selected_investment_plan']
#             amount_to_deposit = form.cleaned_data['amountDeposit']
#             coin_name = form.cleaned_data['coinName']
#             payment_date = form.cleaned_data['paymentDate']
#             wallet_address = form.cleaned_data['wallet_address']

#             # Get the user's profile
#             user_profile = request.user.userprofile

#             # Find the first available Wallet
#             wallet = Wallet.objects.first()

#             # Check if the wallet exists
#             if wallet:
#                 wallet_name = wallet.name
#             else:
#                 wallet_name = 'No wallet available'

#             # Check if the deposit exceeds the maximum allowed amount for the selected plan
#             if amount_to_deposit > selected_plan.maximum_investment:
#                 error_message = f"The deposit amount exceeds the maximum allowed for this plan: {selected_plan.maximum_investment}."
#                 return redirect(reverse('investment:error_view') + f'?error_message={error_message}')

#             try:
#                 with transaction.atomic():
#                     # Update the user's balance
#                     user_profile.balance += amount_to_deposit
#                     user_profile.save()

#                     # Create a Transaction record
#                     Transaction.objects.create(
#                         user=request.user,
#                         amount=amount_to_deposit,
#                         transaction_type='deposit',
#                         status='pending',
#                         description=f"Deposit of {amount_to_deposit} for {coin_name} to wallet {wallet_address}",
#                     )

#                     # Check if the user already has an investment in the selected plan
#                     investment = Investment.objects.filter(user_profile=user_profile, plan=selected_plan, is_active=True).first()

#                     if investment:
#                         # If an existing investment exists, update the ROI by adding the new deposit amount
#                         investment.roi_accumulated += amount_to_deposit
#                         investment.save()
#                     else:
#                         # If no investment exists, create a new one
#                         Investment.objects.create(
#                             user_profile=user_profile,
#                             plan=selected_plan,
#                             deposit_amount=amount_to_deposit,
#                             roi_accumulated=amount_to_deposit,  # Set initial ROI as the deposit amount
#                             deposit_time=payment_date,
#                             is_active=True,
#                         )

#                 # Redirect to success page
#                 success_url = reverse('investment:deposit_success') + f'?deposit_amount={amount_to_deposit}&wallet_address={wallet_address}&wallet_name={wallet_name}&user_name={request.user.username}&plan_name={selected_plan.name}'
#                 return redirect(success_url)

#             except Exception as e:
#                 error_message = f"An unexpected error occurred while processing your deposit: {str(e)}"
#                 return redirect(reverse('investment:error_view') + f'?error_message={error_message}')

#         else:
#             error_message = "There were errors in the form. Please correct them and try again."
#             return redirect(reverse('investment:error_view') + f'?error_message={error_message}')
#     else:
#         form = DepositForm()

#     return render(request, 'userprofile/dashboard.html', {'form': form})


# @login_required
# def deposit_view(request):
#     """ View to handle deposit functionality """
#     if request.method == 'POST':
#         form = DepositForm(request.POST)
#         if form.is_valid():
#             # Get cleaned data from the form
#             selected_plan = form.cleaned_data['selected_investment_plan']
#             amount_to_deposit = form.cleaned_data['amountDeposit']
#             coin_name = form.cleaned_data['coinName']
#             payment_date = form.cleaned_data['paymentDate']
#             wallet_address = form.cleaned_data['wallet_address']

#             # Get the user's profile
#             user_profile = request.user.userprofile

#             # Find the first available Wallet
#             wallet = Wallet.objects.first()

#             # Check if the wallet exists
#             if wallet:
#                 wallet_name = wallet.name
#             else:
#                 wallet_name = 'No wallet available'

#             # Check if the deposit exceeds the maximum allowed amount for the selected plan
#             if amount_to_deposit > selected_plan.maximum_investment:
#                 error_message = f"The deposit amount exceeds the maximum allowed for this plan: {selected_plan.maximum_investment}."
#                 return redirect(reverse('investment:error_view') + f'?error_message={error_message}')

#             try:
#                 with transaction.atomic():
#                     # Update the user's balance by adding the deposit amount
#                     user_profile.balance += amount_to_deposit
#                     user_profile.save()

#                     # Create a Transaction record for the deposit
#                     Transaction.objects.create(
#                         user=request.user,
#                         amount=amount_to_deposit,
#                         transaction_type='deposit',
#                         status='pending',
#                         description=f"Deposit of {amount_to_deposit} for {coin_name} to wallet {wallet_address}",
#                     )

#                     # You no longer modify the ROI, so no changes are made to the Investment object

#                 # Redirect to the success page
#                 success_url = reverse('investment:deposit_success') + f'?deposit_amount={amount_to_deposit}&wallet_address={wallet_address}&wallet_name={wallet_name}&user_name={request.user.username}&plan_name={selected_plan.name}'
#                 return redirect(success_url)

#             except Exception as e:
#                 error_message = f"An unexpected error occurred while processing your deposit: {str(e)}"
#                 return redirect(reverse('investment:error_view') + f'?error_message={error_message}')

#         else:
#             error_message = "There were errors in the form. Please correct them and try again."
#             return redirect(reverse('investment:error_view') + f'?error_message={error_message}')
#     else:
#         form = DepositForm()

#     return render(request, 'userprofile/dashboard.html', {'form': form})



# MANUAL VIEW ADMIN WILL DO EVERYTHIN


@login_required
def deposit_view(request):
    """ View to handle deposit functionality """
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            selected_plan = form.cleaned_data['selected_investment_plan']
            amount_to_deposit = form.cleaned_data['amountDeposit']
            coin_name = form.cleaned_data['coinName']
            payment_date = form.cleaned_data['paymentDate']
            wallet_address = form.cleaned_data['wallet_address']

            # Get the user's profile
            user_profile = request.user.userprofile

            # Find the first available Wallet
            wallet = Wallet.objects.first()

            # Check if the wallet exists
            wallet_name = wallet.name if wallet else 'No wallet available'

            # Check if the deposit exceeds the maximum allowed amount for the selected plan
            if amount_to_deposit > selected_plan.maximum_investment:
                error_message = f"The deposit amount exceeds the maximum allowed for this plan: {selected_plan.maximum_investment}."
                return redirect(reverse('investment:error_view') + f'?error_message={error_message}')

            try:
                # Begin transaction block
                with transaction.atomic():
                    # Log to confirm the start of transaction creation
                    logger.debug(f"Attempting to create a deposit transaction for amount: {amount_to_deposit}")

                    # Create the pending transaction
                    transaction_instance = Transaction.objects.create(
                        user=request.user,
                        amount=amount_to_deposit,
                        transaction_type='deposit',
                        status='pending',  # Set the status to 'pending'
                        description=f"Deposit of {amount_to_deposit} for {coin_name} to wallet {wallet_address}",
                    )

                    # Log to confirm the transaction creation
                    logger.debug(f"Transaction created successfully: {transaction_instance.id}")

                # Redirect to the success page only after successful creation of the transaction
                success_url = reverse('investment:deposit_success') + f'?deposit_amount={amount_to_deposit}&wallet_address={wallet_address}&wallet_name={wallet_name}&user_name={request.user.username}&plan_name={selected_plan.name}'
                return redirect(success_url)

            except Exception as e:
                # Log the exception for debugging purposes
                logger.error(f"Error occurred while processing the deposit: {str(e)}")

                # Handle the exception and ensure error message is returned
                error_message = f"An unexpected error occurred while processing your deposit: {str(e)}"
                return redirect(reverse('investment:error_view') + f'?error_message={error_message}')

        else:
            error_message = "There were errors in the form. Please correct them and try again."
            return redirect(reverse('investment:error_view') + f'?error_message={error_message}')
    else:
        form = DepositForm()

    return render(request, 'userprofile/dashboard.html', {'form': form})









# MANNUAL APPROVAL 2


@staff_member_required
def approve_transaction_view(request, transaction_id):
    """ Admin view to approve a pending transaction and update the user's balance """
    # Get the transaction object
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if transaction.status != 'pending':
        error_message = "This transaction has already been processed or is not in pending status."
        return redirect(reverse('investment:error_view') + f'?error_message={error_message}')

    try:
        with transaction.atomic():
            # Get the user's profile
            user_profile = transaction.user.userprofile

            # Update the user's balance
            user_profile.balance += transaction.amount
            user_profile.save()

            # Mark the transaction as approved
            transaction.status = 'approved'
            transaction.save()

        # Redirect to the success page
        success_url = reverse('investment:transaction_approved') + f'?transaction_id={transaction.id}'
        return redirect(success_url)

    except Exception as e:
        error_message = f"An error occurred while processing the approval: {str(e)}"
        return redirect(reverse('investment:error_view') + f'?error_message={error_message}')












@login_required
def deposit_success(request):
    deposit_amount = request.GET.get('deposit_amount')
    wallet_address = request.GET.get('wallet_address')
    wallet_name = request.GET.get('wallet_name')
    user_name = request.GET.get('user_name')
    plan_name = request.GET.get('plan_name')

    return render(request, 'investment/deposit_success.html', {
        'deposit_amount': deposit_amount,
        'wallet_address': wallet_address,
        'wallet_name': wallet_name,
        'user_name': user_name,
        'plan_name': plan_name
    })






@login_required
def investment_summary(request, investment_id):
    """ Display investment details and accumulated ROI """
    try:
        investment = Investment.objects.get(id=investment_id)
        if investment.user_profile.user != request.user:
            raise PermissionError("You are not authorized to view this investment.")
        
        # Calculate the ROI if the investment is still active
        investment.update_roi()

        return render(request, 'userprofile/investment_summary.html', {'investment': investment})

    except Investment.DoesNotExist:
        messages.error(request, "Investment not found.")
        logger.error(f"Investment with ID {investment_id} not found.")
        return redirect('dashboard')
    except PermissionError as e:
        messages.error(request, str(e))
        logger.error(f"Permission error: {e}")
        return redirect('dashboard')
    except Exception as e:
        messages.error(request, "An error occurred while fetching investment details.")
        logger.error(f"Error fetching investment details: {e}")
        return redirect('dashboard')
    


@login_required
def error_view(request):
    """ View to display error messages """
    # Get the error_message from the GET query parameters
    error_message = request.GET.get('error_message', 'An unknown error occurred.')  # Default to a generic message if none is found
    return render(request, 'investment/error.html', {'error_message': error_message})