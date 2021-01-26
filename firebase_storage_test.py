import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


cred = credentials.Certificate("smart-attendance-584dc-firebase-adminsdk-mrqx9-f4215345a1.json")
fb_app = firebase_admin.initialize_app(cred,{'storageBucket': 'smart-attendance-584dc.appspot.com',}, name='storage')

bucket = storage.bucket(app=fb_app)
# blob = bucket.blob("user_photos/thura.jpg")
# blob.download_to_filename('faces/test.jpg')
