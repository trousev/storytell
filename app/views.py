import uuid
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_celery_results.models import TaskResult
from app.forms import TTSForm, SILERO_VOICES, QWEN_VOICES


def index(request):
    return JsonResponse({"message": "Hello, world!"})


class InferenceView(View):
    def get(self, request):
        form = TTSForm()
        return render(request, "app/inference.html", {
            "form": form,
            "silero_voices": json.dumps(SILERO_VOICES),
            "qwen_voices": json.dumps(QWEN_VOICES),
        })

    def post(self, request):
        form = TTSForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)

        text = form.cleaned_data["text"]
        provider = form.cleaned_data["provider"]
        voice = form.cleaned_data["voice"]
        language = form.cleaned_data["language"]

        output_filename = f"{uuid.uuid4().hex}"

        from app.tasks import synthesize_speech
        from django.conf import settings

        if settings.CELERY_TASK_ALWAYS_EAGER:
            audio_url = synthesize_speech(text, provider, voice, language, output_filename)
            return JsonResponse({"status": "success", "audio_url": audio_url})
        else:
            task = synthesize_speech.delay(text, provider, voice, language, output_filename)
            return JsonResponse({"job_id": task.id})


class JobStatusView(View):
    def get(self, request):
        job_id = request.GET.get("job_id")
        if not job_id:
            return JsonResponse({"error": "job_id required"}, status=400)

        try:
            result = TaskResult.objects.get(task_id=job_id)
        except TaskResult.DoesNotExist:
            return JsonResponse({"status": "pending"})

        if result.status == "SUCCESS":
            return JsonResponse({
                "status": "success",
                "audio_url": json.loads(result.result) if result.result else None,
            })
        elif result.status == "FAILURE":
            return JsonResponse({
                "status": "failure",
                "error": result.result,
            })
        else:
            return JsonResponse({"status": result.status.lower()})


class JobMonitorView(View):
    def get(self, request, job_id):
        try:
            result = TaskResult.objects.get(task_id=job_id)
            if result.status == "SUCCESS" and result.result:
                result.result = json.loads(result.result)
        except TaskResult.DoesNotExist:
            result = None

        return render(request, "app/monitor.html", {
            "job_id": job_id,
            "result": result,
        })