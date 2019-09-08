from django.shortcuts import render, get_object_or_404
from isucon.portal.authentication.decorators import team_is_authenticated
from isucon.portal.contest.decorators import show_result_enabled

from isucon.portal.contest.models import Job, Score

def get_base_context(user):
    return {
        "result": True,
        "staff": False,
    }

@team_is_authenticated
@show_result_enabled
def scores(request):
    context = get_base_context(request.user)

    context.update({
        "passed": Score.objects.passed().filter(team__participate_at=request.user.team.participate_at).select_related("team"),
        "failed": Score.objects.failed().filter(team__participate_at=request.user.team.participate_at).select_related("team"),
    })

    return render(request, "scores.html", context)

@team_is_authenticated
@show_result_enabled
def jobs(request):
    context = get_base_context(request.user)

    jobs = Job.objects.of_team(request.user.team)
    context.update({
        "jobs": jobs,
    })

    return render(request, "jobs.html", context)

@team_is_authenticated
@show_result_enabled
def job_detail(request, pk):
    context = get_base_context(request.user)

    job = get_object_or_404(Job.objects.filter(team=request.user.team), pk=pk)
    context.update({
        "job": job,
    })

    return render(request, "job_detail.html", context)
