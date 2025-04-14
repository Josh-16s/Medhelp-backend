# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import ChatSession, ChatMessage
from services.gemini_service import GeminiService

@csrf_exempt


@csrf_exempt
def chat_sessions(request):
    if request.method == 'GET':
        return get_chat_sessions(request)
    elif request.method == 'POST':
        return create_chat_session(request)
    else:
        return JsonResponse({'succeeded': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def chat_messages(request, session_id):
    if request.method == 'GET':
        return get_chat_messages(request, session_id)
    elif request.method == 'POST':
        return create_chat_message(request, session_id)
    return JsonResponse({'succeeded': False, 'message': 'Method not allowed'}, status=405)

def get_chat_sessions(request):
    try:
        # Get all chat sessions (in a real app, filter by user)
        sessions = ChatSession.objects.all().order_by('-created_at')
        sessions_data = [{
            'id': session.id,
            'title': session.title or f"Chat {session.id}",
            'created_at': session.created_at.isoformat(),
        } for session in sessions]
        
        return JsonResponse({
            'succeeded': True,
            'data': sessions_data
        })
    except Exception as e:
        return JsonResponse({
            'succeeded': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_chat_session(request):
    try:
        # Create a new chat session
        session = ChatSession.objects.create(title="New Conversation")
        
        return JsonResponse({
            'succeeded': True,
            'data': {
                'id': session.id,
                'title': session.title,
                'created_at': session.created_at.isoformat(),
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({
            'succeeded': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_chat_messages(request, session_id):
    try:
        # Get all messages for a specific chat session
        messages = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')
        messages_data = [{
            'id': message.id,
            'sender': message.sender_type,
            'text': message.content,
            'created_at': message.created_at.isoformat(),
        } for message in messages]
        
        return JsonResponse({
            'succeeded': True,
            'data': messages_data
        })
    except Exception as e:
        return JsonResponse({
            'succeeded': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_chat_message(request, session_id):
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '')
        sender_type = data.get('sender_type', 'user')
        conversation_history = data.get('conversation_history', [])
        patient_info = data.get('patient_info', None)
        
        if not message_content:
            return JsonResponse({
                'succeeded': False,
                'message': 'Message content is required'
            }, status=400)
            
        # Save the user message
        session = ChatSession.objects.get(id=session_id)
        user_message = ChatMessage.objects.create(
            session=session,
            content=message_content,
            sender_type=sender_type
        )
        
        # If it's a user message, generate and save an assistant response
        if sender_type == 'user':
            gemini_service = GeminiService()
            assistant_response = gemini_service.chat_with_context(
                message_content,
                conversation_history,
                patient_info
            )
            
            if assistant_response['status'] == 'success':
                # Save the assistant response
                assistant_message = ChatMessage.objects.create(
                    session=session,
                    content=assistant_response['response_text'],
                    sender_type='assistant'
                )
                
                return JsonResponse({
                    'succeeded': True,
                    'data': {
                        'id': user_message.id,
                        'sender': user_message.sender_type,
                        'text': user_message.content,
                        'created_at': user_message.created_at.isoformat(),
                        'response_text': assistant_response['response_text']
                    }
                }, status=201)
            else:
                # Return just the user message if assistant response failed
                return JsonResponse({
                    'succeeded': True,
                    'data': {
                        'id': user_message.id,
                        'sender': user_message.sender_type,
                        'text': user_message.content,
                        'created_at': user_message.created_at.isoformat(),
                    },
                    'error': assistant_response['error_message']
                }, status=201)
        
        # Return just the saved message
        return JsonResponse({
            'succeeded': True,
            'data': {
                'id': user_message.id,
                'sender': user_message.sender_type,
                'text': user_message.content,
                'created_at': user_message.created_at.isoformat(),
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({
            'succeeded': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_assistant_response(request, session_id):
    try:
        # Get the latest assistant message for this session
        latest_message = ChatMessage.objects.filter(
            session_id=session_id,
            sender_type='assistant'
        ).order_by('-created_at').first()
        
        if latest_message:
            return JsonResponse({
                'succeeded': True,
                'data': {
                    'id': latest_message.id,
                    'text': latest_message.content,
                    'created_at': latest_message.created_at.isoformat(),
                }
            })
        else:
            return JsonResponse({
                'succeeded': False,
                'message': 'No assistant response found'
            }, status=404)
    except Exception as e:
        return JsonResponse({
            'succeeded': False,
            'message': str(e)
        }, status=500)