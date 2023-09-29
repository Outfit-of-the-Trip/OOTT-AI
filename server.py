import argparse

from fastapi import FastAPI
import uvicorn
from starlette.responses import RedirectResponse

from utils import load_deepsparse_model, load_config
from utils import get_batch_info, get_camera_info, transfer_data_to_db
from utils import base64_list_to_image
from utils import CameraPredictIn, CameraPredictOut, BatchPredictIn, BatchPredictOut


def build_app(cfg, secret):
    """Load Yolov8 Model"""
    pipeline = load_deepsparse_model(model_path=cfg['model']['dir'])
    
    """Define AI API Server"""
    app = FastAPI()

    @app.get("/", include_in_schema=False)
    def _home():
        return RedirectResponse("/docs")

    @app.get("/ping", tags=["general"], response_model=bool)
    @app.get("/health", tags=["general"], response_model=bool)
    @app.get("/healthcheck", tags=["general"], response_model=bool)
    @app.get("/status", tags=["general"], response_model=bool)
    def _health():
        return True

    @app.post("/predict/batch", tags=["AI"], response_model=BatchPredictOut)
    async def batch_predict(request: BatchPredictIn):
        request_images_list = request.base64_images
        recommend_type = request.recommend_type
        
        request_images_list = [request_images_list[i:i+16] for i in range(0, len(request_images_list), 16)] # Only receive 16 under data to protect server overload
        for request in request_images_list:
            request = base64_list_to_image(request)
            request = [img[:,:,::-1] for img in request]
            pipeline_outputs = pipeline(
                images=request,
                iou_thres=cfg['model']['iou_thres'],
                conf_thres=cfg['model']['conf_thres']
            )
            
            crop_list, label_list, color_list, categori_list, combi_list, combi_color_list = get_batch_info(
                request,
                pipeline_outputs.boxes,
                pipeline_outputs.labels,
                pipeline_outputs.scores
            )
            transfer_data_to_db(crop_list, label_list, color_list, categori_list, combi_list, combi_color_list, recommend_type, secret)
        
        return_dict = {
            'result': True
        }
        return return_dict
        
    @app.post("/predict/camera", tags=["AI"], response_model=CameraPredictOut)
    async def camera_predict(request: CameraPredictIn):
        request = base64_list_to_image([request.base64_image])
        request = [img[:,:,::-1] for img in request]

        pipeline_outputs = pipeline(
            images=request[0],
            iou_thres=cfg['model']['iou_thres'],
            conf_thres=cfg['model']['conf_thres']
        )
        
        best_label, bset_color = get_camera_info(
            request,
            pipeline_outputs.boxes,
            pipeline_outputs.labels,
            pipeline_outputs.scores
        )
        
        return_dict = {
            'label': best_label,
            'color': bset_color
        }
        return return_dict
        
    return app


def main(parser):
    cfg = parser.parse_args()
    cfg = load_config(cfg.config)
    secret = load_config(cfg['secret_dir'])
    
    app = build_app(cfg, secret)
    uvicorn.run(
        app,
        host=cfg['info']['host'],
        port=cfg['info']['port'],
        log_level=cfg['info']['log_level'],
        workers=cfg['info']['workers'],
    )
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", 
        type=str, 
        default='./config/server.yaml',
        help="Set the config to Serve."
    )

    main(parser)