from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def get_question(request):
    if request.method == "GET":
        question_data = {
            "id": 1,
            "text": "ประเทศไทยมีกี่จังหวัด",
            "choices": [50, 68, 72, 77]
        }
        return JsonResponse(question_data)


@csrf_exempt
def create_question(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        new_question = {
            "id": data.get("id", 8),
            "text": data.get("text", "ภาษาโปรแกรมใดได้รับความนิยมสูงสุดในวิทยาการข้อมูล"),
            "choices": data.get("choices", ["C", "C++", "C#", "Python", "R", "Julia"])
        }
        return JsonResponse(new_question, status=201)
