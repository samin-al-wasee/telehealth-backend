from django.conf import settings
from django.db import transaction

from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

from rest_framework.permissions import IsAuthenticated

from appointmentio.models import Appointment, AppointmentTwilioConnector

from notificationio.services import notification_for_video_call


class PublicVideoCallList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        room_name = request.query_params.get("room_name")

        if not room_name:
            raise ValidationError("Room name is required!")

        twilio_connector = AppointmentTwilioConnector.objects.filter(
            room_name=room_name
        ).last()

        # Check if twilio_connector exists
        if not twilio_connector:
            raise ValidationError("No video call found for the given room name!")

        appointment = twilio_connector.appointment

        user_name = None

        if request.user == appointment.patient.user:
            user_name = appointment.doctor.user.get_name()
        elif request.user == appointment.doctor.user:
            user_name = appointment.patient.user.get_name()
        else:
            raise ValidationError("You are not allowed to get this data!")

        response_data = {
            "name": user_name,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        with transaction.atomic():
            room_name = request.data.get("room_name")
            identity = request.data.get("identity")
            appointment_uid = request.data.get("appointment")

            # validate inputs
            if not room_name or not identity or not appointment_uid:
                raise ValidationError("Missing required data!")

            try:
                appointment = Appointment.objects.get(uid=appointment_uid)
            except:
                raise ValidationError("Appointment not found!")

            # create the access token
            access_token = AccessToken(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_API_KEY,
                settings.TWILIO_API_KEY_SECRET,
                identity=identity,
            )

            # create the video grant
            video_grant = VideoGrant(room=room_name)

            # Add the video grant to the access token
            access_token.add_grant(video_grant)

            AppointmentTwilioConnector.objects.create(
                appointment=appointment, room_name=room_name
            )

            # create notification instance
            notification_for_video_call(appointment, request.user)

            response_data = {"token": access_token.to_jwt()}

            # Return the token and room_name in the response
            return Response(response_data, status=status.HTTP_200_OK)
