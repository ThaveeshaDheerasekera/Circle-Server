import logging
from .models import Note
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from .serializers import EntriesSerializer
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)


# All these APIs are filtered by user_id
@api_view(['GET', 'POST'])
def list_and_create_entry(request, username):
    # this code snippet is used to validate the user_id
    # if user_id is not there, a 404 error will be passed
    # else entry variable will be initialised
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        error_message = f'The user with username {username} does not exist.'
        return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

    # getLogList method
    if request.method == 'GET':
        try:
            logs = Note.objects.filter(user=user)
            serializer = EntriesSerializer(logs, many=True)
            return Response({'logs': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            logger.exception('Error in getLogList method')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # createEntry method
    elif request.method == 'POST':
        try:
            serializer = EntriesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # Save the created entry
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = str(e)
            logger.exception("Error in createEntry method")
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['DELETE', 'PUT'])
# def manipulate_entry_by_pk(request, entry_id):
#     # this code snippet is used to validate the entry id
#     # if entry id is not there, a 404 error will be passed
#     # else entry variable will be initialised
#     try:
#         entry = Note.objects.get(pk=entry_id)
#     except Note.DoesNotExist:
#         error_message = f'The entry with ID {entry_id} does not exist.'
#         return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)
#
#     # deleteEntry method
#     if request.method == 'DELETE':
#         try:
#             # delete the image
#             # to save the storage
#             entry.image.delete()
#             entry.delete()
#             message = 'Entry deleted successfully!'
#             return Response({'message': message}, status=status.HTTP_200_OK)
#         except Exception as e:
#             error_message = str(e)
#             logger.exception('Error in deleteEntry method')
#             return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     # updateEntry method
#     elif request.method == 'PUT':
#         try:
#             serializer = EntriesSerializer(entry, data=request.data, partial=True)
#             if serializer.is_valid():
#                 # Check if the image field is updated
#                 # if updated, delete the old image
#                 # to save the storage
#                 if 'image' in request.data and request.data['image'] != str(entry.image):
#                     entry.image.delete()
#                 serializer.save()  # Save the updated entry
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response({'error': serializer.errors}, status=status.HTTP_409_CONFLICT)
#         except Exception as e:
#             error_message = str(e)
#             logger.exception('Error in updateEntry method')
#             return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----------------

# from rest_framework import generics
# from rest_framework.views import APIView
# from rest_framework.pagination import LimitOffsetPagination

# class EntryListGeneric(generics.ListCreateAPIView):
#     serializer_class = EntriesSerializer
#     queryset = Entries.objects.all()
#     pagination_class = LimitOffsetPagination
#
#
# class EntryByPKGeneric(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = EntriesSerializer
#     queryset = Entries.objects.all()
#
#
# class EntryByUserAndPk(APIView):
#     def get(self, request, user_id, pk):
#         entries = Entries.objects.all()
#         serializer = EntriesSerializer(entries, many=True)
