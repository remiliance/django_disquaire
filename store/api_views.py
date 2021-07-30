from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Album, Contact, Booking, BookingLines
from store.serializers import ContactSerializer, BookingSerializer


@api_view(['GET', 'UPDATE', 'DELETE'])
def get_delete_update_contacts(request, pk):
    try:
        contact = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single contact
    if request.method == 'GET':
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    # update details of a single contact
    if request.method == 'PUT':
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a single contact
    elif request.method == 'DELETE':
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def get_post_contacts(request):
    if request.method == 'GET':
        puppies = Contact.objects.all()
        serializer_class = ContactSerializer(puppies, many=True)
        return Response(serializer_class.data)
        # insert a new record for a contact
    if request.method == 'POST':
        data = {
        'name': request.data.get('name'),
        'email': request.data.get('email')
        }
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
