from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Petition, Vote
from .forms import PetitionForm
from django.contrib import messages

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    template_data['petitions'] = Petition.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        user_votes = Vote.objects.filter(user=request.user).values_list('petition_id', flat=True)
        template_data['user_votes'] = list(user_votes)

    return render(request, 'petitions/index.html', {'template_data': template_data})

@login_required
def create(request):
    template_data = {}
    template_data['title'] = 'Create Petition'
    
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Your petition has been created successfully!')
            return redirect('petitions.index')
    else:
        form = PetitionForm()
    
    template_data['form'] = form
    return render(request, 'petitions/create.html', {'template_data': template_data})

@login_required
def vote(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    
    existing_vote = Vote.objects.filter(petition=petition, user=request.user).first()
    
    if existing_vote:
        messages.info(request, 'You have already voted on this petition.')
    else:
        Vote.objects.create(petition=petition, user=request.user, vote_type='yes')
        messages.success(request, 'Your vote has been recorded!')
    
    return redirect('petitions.index')