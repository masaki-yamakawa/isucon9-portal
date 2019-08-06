from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from ipware import get_client_ip

from isucon.portal.authentication.models import Team
from isucon.portal.contest.models import Benchmarker, Job
from isucon.portal.internal.serializers import JobSerializer, JobResultSerializer


router = SimpleRouter()


class JobViewSet(viewsets.ViewSet):
    serializer_class = JobSerializer

    @action(methods=['post'], detail=False)
    def dequeue(self, request, *args, **kwargs):
        """ベンチマーカが処理すべきジョブをジョブキューからdequeueします"""
        # ベンチマーカーを取得するため、HTTPクライアントのIPアドレスを用いる
        client_ip, _ = get_client_ip(request)
        if client_ip is None:
            return HttpResponse('IPアドレスが不正です', status.HTTP_400_BAD_REQUEST)

        try:
            benchmarker = Benchmarker.objects.get(ip=client_ip)
        except Benchmarker.DoesNotExist:
            return HttpResponse('登録されていないベンチマーカーです', status.HTTP_400_BAD_REQUEST)
        try:
            team = Team.objects.get(benchmarker=benchmarker)
        except Team.DoesNotExist:
            return HttpResponse('ベンチマーカーがチームに紐づいていません', status.HTTP_400_BAD_REQUEST)

        job = Job.objects.dequeue(benchmarker)
        if job is None:
            return HttpResponse('ジョブキューが空です', status.HTTP_422_UNPROCESSABLE_ENTITY)

        # ジョブとチームを紐づける
        job.team = team
        job.save()

        serializer = self.serializer_class(instance=job)
        return Response(serializer.data)


router.register("job", JobViewSet, base_name="job")


class JobResultViewSet(viewsets.ViewSet):
    serializer_class = JobResultSerializer

    @action(methods=['post'], detail=True)
    def report(self, request, pk=None):
        """ベンチマーカーからの結果報告を受け取り、ジョブを更新します"""
        instance = get_object_or_404(Job.objects.all(), pk=pk)
        serializer = self.get_serializer(data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            instance.done(**serializer.validated_data)
        except RuntimeError:
            return HttpResponse('ジョブ結果報告の形式が不正です', status.HTTP_400_BAD_REQUEST)

        return HttpResponse('ジョブ結果報告を受け付けました', status.HTTP_201_ACCEPTED)


router.register("job", JobResultViewSet, base_name="job-result")