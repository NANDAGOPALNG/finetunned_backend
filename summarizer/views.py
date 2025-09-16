from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .model_service import generate_text

# Upload view with DB save + ML integration placeholder
class DocumentUploadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        doc = Document.objects.create(
            owner=request.user,
            file=file,
            title=getattr(file, 'name', '')
        )

        # =============================
        # ML Integration Placeholder
        # =============================
        # Your ML engineer can call their model here using `doc.file.path`
        # Example:
        #result = model_service.process(doc.file.path)
        #doc.extracted_text = result['text']
        #doc.summary_text = result['summary']
        #doc.status = 'ready'
        #doc.save()
        # =============================
        def summarize(request):
            if request.method == "POST":
                body = json.loads(request.body.decode("utf-8"))
                user_text = body.get("text", "")

            if not user_text.strip():
                return JsonResponse({"error": "No input provided"}, status=400)

            # Generate with model
            output = generate_text(f"Summarize in plain English:\n{user_text}")
            return JsonResponse({"summary": output})
    
return JsonResponse({"error": "POST required"}, status=405)
 serializer = DocumentSerializer(doc)
return Response(serializer.data, status=status.HTTP_201_CREATED)

# List all documents of current user
class DocumentListAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Retrieve / Update / Delete a document
class DocumentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)
    


