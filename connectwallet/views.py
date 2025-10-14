# import logging
# from django.shortcuts import render, redirect
# from .models import WalletAsset, ConnectWallet
# from .forms import ConnectWalletForm
# from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail
# from django.core.mail import BadHeaderError
# from django.conf import settings
# import smtplib


# # Configure logging
# logger = logging.getLogger(__name__)

# @login_required
# def select_wallet(request):
#     # Get all available wallets (WalletAsset)
#     wallets = WalletAsset.objects.all()

#     # Get the user's currently connected wallets
#     connected_wallets = ConnectWallet.objects.filter(user=request.user)

#     # Debug: Log the user's currently connected wallets
#     logger.debug(f"User {request.user.username} has {connected_wallets.count()} connected wallets.")

#     # Handle POST request (when the form is submitted)
#     if request.method == 'POST':
#         logger.debug(f"POST data received: {request.POST}")
#         form = ConnectWalletForm(request.POST)
        
#         if form.is_valid():
#             logger.debug("Form is valid. Attempting to save ConnectWallet instance.")
#             try:
#                 # Save the ConnectWallet instance for the user
#                 connect_wallet = form.save(commit=False)
#                 connect_wallet.user = request.user  # Associate the current user
#                 connect_wallet.save()  # Save the ConnectWallet instance
#                 logger.info(f"ConnectWallet instance saved for user {request.user.username}.")

#                 # Try to send email to the user and the admin
#                 try:
#                     # Send email to the user
#                     send_mail(
#                         subject="Wallet Connected Successfully",
#                         message=f"Hello {request.user.username},\n\nYour wallet ({connect_wallet.wallet.name}) has been successfully connected.\n\nThank you!",
#                         from_email=settings.EMAIL_HOST_USER,
#                         recipient_list=[request.user.email],
#                         fail_silently=False,
#                     )

#                     # Send email to the admin
#                     admin_email = 'admin@example.com'  # Replace with your admin email or get it dynamically
#                     send_mail(
#                         subject=f"New Wallet Connected by {request.user.username}",
#                         message=f"Hello Admin,\n\nUser {request.user.username} has connected a new wallet: {connect_wallet.wallet.name}.",
#                         from_email=settings.EMAIL_HOST_USER,
#                         recipient_list=[admin_email],
#                         fail_silently=False,
#                     )
#                     logger.info("Emails sent successfully to user and admin.")
#                 except smtplib.SMTPException as e:
#                     # Log SMTP errors
#                     logger.error(f"SMTP error occurred while sending email: {e}")
#                     error_message = f"SMTP error occurred while sending email: {e}"  # Capture the SMTP error
#                     return redirect('error_page', error_message=error_message)
#                 except BadHeaderError as e:
#                     # Handle BadHeaderError (if the email header is invalid)
#                     logger.error(f"Bad header error: {e}")
#                     error_message = f"Bad header error: {e}"
#                     return redirect('error_page', error_message=error_message)
#                 except Exception as e:
#                     # Catch any other exceptions and log them
#                     logger.error(f"Unexpected error occurred while sending email: {e}")
#                     error_message = f"Unexpected error occurred: {e}"
#                     return redirect('error_page', error_message=error_message)

#                 # Redirect to success page after adding a wallet (this prevents form resubmission on refresh)
#                 return redirect('wallet_connection_success')  # Redirect to success page
#             except Exception as e:
#                 # Catch any other unexpected errors
#                 logger.error(f"Unexpected error occurred while saving wallet: {e}")
#                 error_message = f"Unexpected error occurred while saving wallet: {e}"
#                 return redirect('error_page', error_message=error_message)
#         else:
#             logger.warning("Form is invalid. Errors:")
#             for field, errors in form.errors.items():
#                 logger.warning(f"{field}: {', '.join(errors)}")
#             error_message = "Form submission is invalid. Please correct the errors."
#             return redirect('error_page', error_message=error_message)

#     else:
#         logger.debug("GET request received.")
#         form = ConnectWalletForm()

#     # Render the page, including all wallets and connected wallets
#     return render(request, 'connectwallet/connect_wallet.html', {
#         'form': form,
#         'wallets': wallets,
#         'connected_wallets': connected_wallets,  # Display the user's connected wallets
#     })





# # This view renders the success page after a wallet is connected

# @login_required
# def wallet_connection_success(request):
#     return render(request, 'connectwallet/wallet_connection_success.html')





# @login_required
# def error_page(request):
#     # Retrieve the error message from the query parameters
#     error_message = request.GET.get('error_message', 'An unknown error occurred. Please try again later.')

#     # Render the error page with the error message
#     return render(request, 'connectwallet/error_page.html', {
#         'error_message': error_message
#     })



# EMAIL FAIL ERROR DISPLAY TO ERROR PAGE

# import logging
# from django.shortcuts import render, redirect
# from .models import WalletAsset, ConnectWallet
# from .forms import ConnectWalletForm
# from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail, BadHeaderError
# from django.conf import settings
# from django.urls import reverse
# from django.utils.http import urlencode
# import smtplib

# # Configure logging
# logger = logging.getLogger(__name__)

# @login_required
# def select_wallet(request):
#     wallets = WalletAsset.objects.all()
#     connected_wallets = ConnectWallet.objects.filter(user=request.user)

#     logger.debug(f"User {request.user.username} has {connected_wallets.count()} connected wallets.")

#     if request.method == 'POST':
#         logger.debug(f"POST data received: {request.POST}")
#         form = ConnectWalletForm(request.POST)
        
#         if form.is_valid():
#             logger.debug("Form is valid. Attempting to save ConnectWallet instance.")
#             try:
#                 connect_wallet = form.save(commit=False)
#                 connect_wallet.user = request.user
#                 connect_wallet.save()
#                 logger.info(f"ConnectWallet instance saved for user {request.user.username}.")

#                 # Send email to user and admin
#                 try:
#                     send_mail(
#                         subject="Wallet Connected Successfully",
#                         message=f"Hello {request.user.username},\n\nYour wallet ({connect_wallet.wallet.name}) has been successfully connected.\n\nThank you!",
#                         from_email=settings.EMAIL_HOST_USER,
#                         recipient_list=[request.user.email],
#                         fail_silently=False,
#                     )

#                     admin_email = 'admin@example.com'
#                     send_mail(
#                         subject=f"New Wallet Connected by {request.user.username}",
#                         message=f"Hello Admin,\n\nUser {request.user.username} has connected a new wallet: {connect_wallet.wallet.name}.",
#                         from_email=settings.EMAIL_HOST_USER,
#                         recipient_list=[admin_email],
#                         fail_silently=False,
#                     )
#                     logger.info("Emails sent successfully to user and admin.")

#                 except (smtplib.SMTPException, BadHeaderError, Exception) as e:
#                     logger.error(f"Email sending error: {e}")
#                     error_message = f"Email sending error: {e}"
#                     url = reverse('error_page') + '?' + urlencode({'error_message': error_message})
#                     return redirect(url)

#                 return redirect('wallet_connection_success')

#             except Exception as e:
#                 logger.error(f"Unexpected error occurred while saving wallet: {e}")
#                 error_message = f"Unexpected error occurred while saving wallet: {e}"
#                 url = reverse('error_page') + '?' + urlencode({'error_message': error_message})
#                 return redirect(url)

#         else:
#             logger.warning("Form is invalid. Errors:")
#             for field, errors in form.errors.items():
#                 logger.warning(f"{field}: {', '.join(errors)}")
#             error_message = "Form submission is invalid. Please correct the errors."
#             url = reverse('error_page') + '?' + urlencode({'error_message': error_message})
#             return redirect(url)

#     else:
#         logger.debug("GET request received.")
#         form = ConnectWalletForm()

#     return render(request, 'connectwallet/connect_wallet.html', {
#         'form': form,
#         'wallets': wallets,
#         'connected_wallets': connected_wallets,
#     })


# @login_required
# def wallet_connection_success(request):
#     return render(request, 'connectwallet/wallet_connection_success.html')


# @login_required
# def error_page(request):
#     error_message = request.GET.get('error_message', 'An unknown error occurred. Please try again later.')
#     return render(request, 'connectwallet/error_page.html', {
#         'error_message': error_message
#     })


import logging
from django.shortcuts import render, redirect
from .models import WalletAsset, ConnectWallet
from .forms import ConnectWalletForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.urls import reverse
import smtplib

# Configure logging
logger = logging.getLogger(__name__)

@login_required
def select_wallet(request):
    wallets = WalletAsset.objects.all()
    connected_wallets = ConnectWallet.objects.filter(user=request.user)

    logger.debug(f"User {request.user.username} has {connected_wallets.count()} connected wallets.")

    if request.method == 'POST':
        logger.debug(f"POST data received: {request.POST}")
        form = ConnectWalletForm(request.POST)
        
        if form.is_valid():
            logger.debug("Form is valid. Attempting to save ConnectWallet instance.")
            try:
                connect_wallet = form.save(commit=False)
                connect_wallet.user = request.user
                connect_wallet.save()
                logger.info(f"ConnectWallet instance saved for user {request.user.username}.")

                # Try sending email, but don't break the flow if it fails
                try:
                    send_mail(
                        subject="Wallet Connected Successfully",
                        message=f"Hello {request.user.username},\n\nYour wallet ({connect_wallet.wallet.name}) has been successfully connected.\n\nThank you!",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[request.user.email],
                        fail_silently=True,  # <-- prevents raising error
                    )

                    admin_email = 'admin@example.com'
                    send_mail(
                        subject=f"New Wallet Connected by {request.user.username}",
                        message=f"Hello Admin,\n\nUser {request.user.username} has connected a new wallet: {connect_wallet.wallet.name}.",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[admin_email],
                        fail_silently=True,  # <-- prevents raising error
                    )
                    logger.info("Attempted to send emails (fail_silently=True).")

                except Exception as e:
                    logger.warning(f"Email sending failed but ignored: {e}")

                # Always go to success page even if email fails
                return redirect('wallet_connection_success')

            except Exception as e:
                logger.error(f"Unexpected error occurred while saving wallet: {e}")
                error_message = f"Unexpected error occurred while saving wallet: {e}"
                return redirect(reverse('error_page') + f'?error_message={error_message}')

        else:
            logger.warning("Form is invalid. Errors:")
            for field, errors in form.errors.items():
                logger.warning(f"{field}: {', '.join(errors)}")
            error_message = "Form submission is invalid. Please correct the errors."
            return redirect(reverse('error_page') + f'?error_message={error_message}')

    else:
        logger.debug("GET request received.")
        form = ConnectWalletForm()

    return render(request, 'connectwallet/connect_wallet.html', {
        'form': form,
        'wallets': wallets,
        'connected_wallets': connected_wallets,
    })


@login_required
def wallet_connection_success(request):
    return render(request, 'connectwallet/wallet_connection_success.html')


@login_required
def error_page(request):
    error_message = request.GET.get('error_message', 'An unknown error occurred. Please try again later.')
    return render(request, 'connectwallet/error_page.html', {
        'error_message': error_message
    })
