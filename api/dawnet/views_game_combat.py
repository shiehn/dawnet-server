from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.parsers import JSONParser
from byo_network_hub.models import GameMap
from .serializers import GameMapSerializer
from .serializers import GameStateSerializer
import logging

logger = logging.getLogger(__name__)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from game_engine.api.combat_processor import CombatProcessor
from rest_framework.permissions import IsAuthenticated


class GameCombatAttackView(APIView):
    """
    Attack an encounter.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if request.user is None:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_id = request.user.id

        item_id = request.data.get("item_id", None)

        logger.info("COMBAT user_id: " + str(user_id))
        logger.info("COMBAT item_id: " + str(item_id))

        if item_id is None:
            return Response(
                {"message": "Item is required in the payload"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        combat_processor = CombatProcessor()

        combat_result = combat_processor.attack(item_id)
        if combat_result == "encounter-victory" or combat_result == "encounter-loss":
            return Response({"message": combat_result}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": combat_result}, status=status.HTTP_400_BAD_REQUEST
            )
