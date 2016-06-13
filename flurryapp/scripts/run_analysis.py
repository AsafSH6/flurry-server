import django
django.setup()

from flurryapp.models import Driver
from flurryapp.analysis.analyzer import Analyzer

if __name__ == '__main__':
    Analyzer(Driver.objects.extract_features(debug=True)).classify()
