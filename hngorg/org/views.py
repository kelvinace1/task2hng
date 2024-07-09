from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,  permission_classes
from .models import Organisation
from .serializers import OrganisationSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import User 
import uuid

a=1
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_organisation(request):
    if request.method == 'POST':
        user = request.user
        name = request.data.get('name')
        description = request.data.get('description', '')

        if not name:
            return Response({
            
                'status': 'bad request',
                'message': 'client error',
                'status_code': status.HTTP_400_BAD_REQUEST
            }, 
            
            status=status.HTTP_400_BAD_REQUEST)

        organisation = Organisation.objects.create(
            orgId=str(uuid.uuid4()),
            name=name,
            description=description
        )
        organisation.users.add(user)

        serializer = OrganisationSerializer(organisation)
        return Response({
            "status": "success",
            "message": "Organisation created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    elif request.method == "GET":

        user = request.user
        created_organisations = user.organisations.filter(users=user)
        user_organisations = user.organisations.all()

        organisations = created_organisations | user_organisations


        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            "status": "success",
            "message": "Organisations retrieved successfully",
            "data": {
                "organisations": serializer.data
            }
        }, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organisation_detail(request, orgId):
    try:
        organisation = Organisation.objects.get(orgId=orgId)
    except Organisation.DoesNotExist:
        return Response({
            "status": "Not Found",
            "message": "Organisation does not exist"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = OrganisationSerializer(organisation)
    return Response({
        "status": "success",
        "message": "Organisation  retrieved successfully",
        "data": serializer.data
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_users(request, orgId):
    try:
        organisation = Organisation.objects.get(orgId=orgId)
    except Organisation.DoesNotExist:
        return Response({
            "status": "Not Found",
            "message": "Organization does not exist"
        }, status=status.HTTP_404_NOT_FOUND)

    user = request.data.get('userId')

    if user:
        try:
            user = User.objects.get(userId=user)
        except User.DoesNotExist:
            return Response({
                "status": "Not Found",
                "message": "invalid id",
            }, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({
            "status": "Bad Request",
            "message": "Invalid id"
        }, status=status.HTTP_400_BAD_REQUEST)


    organisation.users.add(user)
    organisation.save()

    return Response({
        "status": "success",
        "message": "User added to organization successfully"
    }, status=status.HTTP_200_OK)



