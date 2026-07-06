from django.contrib import admin
from .models import Student, Category, Candidate, Vote
from .models import AllowedVoter


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_registered')
    search_fields = ('email',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_open')
    list_editable = ('is_open',)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'vote_count')
    list_filter = ('category',)

    def vote_count(self, obj):
        return obj.vote_count()
    vote_count.short_description = 'Votes'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('student', 'candidate', 'category', 'timestamp', 'is_invalidated')
    list_filter = ('category', 'is_invalidated', 'candidate')
    list_editable = ('is_invalidated',)
    search_fields = ('student__email',)
    actions = ['invalidate_selected', 'restore_selected']

    def invalidate_selected(self, request, queryset):
        queryset.update(is_invalidated=True)
    invalidate_selected.short_description = "Mark selected votes as invalid"

    def restore_selected(self, request, queryset):
        queryset.update(is_invalidated=False)
    restore_selected.short_description = "Restore selected votes"



@admin.register(AllowedVoter)
class AllowedVoterAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)