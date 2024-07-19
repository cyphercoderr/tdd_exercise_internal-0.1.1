# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib import messages
from django.core.cache import cache

from .models import Clue

def update_session_total_attempts(request, increment=1):
    """Update the total_attempts count in cache."""

    total_attempts = request.session.get('total_attempts', 0)
    total_attempts += increment
    request.session['total_attempts'] = total_attempts
    return total_attempts

def drill_view(request):
    if request.method == 'GET':
        update_session_total_attempts(request)

    if request.method == 'POST':
        clue_id = request.POST.get('clue_id')
        answer = request.POST.get('answer', '').strip().lower()

        clue = get_object_or_404(Clue, id=clue_id)
        correct_answer = clue.entry.entry_text.lower()

        if answer == correct_answer:
            # Correct answer
            correct_answers_count = request.session.get('correct_answers', 0) + 1
            request.session['correct_answers'] = correct_answers_count

            total_clues = Clue.objects.count()
            message = f"{correct_answer} is the correct answer! You have now answered {correct_answers_count} (of {total_clues}) clues correctly."
            messages.success(request, message)
            return redirect('xword-answer', clue_id=clue_id)
        else:
            # Incorrect answer
            update_session_total_attempts(request)
            messages.error(request, "Your answer is not correct. Please try again.")

    clue = Clue.objects.order_by("?").first()
    context = {
        'clue_id': clue.id if clue else None,
        'clue_text': clue.clue_text if clue else ""
    }
    return render(request, 'drill.html', context)

def answer_view(request, clue_id):
    clue = get_object_or_404(Clue, id=clue_id)
    entries_stats = Clue.objects.values('entry__entry_text').annotate(count=Count('id')).order_by('-count')

    clue_count = Clue.objects.filter(clue_text=clue.clue_text).count()
    unique_message = "only appearance of this clue" if clue_count == 1 else ""

    answered_correctly = request.session.get('correct_answers', 0)
    total_attempts = request.session.get('total_attempts', 0)

    correct_answers_message = (
        f"{clue.entry.entry_text} is the correct answer! You have now answered "
        f"{answered_correctly} (of {total_attempts}) clues correctly."
    )

    context = {
        'clue': clue,
        'entries_stats': entries_stats,
        'unique_message': unique_message,
        'correct_answers_message': correct_answers_message
    }

    return render(request, 'answer.html', context)
