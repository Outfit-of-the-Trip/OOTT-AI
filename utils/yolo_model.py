import deepsparse
from deepsparse.yolo import Pipeline

def load_deepsparse_model(model_path):
    class_names = ['blazer', 'denim jacket', 'leather jacket', 'coat', 'windbreaker jacket', "cardigan", "puffer", "tee shirt", "long sleeve shirt", "tank top", "shirt", "polo shirt", "sweat shirt", "hoodie sweat shirt", "knit sweater", "dress", "jeans", "slacks", "sweat pants", "skirt", "shorts pants", "sneakers", "dress shoes", "sandals"]
    pipeline = Pipeline.create(
        task="yolov8",
        model_path=model_path,
        class_names = class_names,
        batch_size=None
    )
    return pipeline