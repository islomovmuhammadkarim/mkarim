from django.shortcuts import render,redirect
from .models import Banner,Service,AboutMe,Eduacation,Experience,Project,ProjectImage,ContactMessage,ContactInfo,Skill,Blog,Comment,Category,Tag,ClientStat
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
import requests

# Create your views here.
def home(request):
    about_me = AboutMe.objects.first()
    services = Service.objects.all()
    experiences =Experience.objects.all()  # iterable
    educations = Eduacation.objects.all()   # iterable
    social_media = about_me.social_media
    projects = Project.objects.all()
    banner = Banner.objects.filter(is_active=True).first() 
    client_stats = ClientStat.objects.filter(is_active=True)  # faqat faol statlar


    context = {
        "about": about_me,
        "experiences": experiences,
        "educations": educations,
        "social_media": social_media,
        'projects':projects,
        "banner": banner,
        'client_stats': client_stats,
        'services':services,

    }
    return render(request, 'portfolio/home.html',context)



def about(request):
    about_me = AboutMe.objects.first()
    experiences =Experience.objects.all()  # iterable
    educations = Eduacation.objects.all()   # iterable
    social_media = about_me.social_media

    context = {
        "about": about_me,
        "experiences": experiences,
        "educations": educations,
        "social_media": social_media,
    }
    return render(request, 'portfolio/about.html', context=context)




def works(request):
    projects = Project.objects.filter(is_active=True).order_by('-create_at')
    return render(request, 'portfolio/works.html', {'projects': projects})


def work_details(request, slug):
    project = get_object_or_404(Project, slug=slug, is_active=True)
    images = ProjectImage.objects.filter(project=project)

    # Keyingi loyiha
    next_project = Project.objects.filter(
        create_at__gt=project.create_at,
        is_active=True
    ).order_by('create_at').first()

    # Agar keyingi loyiha bo‘lmasa, birinchi loyihaga qaytish
    if not next_project:
        next_project = Project.objects.filter(is_active=True).order_by('create_at').first()

    context = {
        'project': project,
        'images': images,
        'next_project': next_project
    }
    return render(request, 'portfolio/work-details.html', context)


def contact(request):
    about_me = AboutMe.objects.first()
    social_media = about_me.social_media  # bu list bo'lishi mumkin
    contact_info = ContactInfo.objects.all()


    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')

        # ContactMessage yaratish
        ContactMessage.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message_text
        )
        telegram_message = f"Yangi xabar!\nIsm: {full_name}\nEmail: {email}\nMavzu: {subject}\nXabar: {message_text}"
        requests.get(
            f"https://api.telegram.org/bot8451469762:AAHkvSv9TapiqFhOxdBshMjJm8A4L3euB_E/sendMessage",
            params={"chat_id": 7438442445, "text": telegram_message}
        )
        messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi!")
        return redirect('contact')
    
    context = {
        'contact_infos': contact_info,
        'social_media': social_media,
    }
    
    return render(request, 'portfolio/contact.html', context)



def credentials(request):
    # Foydalanuvchi profilini olish (birinchi user uchun)
    about_me = AboutMe.objects.first()
    
    # Foydalanuvchi bilan bog‘liq barcha education va experience
    educations = Eduacation.objects.filter(about_me=about_me).order_by('start_year')
    experiences = Experience.objects.filter(about_me=about_me).order_by('start_year')
    
    # Skills (ManyToMany)
    skills = about_me.skills.all() if about_me else []

    context = {
        'about_me': about_me,
        'educations': educations,
        'experiences': experiences,
        'skills': skills,
    }
    return render(request, 'portfolio/credentials.html', context)



def blog_list(request):
    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')

    blogs = Blog.objects.all().order_by('-created_at')

    if search_query:
        blogs = blogs.filter(title__icontains=search_query)

    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)

    if tag_slug:
        blogs = blogs.filter(tags__slug=tag_slug)

    recent_posts = Blog.objects.all().order_by('-created_at')[:5]
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'blogs': blogs,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
        'search_query': search_query,
    }

    return render(request, 'portfolio/blog.html', context)


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    recent_posts = Blog.objects.all().order_by('-created_at')[:5]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    comments = Comment.objects.filter(blog=blog, parent=None).order_by('-created_at')

    context = {
        'blog': blog,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
        'comments': comments,
    }
    return render(request, 'portfolio/blog-details.html', context)

def add_comment(request, slug):
    if request.method == "POST":
        blog = get_object_or_404(Blog, slug=slug)
        name = request.POST.get('name', '').strip()
        message = request.POST.get('message', '').strip()
        parent_id = request.POST.get('parent_id')

        if not name or not message:
            # Agar name yoki message bo‘sh bo‘lsa, blogga qaytadi
            return redirect('blog_details', slug=slug)

        parent_comment = None
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                parent_comment = None

        Comment.objects.create(
            blog=blog,
            name=name,
            message=message,
            parent=parent_comment
        )
        return redirect('blog_details', slug=slug)
    return redirect('blog_details', slug=slug)





def service_view(request):
    services = Service.objects.all()
    about_me = AboutMe.objects.first()
    experiences =Experience.objects.all()  # iterable
    educations = Eduacation.objects.all()   # iterable
    social_media = about_me.social_media

    context = {
        'services': services,
        "about": about_me,
        "experiences": experiences,
        "educations": educations,
        "social_media":social_media
    }
    return render(request, 'portfolio/service.html', context)
