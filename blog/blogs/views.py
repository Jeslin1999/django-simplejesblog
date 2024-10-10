from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import FormView,View,DetailView,UpdateView,CreateView,ListView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .forms import RegisterForm,LoginForm,PostForm, UserProfileForm
from .models import User,Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


def home(request):
    context = {}
    return render(request,'index.html',context)



class RegisterView(FormView):
    template_name = 'signup.html'  # Template to render the form
    form_class = RegisterForm      # The form class to use
    success_url = reverse_lazy('base-account')  # Redirect URL after successful registration

    def form_valid(self, form):
        user = form.save()           # Save the new user
        login(self.request, user) 
        return super().form_valid(form) 

    def form_invalid(self, form):
        return super().form_invalid(form)  
    

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect('base-account')
        else:
            return self.form_invalid(form) 
        
        
class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
    

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('profile')  # Redirect to the profile view

    def get_object(self):
        # Return the current user
        return self.request.user
    
def signout(request):
    logout(request)
    return redirect('login')


def index(request):
    context = {}
    return render(request,'base-account.html',context)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    success_url = reverse_lazy('view_posts')

    def form_valid(self, form):
        # Set the author to the current user before saving
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        form.save_m2m()  
        messages.success(self.request, "Post created successfully!") 
        return super().form_valid(form)

class ViewPostsView(ListView):
    model = Post
    template_name = 'view_posts.html'
    context_object_name = 'page_obj'
    paginate_by = 5  # Paginate with 5 posts per page
    ordering = ['-created_at']  # Order by created_at descending

    def get_queryset(self):
        return Post.objects.all()

class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'post_detail.html', {'post': post})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('view_posts')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('view_posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        post.delete()
    return redirect('view_posts')