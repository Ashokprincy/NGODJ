from django.shortcuts import render, redirect, get_object_or_404
from .models import Campaign, Donation
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Sum  # Added Sum for impact calculation
from django.db import transaction    # Added for data integrity

def index(request):
    """Landing page showing all active campaigns."""
    campaigns = Campaign.objects.all()
    return render(request, 'donations/index.html', {'campaigns': campaigns})

def register(request):
    """Public registration view for new donors."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def donate(request, campaign_id):
    """Handles transactions with data safety and progress tracking."""
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    recent_donations = Donation.objects.filter(campaign=campaign).order_by('-date')[:5]
    
    # Calculate progress percentage for the UI bar
    if campaign.goal_amount > 0:
        progress = (campaign.raised_amount / campaign.goal_amount) * 100
        progress = min(progress, 100)
    else:
        progress = 0

    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive.")

            # ATOMIC TRANSACTION: Both steps must succeed, or both fail.
            with transaction.atomic():
                # 1. Record the donation
                Donation.objects.create(
                    donor=request.user,
                    campaign=campaign,
                    amount=amount
                )
                
                # 2. Update campaign total
                campaign.raised_amount += amount
                campaign.save()

            # Calculate donor's lifetime impact for the success message
            total_user_impact = Donation.objects.filter(donor=request.user).aggregate(Sum('amount'))['amount__sum'] or 0

            messages.success(request, f"🎉 Amazing! You just donated ${amount} to {campaign.title}. Your lifetime impact is now ${total_user_impact:,.2f}!")
            return redirect('home')

        except (ValueError, TypeError):
            messages.error(request, "Invalid amount. Please enter a valid number.")
    
    return render(request, 'donations/donate.html', {
        'campaign': campaign,
        'recent_donations': recent_donations,
        'progress': progress
    })

@login_required
def profile(request):
    """Private donor profile showing personal impact history."""
    user_donations = Donation.objects.filter(donor=request.user).order_by('-date')
    total_impact = user_donations.aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'donations/profile.html', {
        'donations': user_donations,
        'total_impact': total_impact
    })

@staff_member_required
def admin_dashboard(request):
    """Staff-only view with visual charts and searchable donor database."""
    query = request.GET.get('q')
    campaigns = Campaign.objects.all()
    
    if query:
        donations = Donation.objects.filter(
            Q(donor__username__icontains=query) | 
            Q(campaign__title__icontains=query)
        ).order_by('-date')
    else:
        donations = Donation.objects.all().order_by('-date')
    
    total_raised = sum(c.raised_amount for c in campaigns)
    campaign_names = [c.title for c in campaigns]
    campaign_funds = [float(c.raised_amount) for c in campaigns]
    
    return render(request, 'donations/admin_dashboard.html', {
        'donations': donations,
        'total_raised': total_raised,
        'campaign_names': campaign_names,
        'campaign_funds': campaign_funds,
        'query': query
    })

