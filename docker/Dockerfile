FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
# ------------------------------------------------------------------
# Close noninteractive
ENV DEBIAN_FRONTEND noninteractive
# ------------------------------------------------------------------
USER root
WORKDIR /workspace
# ------------------------------------------------------------------
# Install requirements.sh & entrypoint.sh
COPY ./docker /workspace/docker
RUN chmod u+x /workspace/docker/install.sh \
                && /workspace/docker/install.sh