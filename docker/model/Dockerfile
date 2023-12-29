FROM nvcr.io/nvidia/pytorch:23.05-py3 as base

RUN pip install numpy torchvision

COPY aic .

WORKDIR aic/clsf_model/
