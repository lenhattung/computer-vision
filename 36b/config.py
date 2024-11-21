# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAME_INTERVAL = 30  # milliseconds

# Recognition settings
FACE_CONFIDENCE_THRESHOLD = 0.6
MIN_APPEARANCES = 10
RECOGNITION_TIME = 15  # seconds

# Database settings
DB_FILE = 'attendance.db'

# GUI settings
WINDOW_TITLE = "Hệ thống điểm danh"
WINDOW_SIZE = "1200x700"
DEFAULT_CLASS = "21DTH"

# Model paths
MODEL_PATH = './'
FACE_DETECTION_MODEL = 'models/res10_300x300_ssd_iter_140000_fp16.caffemodel'
FACE_DETECTION_PROTO = 'models/deploy.prototxt.txt'
FACE_DESCRIPTOR = 'models/openface.nn4.small2.v1.t7'
FACE_RECOGNITION_MODEL = 'ml_face_person_identity.pkl'