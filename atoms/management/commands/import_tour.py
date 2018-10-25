import json
import os
import re
from json import JSONDecodeError

from atoms.models import Location, Media, Source, Text
from django.core.management.base import BaseCommand
from themes.models import Collection


class Command(BaseCommand):
    help = 'Imports data from the Portus tour into the database'

    def add_arguments(self, parser):
        parser.add_argument('collection', nargs=1, type=str)
        parser.add_argument('tour_path', nargs='+', type=str)

    def handle(self, *args, **options):
        collection_title = options['collection']
        collection, _ = Collection.objects.get_or_create(
            title=collection_title)

        for tour_path in options['tour_path']:
            if not os.path.isfile(tour_path):
                self.stderr.write('Invalid file path: {}'.format(tour_path))
                continue

            try:
                with open(tour_path) as f:
                    tour = json.load(f)

                self.stdout.write('Importing tour file: {}'.format(tour_path))
                self.import_tour(collection, os.path.basename(tour_path), tour)
            except JSONDecodeError as e:
                self.stderr.write(
                    'Failed to load the json file at: {}'. format(tour_path))
                continue

        # updates the term data for the collection
        collection.save()

    def import_tour(self, collection, title, data):
        source = self.get_or_create_source('tour: {}'.format(title))

        for slide in data['storymap']['slides']:
            text = self.get_or_create_text(collection, source, slide['text'])
            media = self.get_or_create_media(
                collection, source, slide['media'])
            location = self.get_or_create_location(
                collection, source, slide['location'])

            if media:
                text.items.add(media)
                media.items.add(text)
                if location:
                    media.items.add(location)
                media.save()

            if location:
                text.items.add(location)
                location.items.add(text)
                if media:
                    location.items.add(media)
                location.save()

            text.save()

    def get_or_create_source(self, title):
        source, _ = Source.objects.get_or_create(title=title)
        return source

    def get_or_create_text(self, collection, source, data):
        text, _ = Text.objects.get_or_create(
            source=source, title=data['headline'])
        text.collection = collection
        text.content = data['text']
        text.save()

        return text

    def get_or_create_media(self, collection, source, data):
        if not data['url']:
            return None

        url = self.get_url(data['url'])
        if not url:
            return None

        title = data['caption']
        if not title:
            title = url

        media, _ = Media.objects.get_or_create(
            source=source, title=title, url=url)
        media.collection = collection
        media.credit = data['credit']
        media.save()

        return media

    def get_url(self, text):
        url = None

        if not text:
            return None

        if 'http' in text:
            url = re.findall(r'http\S+', text)[0]
            url = url.replace('\'', '')
        else:
            url = 'https://tour.portusproject.org/{}'.format(url)

        return url

    def get_or_create_location(self, collection, source, data):
        lat = data['lat']
        lon = data['lon']

        if not lat or not lon:
            return None

        title = '{}, {}'.format(lat, lon)

        location, _ = Location.objects.get_or_create(
            source=source, title=title, lat=lat, lon=lon)
        location.collection = collection
        location.zoom = data['zoom']
        location.save()

        return location
