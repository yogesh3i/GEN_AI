from setuptools import find_packages,setup 

setup(
    name="QA system with Hystack",
    version="0.0.1",
    author = "Yogesh",
    author_email="yogideotale33@gmail.com",
    packages=find_packages(),
    install_requires = ["pinecone-haystack","haystack-ai","fastapi","uvicorn","python-dotenv"]
)