from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models
from ckeditor.fields import RichTextField



# ------------------------------
# Custom User Model
# ------------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        help_text="Enter your email address"
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        help_text="Enter your username"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
# ------------------------------



# ------------------------------
# About Me Section
# ------------------------------
class AboutMe(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        help_text="Select the user this profile belongs to"
    )
    about_me = models.TextField(
        help_text="Write a short description about yourself"
    )
    image_name = models.CharField(
        max_length=100,
        default='port.jpg',
        help_text="Static images/portfolio papkasidagi rasm nomi"
    )
    skills = models.ManyToManyField(
        'Skill',
        blank=True,
        help_text="Select your skills"
    )
    my_name = models.CharField(
        max_length=100,
        help_text="Enter your full name"
    )
    social_media = models.JSONField(
        null=True,
        blank=True,
        help_text="Add your social media links in JSON format"
    )

    def __str__(self):
        return self.my_name
# ------------------------------


# ------------------------------
# Education Section
# ------------------------------
class Eduacation(models.Model):
    about_me = models.ForeignKey(
        AboutMe,
        on_delete=models.CASCADE,
        help_text="Select the profile this education belongs to"
    )
    start_year = models.CharField(
        max_length=4,
        help_text="Start year, e.g., 2005"
    )
    end_year = models.CharField(
        max_length=4,
        help_text="End year, e.g., 2008"
    )
    degree = models.CharField(
        max_length=100,
        help_text="Degree name, e.g., Bachelor of Science"
    )
    university = models.CharField(
        max_length=100,
        help_text="Enter the name of the university"
    )
    description = models.TextField(
        help_text="Add a description of your education"
    )

    def __str__(self):
        return f"{self.degree} - {self.university}"


# ------------------------------
# Experience Section
# ------------------------------
class Experience(models.Model):
    about_me = models.ForeignKey(
        AboutMe,
        on_delete=models.CASCADE,
        help_text="Select the profile this experience belongs to"
    )
    start_year = models.CharField(
        max_length=4,
        help_text="Start year, e.g., 2018"
    )
    end_year = models.CharField(
        max_length=4,
        help_text="End year, e.g., 2021"
    )
    position = models.CharField(
        max_length=100,
        help_text="Job position, e.g., Software Engineer"
    )
    company = models.CharField(
        max_length=100,
        help_text="Company name"
    )
    description = models.TextField(
        help_text="Describe your responsibilities and achievements"
    )

    def __str__(self):
        return f"{self.position} at {self.company}"



# ------------------------------
# Skills Section
# ------------------------------
class Skill(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Enter skill name, e.g., Python"
    )
    
    def __str__(self):
        return self.name
# ------------------------------

# ------------------------------
# Project Section
# ------------------------------
class Project(models.Model):
    title = models.CharField(
        max_length=100,
        help_text="Enter project title"
    )
    year = models.CharField(
        max_length=4,
        help_text="Enter project year, e.g., 2023"
    )
    client = models.CharField(
        max_length=100,
        help_text="Client name (optional)"
    )
    service = models.CharField(
        max_length=100,
        help_text="Type of service provided"
    )
    project_type = models.CharField(
        max_length=100,
        help_text="Project category/type"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Detailed description of the project"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Automatically generated slug from title"
    )
    is_active = models.BooleanField(
        default=False,
        help_text="Mark whether this project is active"
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Project creation date"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ------------------------------
# Project Images
# ------------------------------
class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        help_text="Select the project for this image"
    )
    image = models.ImageField(
        upload_to='project/image',
        help_text="Upload an image related to the project"
    )

    def __str__(self):
        return f"Image for {self.project.title}"

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=255, help_text="Foydalanuvchi ismi")
    email = models.EmailField(help_text="Foydalanuvchi emaili")
    subject = models.CharField(max_length=255, help_text="Xabar mavzusi")
    message = models.TextField(help_text="Xabar matni")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"

from django.db import models

class ContactInfo(models.Model):
    TYPE_CHOICES = (
        ('email', 'Email'),
        ('phone', 'Telefon'),
        ('address', 'Manzil'),
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        help_text="Kontakt turi: email, telefon yoki manzil"
    )
    title = models.CharField(
        max_length=100,
        help_text="Masalan: Email, Telefon, Manzil"
    )
    line1 = models.CharField(max_length=255, help_text="Birinchi qator")
    line2 = models.CharField(max_length=255, blank=True, null=True, help_text="Ikkinchi qator (ixtiyoriy)")
    line3 = models.CharField(max_length=255, blank=True, null=True, help_text="Uchinchi qator (ixtiyoriy)")

    def __str__(self):
        return f"{self.get_type_display()} - {self.line1}"




from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="blog/")
    content = RichTextField()

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="blogs"
    )
    tags = models.ManyToManyField(Tag, related_name="blogs", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            # unique qilish
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, related_name="comments", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=120)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Nested comment qo‘shish uchun parent field
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Comment by {self.name}"


from django.db import models

# Xizmatlar modeli
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Font Awesome yoki Iconoir klassini yozing")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=255, help_text="Banner main text")
    featured_text = models.CharField(max_length=255, help_text="Text to highlight")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ClientStat(models.Model):
    number = models.CharField(max_length=10, help_text="Raqam, masalan: 07 yoki +125")
    title = models.CharField(max_length=50, help_text="Stat sarlavhasi, masalan: Yillik Tajriba")
    description = models.CharField(max_length=100, help_text="Qo‘shimcha matn, masalan: Mijozlar butun dunyo bo‘ylab")
    is_active = models.BooleanField(default=True, help_text="Faol bo‘lsin yoki yo‘q")

    class Meta:
        verbose_name = "Mijoz Statistikasi"
        verbose_name_plural = "Mijoz Statistikalari"

    def __str__(self):
        return f"{self.number} - {self.title}"
