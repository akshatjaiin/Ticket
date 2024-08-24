from django.http import HttpResponse

def index(request):
    return HttpResponse("""
<html>
<body>
HelloWorld
<script>
window.location.href+="/ticket";
</script>
</body>
</html>
    """);
