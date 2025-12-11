from django.contrib import admin
from .models import (
    CustomUser,AboutMe, Eduacation, Experience, Project, ProjectImage,
    ContactMessage, ContactInfo, Skill, Blog, Comment,Category,Tag,Service
)

# -----------------------------------------
# Custom User Admin
# -----------------------------------------
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "is_staff", "is_active")
    search_fields = ("email", "username")
    list_filter = ("is_staff", "is_active")
    ordering = ("email",)


# -----------------------------------------
# Education Inline for AboutMe
# -----------------------------------------
class EducationInline(admin.TabularInline):
    model = Eduacation
    extra = 1


# -----------------------------------------
# Experience Inline for AboutMe
# -----------------------------------------
class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


# -----------------------------------------
# About Me Admin
# -----------------------------------------
@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ("my_name", "user")
    search_fields = ("my_name", "user__email")
    list_filter = ("user",)
    filter_horizontal = ("skills",)
    inlines = [EducationInline, ExperienceInline]


# -----------------------------------------
# Skills Admin
# -----------------------------------------
@admin.register(Skill)  
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)




# Inline class for ProjectImage so that images can be added directly inside Project
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1  # nechta bo‘sh rasm qo‘shish mumkinligini belgilaydi

# Admin class for Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'client', 'project_type', 'is_active', 'create_at')
    list_filter = ('is_active', 'year', 'project_type')
    search_fields = ('title', 'client', 'service', 'project_type')
    prepopulated_fields = {"slug": ("title",)}  # slug avtomatik hosil bo‘lsin
    inlines = [ProjectImageInline]

# Admin registration for ProjectImage (agar alohida ko‘rsatmoqchi bo‘lsangiz)
@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'image')





@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'email', 'subject', 'message')



@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'line1', 'line2', 'line3')
    list_filter = ('type',)
    search_fields = ('title', 'line1', 'line2', 'line3')




@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'views')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('category', 'tags')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',) 


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)


from .models import Service

# Service modelini adminga qo'shish
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)



from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured_text', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'featured_text')


from .models import ClientStat

@admin.register(ClientStat)
class ClientStatAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('number', 'title', 'description')
