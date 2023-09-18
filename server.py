import argparse
from typing import List
from fastapi import FastAPI, UploadFile
import uvicorn
from starlette.responses import RedirectResponse
from fastapi.responses import JSONResponse, Response
from typing import List

from utils import get_image_info, transfer_data_to_db, load_deepsparse_model, load_config, from_image_to_bytes


def build_app(cfg):
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

    @app.post("/predict/batch", tags=["AI"], response_model=bool)
    async def batch_predict(request: List[UploadFile], recommend_type: str):
        if len(request) > 16: # Only receive 16 under data to protect server overload
            return False
        
        request = pipeline.input_schema.from_files(
                (file.file for file in request), from_server=True
        )
        request.iou_thres = 0.25
        request.conf_thres = 0.55
        pipeline_outputs = pipeline(request)
        crop_list, label_list, color_list, combi_list = get_image_info(
            request.images,
            pipeline_outputs.boxes,
            pipeline_outputs.labels,
            pipeline_outputs.scores
        )
        print("crop_list", crop_list)
        print("label_list", label_list)
        print("color_list", color_list)
        print("combi_list", combi_list)
        print(pipeline_outputs)
        
        return transfer_data_to_db(crop_list, label_list, color_list, combi_list, recommend_type)


    @app.post("/predict/each", tags=["AI"])
    async def each_predict(request: List[UploadFile]):
        request = pipeline.input_schema.from_files(
                (file.file for file in request), from_server=True
        )
        request.iou_thres = cfg['model']['iou_thres']
        request.conf_thres = cfg['model']['conf_thres']
        pipeline_outputs = pipeline(request)
        crop_list, label_list, color_list, combi_list = get_image_info(
            request.images,
            pipeline_outputs.boxes,
            pipeline_outputs.labels,
            pipeline_outputs.scores
        )
        
        print("crop_list", crop_list)
        print("label_list", label_list)
        print("color_list", color_list)
        print("combi_list", combi_list)
        # print(pipeline_outputs)
        
        # encoding_images = [from_image_to_bytes(img) for img in crop_list]
        print(type(crop_list[0]))
        print(crop_list[0])
        byte_test = crop_list[0]
        # return_json = {
        #     "byte_images": encoding_images,
        #     "label_list": label_list,
        #     "color_list": color_list
        # }
        return Response(content=byte_test, media_type="image/jpg")

    return app

def main(parser):
    cfg = parser.parse_args()
    cfg = load_config(cfg.config)
    
    app = build_app(cfg)
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