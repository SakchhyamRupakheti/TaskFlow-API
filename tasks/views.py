from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from rest_framework.pagination import PageNumberPagination
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny


@api_view(["GET"])
def hello_api(request):
    data = {
        "message": "Welcome to TaskFlow API!",
        "status": "success"
    }
    return Response(data)


@api_view(["GET", "POST"])
def task_list(request):

    if request.method == "GET":
        tasks = Task.objects.filter(owner=request.user )
        
#this filters tasks by their status
        
        task_status = request.query_params.get("status")
        if task_status:
            tasks = tasks.filter(status=task_status)
            
#search tasks by title    
        search = request.query_params.get("search")
        if search:
            tasks = tasks.filter(title__icontains=search)
            
#order tasks by creation date
        ordering = request.query_params.get("ordering")
        if ordering == "newest":
            tasks = tasks.order_by("-created_at")
        elif ordering == "oldest":
            tasks = tasks.order_by("created_at")
            
        #pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5
        
        page = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk, owner=request.user)
    except Task.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

 
    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data)


    elif request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

  
    elif request.method == "PATCH":
        print("PATCH request received", request.data)
        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

  
    elif request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response(
            {"message": "User registered successfully",
             "username": user.username},
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )
