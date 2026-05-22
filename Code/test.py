import kagglehub

# Download latest version
path = kagglehub.model_download("google/gemma-3n/tfLite/gemma-3n-e2b-it-int4")

print("Path to model files:", path)