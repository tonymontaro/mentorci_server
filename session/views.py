import os

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from django.http import JsonResponse

from .models import SessionLog, SESSION_TYPES, SESSION_FEELINGS, PROJECTS
from .serializers import SessionLogSerializer, DetailedSessionLogSerializer
from student.models import Student, STAGES
from .decorators import validate_create_data, validate_update_data


class ListCreateSessionLogView(generics.ListCreateAPIView):
    """
    GET students/
    POST students/
    """
    serializer_class = SessionLogSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return SessionLog.objects.filter(mentor=self.request.user).order_by(
            '-date')

    @validate_create_data
    def post(self, request, *args, **kwargs):
        try:
            student = Student.objects.filter(mentor=self.request.user).get(
                pk=request.data.get('student'))
            session = SessionLog.objects.create(
                student=student,
                summary=request.data.get('summary'),
                concern=request.data.get('concern'),
                date=request.data.get('date'),
                types=request.data.get('types'),
                projects=request.data.get('projects'),
                duration=request.data.get('duration'),
                feeling=request.data.get('feeling'),
                mentor=request.user
            )
            return Response(
                data=SessionLogSerializer(session).data,
                status=status.HTTP_201_CREATED
            )
        except Student.DoesNotExist:
            return Response(
                data={
                    "message": "None of your students has an ID of {}".format(
                        request.data.get('student'))},
                status=status.HTTP_404_NOT_FOUND
            )


class SessionLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET students/:id/
    PUT students/:id/
    DELETE students/:id/
    """
    queryset = SessionLog.objects.all()
    serializer_class = SessionLogSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def _session_not_found(self, pk):
        return Response(
            data={
                "message": "None of your sessions has an ID of {}".format(pk)},
            status=status.HTTP_404_NOT_FOUND
        )

    def get(self, request, *args, **kwargs):
        try:
            session = self.queryset.filter(mentor=self.request.user).get(
                pk=kwargs["pk"])
            if request.GET.get('detailed', '').lower() == 'true':
                session.types = '|'.join(
                    [dict(SESSION_TYPES).get(t, '') for t in
                     session.types.split('|')])
                session.feeling = dict(SESSION_FEELINGS).get(session.feeling, '')
                return Response(DetailedSessionLogSerializer(session).data)
            return Response(SessionLogSerializer(session).data)
        except SessionLog.DoesNotExist:
            return self._session_not_found(kwargs['pk'])

    @validate_update_data
    def put(self, request, *args, **kwargs):
        try:
            session = self.queryset.filter(mentor=self.request.user).get(
                pk=kwargs["pk"])
            serializer = SessionLogSerializer()
            updated_session = serializer.update(session, request.data)
            return Response(SessionLogSerializer(updated_session).data)
        except SessionLog.DoesNotExist:
            return self._session_not_found(kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        try:
            session = self.queryset.filter(mentor=self.request.user).get(
                pk=kwargs["pk"])
            session.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SessionLog.DoesNotExist:
            return self._session_not_found(kwargs['pk'])


def form_options(request, version):
    return JsonResponse({
        'types': SESSION_TYPES,
        'feelings': SESSION_FEELINGS,
        'projects': PROJECTS,
        'projectDict': dict(PROJECTS),
        'typeDict': dict(SESSION_TYPES),
        'feelingDict': dict(SESSION_FEELINGS),
        'stages': STAGES,
        'formUrl': os.getenv('formUrl')
    }, safe=False)
