import uvicorn

if __name__ == "__main__":
    uvicorn.run("pages.all_main:app", host="127.0.0.1", port=8000, reload=True)


#для docker
# if __name__ == "__main__":
#     uvicorn.run("pages.all_main:app", host="0.0.0.0", port=8000, reload=True)
