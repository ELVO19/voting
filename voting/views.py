from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import Student, Category, Candidate, Vote, AllowedVoter


def get_logged_in_student(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return None
    return Student.objects.filter(id=student_id).first()





def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            pwd = form.cleaned_data['password']

            if not email.endswith('@strathmore.edu'):
                messages.error(request, "You must use your @strathmore.edu email to vote.")
                return render(request, 'voting/login.html', {'form': form})

            if not AllowedVoter.objects.filter(email=email).exists():
                messages.error(request, "This email is not on the approved voter list. Contact the election admin.")
                return render(request, 'voting/login.html', {'form': form})

            student, created = Student.objects.get_or_create(email=email)

            if created:
                student.set_password(pwd)
                student.save()
                messages.success(request, "Account created. You're logged in.")
            else:
                if not student.check_password(pwd):
                    messages.error(request, "Incorrect password for this email.")
                    return render(request, 'voting/login.html', {'form': form})

            request.session['student_id'] = student.id
            return redirect('vote')
    else:
        form = LoginForm()

    return render(request, 'voting/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('login')


def vote_view(request):
    student = get_logged_in_student(request)
    if not student:
        return redirect('login')

    has_voted = Vote.objects.filter(student=student).exists()
    if has_voted:
        return redirect('confirmation')

    categories = Category.objects.prefetch_related('candidates').all()
    voters_count = Student.objects.filter(vote__isnull=False).distinct().count()

    if request.method == 'POST':
        candidate_ids = request.POST.getlist('candidates')

        if len(candidate_ids) != 2:
            messages.error(request, "You must select exactly 2 candidates.")
            return redirect('vote')

        candidates = Candidate.objects.filter(id__in=candidate_ids)
        if candidates.count() != 2:
            messages.error(request, "Invalid selection. Please try again.")
            return redirect('vote')

        for candidate in candidates:
            if not candidate.category.is_open:
                messages.error(request, f"Voting is closed for {candidate.category.name}.")
                return redirect('vote')
            Vote.objects.create(candidate=candidate, category=candidate.category, student=student)

        return redirect('confirmation')

    context = {
        'categories': categories,
        'has_voted': has_voted,
        'student': student,
        'voters_count': voters_count,
    }
    return render(request, 'voting/vote.html', context)

def confirmation_view(request):
    student = get_logged_in_student(request)
    if not student:
        return redirect('login')

    votes = Vote.objects.filter(student=student).select_related('candidate')

    if not votes.exists():
        return redirect('vote')

    voters_count = Student.objects.filter(vote__isnull=False).distinct().count()

    return render(request, 'voting/confirmation.html', {'votes': votes, 'student': student, 'voters_count': voters_count})


def results_view(request):
    categories = Category.objects.prefetch_related('candidates').all()

    results = []
    for category in categories:
        candidates = category.candidates.all()
        candidate_data = [
            {'name': c.name, 'votes': c.vote_count(), 'photo': c.photo}
            for c in candidates
        ]
        candidate_data.sort(key=lambda x: x['votes'], reverse=True)
        total_votes = sum(c['votes'] for c in candidate_data)
        results.append({
            'category': category,
            'candidates': candidate_data,
            'total_votes': total_votes,
        })

    return render(request, 'voting/results.html', {'results': results})