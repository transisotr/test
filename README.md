# test


# conda 环境安装谷歌云AI
conda install -c conda-forge google-genai


# Replace the `GOOGLE_CLOUD_PROJECT_ID` and `GOOGLE_CLOUD_LOCATION` values
# with appropriate values for your project.
export GOOGLE_CLOUD_PROJECT=train-max-20260104
export GOOGLE_CLOUD_LOCATION=global
export GOOGLE_GENAI_USE_VERTEXAI=True

# 在windows环境下设置环境变量
set GOOGLE_GENAI_USE_VERTEXAI=True
set GOOGLE_CLOUD_PROJECT=train-max-20260104
set GOOGLE_CLOUD_LOCATION=global

# 授权谷歌云AI
gcloud auth application-default login


# 1. 设置局部邮箱（只在这个文件夹生效）
git config user.email "robe_velocity@163.com"

# 2. 设置局部用户名
git config user.name "transisotr"

