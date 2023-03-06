from django.contrib.auth import authenticate, login
from user.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserCreateAPIView(APIView):

    def post(self, request):
        """Crée un nouvel utilisateur.

        Crée un nouvel utilisateur en utilisant les informations fournies dans la requête post.
        Si les informations sont valides, l'utilisateur sera enregistré dans la base de donnée et une réponse HTTP 201
        CREATED est renvoyée avec les informations de l'utilisateur.
        Sinon, une réponse HTTP 400 BAD REQUEST est renvoyée avec les erreurs de validation.

        Args:
            request (HttpRequest): L'objet HttpRequest contenant les données de la requête.

        Returns:
            Response: Une réponse HTTP contenant les informations de l'utilisateur nouvellement créé
            et le code de statut HTTP approprié.

        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    def post(self, request):
        """Connecte un utilisateur existant.

        Connecte un utilisateur existant en utilisant les informations fournies dans la requête POST.
        Si les informations d'identification sont valides, l'utilisateur est connecté et une réponse HTTP 200 OK
        est renvoyée. Sinon, une réponse HTTP 400 BAD REQUEST est renvoyée avec un message d'erreur.

        Args:
            request (HttpRequest): L'objet HttpRequest contenant les données de la requête.

        Returns:
            Response: Une réponse HTTP avec un code de statut approprié en fonction du résultat de la tentative de
            connexion.
            Si la connexion est réussie, renvoie une réponse HTTP 200 OK. Si les informations d'identification sont
            invalides, renvoie une réponse HTTP 400 BAD REQUEST avec un message d'erreur.

        """
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email ou mot de passe invalide'}, status=400)
