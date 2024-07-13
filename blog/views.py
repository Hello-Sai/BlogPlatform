from django.shortcuts import redirect, render,HttpResponseRedirect
from django.contrib import messages
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from blog.models import Comment, Post
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.
# def home(request):
#     return render(request,'home.html')

@method_decorator(csrf_exempt, name="dispatch")
class PostsView(generic.ListView):
    paginate_by = 5
    model = Post
    template_name = "home.html"
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

@method_decorator(csrf_exempt ,name="dispatch")
class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post_detail.html"
@method_decorator([csrf_exempt,login_required],name="dispatch")
class PostCreationView(generic.View):
    def get(self,request):
        return render(request,"post_create.html")
    def post(self,request):
        try:
            title = request.POST['title']
            content = request.POST['content']

            request.user.posts.create(title = title,content = content)

            messages.success(request,"Successfully posted")
            return render(request,'post_create.html')
        except Exception as e:
            messages.error(request,"Got an Exception -> %s"%(e),"danger")
        return render(request,'post_create.html')

@method_decorator((csrf_exempt,login_required) ,name="dispatch")
class CommentCreationView(generic.View):    
    def post(self,request,slug):
        content = request.POST['content']
        post = Post.objects.filter(slug = slug)
        if post:
            request.user.comments.create(
                content = content,
                post = post.first(),
            )
            messages.success(request,"Successfully Commented")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        messages.error(request,"Not a valid Id","danger")
        return render(request,'post_detail.html') 



@method_decorator(csrf_exempt ,name="dispatch")
class LoginView(generic.View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        user = authenticate(username = request.POST['username'],password=request.POST['password'])
        if user:
            login(request,user)
            messages.success(request,'Successfully Logged In')
            return redirect('home')
        messages.error(request,'Invalid username / password','danger')
        return render(request,'login.html')

@method_decorator(csrf_exempt ,name="dispatch") 
class RegisterView(generic.View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        try:
            if not User.objects.filter(username = request.POST['username']):
            
                user = User.objects.create_user(username = request.POST['username'],password = request.POST['password'])
                if user:
                    messages.success(request,"Account Created Successfully.")
                    login(request,user)
                    return redirect('home')
            messages.error(request,"An Account with this Username already exists ","danger")
            return redirect('register')
        except Exception as e:
            messages.error(request,"Got following error -> %s"%e)
        return render(request,'register.html')
    
@method_decorator(csrf_exempt ,name="dispatch")
class LogoutView(generic.View):
    def get(self,request):
        logout(request)
        messages.success(request,"Successfully Logged Out")
        return redirect('home')
