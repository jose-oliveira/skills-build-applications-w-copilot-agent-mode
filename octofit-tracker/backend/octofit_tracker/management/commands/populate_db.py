
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Use PyMongo to clear collections directly
        client = MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']
        db.activity.delete_many({})
        db.leaderboard.delete_many({})
        db.workout.delete_many({})
        db.user.delete_many({})
        db.team.delete_many({})

        # Now use Django ORM to insert test data
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        users = [
            User.objects.create(email='tony@marvel.com', username='Iron Man', team=marvel),
            User.objects.create(email='steve@marvel.com', username='Captain America', team=marvel),
            User.objects.create(email='bruce@marvel.com', username='Hulk', team=marvel),
            User.objects.create(email='clark@dc.com', username='Superman', team=dc),
            User.objects.create(email='bruce@dc.com', username='Batman', team=dc),
            User.objects.create(email='diana@dc.com', username='Wonder Woman', team=dc),
        ]

        run = Workout.objects.create(name='5K Run', description='Run 5 kilometers', suggested_points=50)
        pushups = Workout.objects.create(name='100 Pushups', description='Do 100 pushups', suggested_points=30)

        Activity.objects.create(user=users[0], activity_type='run', duration_minutes=30, points=50)
        Activity.objects.create(user=users[1], activity_type='pushups', duration_minutes=10, points=30)
        Activity.objects.create(user=users[3], activity_type='run', duration_minutes=28, points=50)
        Activity.objects.create(user=users[4], activity_type='pushups', duration_minutes=12, points=30)

        Leaderboard.objects.create(team=marvel, total_points=80, month='November 2025')
        Leaderboard.objects.create(team=dc, total_points=80, month='November 2025')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
