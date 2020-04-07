from django.contrib.auth.models import User, Profile
import django_filters

class TutorFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['classes_taken', 'location', ]