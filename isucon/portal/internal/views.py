import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from rest_framework import exceptions
from ipware import get_client_ip

from isucon.portal.authentication.models import Team
from isucon.portal.contest.models import Benchmarker, Job, Server
from isucon.portal.internal.serializers import JobSerializer, JobResultSerializer, ServerSerializer
from isucon.portal.contest import exceptions as contest_exceptions

router = SimpleRouter()


class JobViewSet(viewsets.GenericViewSet):
    serializer_class = JobSerializer

    @action(methods=['post'], detail=False)
    def dequeue(self, request, *args, **kwargs):
        """ベンチマーカが処理すべきジョブをジョブキューからdequeueします"""
        # ベンチマーカーを取得するため、HTTPクライアントのIPアドレスを用いる
        client_ip, _ = get_client_ip(request)
        if client_ip is None:
            raise exceptions.ParseError()

        try:
            benchmarker = Benchmarker.objects.get(ip=client_ip)
        except Benchmarker.DoesNotExist:
            res = Response({"error":'Unknown IP Address', "benchmarker-ip": client_ip, "registered-ips:": Benchmarker.objects.all()}, status=status.HTTP_400_BAD_REQUEST)
            print(res.data)
            return res


        # チームとベンチマーカーが紐づくと仮定して、ジョブを取ってくる
        try:
            job = Job.objects.dequeue(benchmarker)
            job.benchmarker = benchmarker
            job.save()
            serializer = self.get_serializer_class()(instance=job)
            return Response(serializer.data)
        except contest_exceptions.JobDoesNotExistError:
            pass

        # チームに紐づくジョブを見つけられなかったら、他に手頃なジョブを引っ張ってくる
        # TODO: ポータルが、チームとベンチマーカーの紐付けがない状況かどうか判断できる何かしらを用意し、それを根拠に分岐する
        try:
            job = Job.objects.dequeue()
            job.benchmarker = benchmarker
            job.save()
            serializer = self.get_serializer_class()(instance=job)
            return Response(serializer.data)
        except contest_exceptions.JobDoesNotExistError:
            pass

        # 結局ジョブが見つからなかった
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def latest(self, request, pk=None):
        team_id = request.GET.get(key='team_id', default='-1')
        # TODO Delete print statement below this
#        print('Call latest API: team_id=' + team_id)
        job = Job.objects.get_latest(team_id)
        serializer = self.get_serializer_class()(instance=job)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def enqueue(self, request):
        params = json.loads(request.body)
        team_id = params.get('team_id', -1)
        # TODO Delete print statement below this
#        print('Call enqueue API: team_id=' + str(team_id))
        team = Team.objects.filter(id=team_id).first()
        if not Server.objects.of_team(team).exists():
            return JsonResponse(
                {"error": "Server is not set"}, status = 409
            )

        job = None
        try:
            job = Job.objects.enqueue(team)
        except Job.DuplicateJobError:
            return JsonResponse(
                {"error": "Job is running"}, status = 409
            )

        data = {
            "id": job.id,
        }

        return JsonResponse(
            data, status = 200
        )


router.register("job", JobViewSet, base_name="job")


class JobResultViewSet(viewsets.GenericViewSet):
    serializer_class = JobResultSerializer

    @action(methods=['post'], detail=True)
    def report(self, request, pk=None):
        """ベンチマーカーからの結果報告を受け取り、ジョブを更新します"""
        instance = get_object_or_404(Job.objects.all(), pk=pk)
        serializer = self.get_serializer(data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)

            if not "score" in serializer.validated_data:
                raise RuntimeError()

            data = {
                "is_passed": False,
            }
            data.update(serializer.validated_data)

            instance.done(**data)
        except RuntimeError:
            return Response({"error":'Invalid format'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)


router.register("job", JobResultViewSet, base_name="job-result")


class ServerViewSet(viewsets.GenericViewSet):
    serializer_class = ServerSerializer

    @action(methods=['get'], detail=False)
    def target(self, request, pk=None):
        participate_at = request.GET.get(key='participate_at', default='1999-12-31')
        # TODO Delete print statement below this
#        print('Call target API: participate_at=' + str(participate_at))
        teams = Team.objects.filter(participate_at=participate_at).order_by('id').all()
        servers = []
        for team in teams:
            # TODO 後で削除
            print('Append teams_id=' + str(team.id))
            server = Server.objects.get_bench_target(team)
            servers.append(server)

        serializer = self.get_serializer_class()(instance=servers, many=True)
        return Response(serializer.data)

router.register("server", ServerViewSet, base_name="server")
